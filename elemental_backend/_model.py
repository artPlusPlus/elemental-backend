"""
Todo
    implement ViewResults (in progress)
    implement stale state management
    use stale state to lazily recompute ViewResults
    use stale state to lazily recompute ResourceReferences
"""
import logging
import weakref
import collections
from operator import attrgetter

from elemental_core import NO_VALUE
from elemental_core.util import process_uuid_value

from ._resource_index import ResourceIndex
from ._util import iter_subclasses
from ._resource_model_base import ResourceModelBase
from .errors import (
    ResourceError,
    ResourceNotFoundError,
    ResourceNotRegisteredError,
    ResourceCollisionError,
    ResourceNotReleasedError,
    ResourceNotRetrievedError
)


# from .resources import (
#     Resource,
#     ResourceType,
#     ResourceInstance,
#     ContentType,
#     ContentInstance,
#     AttributeType,
#     AttributeInstance,
#     ViewType,
#     ViewInstance,
#     ViewResult,
#     FilterType,
#     FilterInstance,
#     SorterType,
#     SorterInstance
# )


_LOG = logging.getLogger(__name__)


class Model(object):
    """
    A `Model` manages `Resource` instances and their relationships.
    """
    @property
    def index__resource_cls__resources(self):
        return self._map__resource_cls__resources

    def __init__(self):
        """
        Constructor for a `Model` instance.
        """
        super(Model, self).__init__()

        # The values of self._resources should be the only strong reference
        # Model makes to Resource objects.
        self._resources = weakref.WeakKeyDictionary()
        self._resource_models = weakref.WeakKeyDictionary()
        self._resource_indexes = weakref.WeakKeyDictionary()

        self._map__resource_cls__resources = weakref.WeakKeyDictionary()
        self._map__resource__stale_dependencies = weakref.WeakKeyDictionary()

        for resource_model in iter_subclasses(ResourceModelBase):
            resource_cls = resource_model.__resource_cls__
            resource_indexes = resource_model.__resource_indexes__

            self._resource_models[resource_cls] = resource_model(self)

            for index in resource_indexes:
                if index.key_type is resource_cls:
                    self._indexes[(index.key_type, index.value_type)] = index

    def register_resource(self, resource):
        """
        Registers an elemental Resource instance for management by the Model.

        When a Resource instance is registered, the Model will hold a single
        strong reference and multiple weak references to the Resource instance.

        Args:
            resource (Resource): A `Resource` instance to be managed by the `Model`.
        """
        msg = 'Registering resource: "{0}"'
        msg = msg.format(repr(type(resource)))
        _LOG.info(msg)

        try:
            resource_id = resource.id
        except AttributeError:
            msg = (
                'Failed to register resource: '
                'Object "{0}" has no attribute "id".'
            )
            msg = msg.format(repr(resource))

            _LOG.error(msg)
            raise ResourceNotRegisteredError(msg, resource_type=type(resource))

        if not resource_id:
            msg = (
                'Failed to register resource: '
                'Object "{0}" has invalid id - "{1}"'
            )
            msg = msg.format(repr(resource), resource_id)

            _LOG.error(msg)
            raise ResourceNotRegisteredError(msg, resource_type=type(resource),
                                             resource_id=resource_id)

        # Registrars create relationships between resources, while
        # Deregistrars unwind those relationships. Each Resource class must
        # have both a Registrar and Deregistrar
        registrars = self._compute_resource_registrars(resource)
        deregistrars = self._compute_resource_deregistrars(resource)

        if not registrars:
            msg = (
                'Failed to register resource: '
                'Unsupported type "{0}"'
            )
            msg = msg.format(repr(type(resource)))

            _LOG.error(msg)
            raise ResourceNotRegisteredError(msg, resource_type=type(resource),
                                             resource_id=resource_id)
        elif registrars.keys() != deregistrars.keys():
            msg = (
                'Failed to register resource: '
                'Mismatch in registrars/deregistrars for type "{0}"'
            )
            msg = msg.format(repr(type(resource)))

            _LOG.error(msg)
            raise ResourceNotRegisteredError(msg, resource_type=type(resource),
                                             resource_id=resource_id)

        # As registrars are associated with Resource classes, they are invoked
        # in reverse method resolution order; that is, registrars associated
        # with base classes are invoked before those associated with leaf-level
        # classes.
        sorted_resource_types = sorted(registrars.keys(),
                                       key=lambda cls: len(cls.mro()))
        sorted_deregistrars = []

        # A list of deregistrars is made as registrars are invoked.
        # In the event a registrar fails, the deregistrars are invoked in
        # normal method resolution order (leaf to base) in order to rollback
        # changes to the model.
        registrar_error = None
        problem_registrar = None
        while not registrar_error and sorted_resource_types:
            resource_type = sorted_resource_types.pop(0)
            registrar = registrars[resource_type]

            try:
                registrar(resource)
            except ResourceCollisionError as e:
                raise e
            except ResourceNotRegisteredError as e:
                registrar_error = e
                problem_registrar = registrar
                break
            except Exception as e:
                registrar_error = e
                problem_registrar = registrar

            sorted_deregistrars.append(deregistrars[resource_type])

        rollback_errors = []
        while registrar_error and sorted_deregistrars:
            deregistrar = sorted_deregistrars.pop()
            try:
                deregistrar(resource)
            except Exception as dr_e:
                msg = 'Deregistrar "{0}" failed - "{1}"'
                msg = msg.format(deregistrar.__name__, dr_e)
                rollback_errors.append(msg)

        if registrar_error:
            if rollback_errors:
                msg = (
                    'Failed to register resource: '
                    'Registrar "{0}" failed - {1}: "{2}"\n'
                    'Model Integrity Compromised: '
                    'Registration rollback failed\n\t{2}'
                )
                msg = msg.format(problem_registrar.__name__,
                                 str(type(registrar_error).__name__),
                                 str(registrar_error),
                                 '\n\t'.join(rollback_errors))
            else:
                msg = (
                    'Failed to register resource: '
                    'Registrar "{0}" failed - "{1}"\n'
                    'Model integrity recovered: '
                    'Registration rollback succeeded'
                )
                msg = msg.format(problem_registrar.__name__,
                                 str(registrar_error))

            _LOG.error(msg)
            raise ResourceNotRegisteredError(msg, resource_type=type(resource),
                                             resource_id=resource_id)

        msg = 'Registered resource: "{0}" - "{1}"'
        msg = msg.format(repr(type(resource)), resource.id)
        _LOG.info(msg)
        return resource

    def retrieve_resource(self, resource_id):
        """
        Retrieves a `Resource` instance managed by the `Model`.

        Args:
            resource_id (str or uuid): The ID of the `Resource` to retrieve.

        Returns:
            A `Resource` instance.
        """
        msg = 'Retrieving resource: "{0}"'.format(resource_id)
        _LOG.info(msg)

        try:
            _resource_id = process_uuid_value(resource_id)
        except ValueError:
            msg = (
                'Failed to retrieve resource with id "{0}": '
                'Invalid UUID value.'
            )
            msg = msg.format(resource_id)

            _LOG.error(msg)
            raise ValueError(msg)
        else:
            if _resource_id:
                resource_id = _resource_id
            else:
                msg = (
                    'Failed to retrieve resource with id "{0}":'
                    'Invalid UUID value'
                )
                msg = msg.format(_resource_id)

                _LOG.error(msg)
                raise ValueError(msg)

        try:
            result = self._resources[resource_id]
        except KeyError:
            msg = (
                'Failed to retrieve resource:'
                'No resource found matching id "{0}"'
            )
            msg = msg.format(resource_id)

            _LOG.error(msg)
            raise ResourceNotFoundError(msg, resource_type=None,
                                        resource_id=resource_id)

        retrievers = self._compute_resource_retrievers(result)
        sorted_resource_types = sorted(retrievers.keys(),
                                       key=lambda cls: len(cls.mro()))
        retriever_error = None
        problem_retriever = None
        while not retriever_error and sorted_resource_types:
            resource_type = sorted_resource_types.pop(0)
            retriever = retrievers[resource_type]

            try:
                result = retriever(result)
            except ResourceNotFoundError:
                raise
            except Exception as e:
                retriever_error = e
                problem_retriever = retriever

        if retriever_error:
            msg = (
                'Failed to retrieve resource: '
                'Retriever "{0}" failed - "{1}"'
            )
            msg = msg.format(problem_retriever.__name__,
                             str(retriever_error))

            _LOG.error(msg)
            raise ResourceNotRetrievedError(msg, resource_type=type(result),
                                            resource_id=resource_id)

        msg = 'Retrieved resource: "{0}" - "{1}"'
        msg = msg.format(repr(type(result)), result.id)
        _LOG.info(msg)
        return result

    def release_resource(self, resource_id):
        """
        Releases a previously registered elemental Resource instance from
            management by the Model.

        The Model will delete all references to the Resource instance,
        including its single strong reference. If no other strong references
        exist, the Resource instance will get garbage collected.

        Args:
            resource_id (str or uuid): The ID of the `Resource` to release.

        Returns:
            The released `Resource` instance.
        """
        msg = 'Releasing resource: "{0}"'.format(resource_id)
        _LOG.info(msg)

        result = self.retrieve_resource(resource_id)
        deregistrars = self._compute_resource_deregistrars(result)
        registrars = self._compute_resource_registrars(result)

        if not deregistrars:
            msg = (
                'Failed to release resource: '
                'Unsupported type "{0}"'
            )
            msg = msg.format(repr(type(result)))

            _LOG.error(msg)
            raise ResourceNotReleasedError(msg, resource_type=type(result),
                                           resource_id=resource_id)
        elif registrars.keys() != deregistrars.keys():
            msg = (
                'Failed to release resource: '
                'Mismatch in deregistrars/registrars for type "{0}"'
            )
            msg = msg.format(repr(type(result)))

            _LOG.error(msg)
            raise ResourceNotReleasedError(msg, resource_type=type(result),
                                           resource_id=resource_id)

        # As deregistrars are associated with Resource classes, they are
        # invoked in method resolution order; that is, registrars associated
        # with leaf-level classes are invoked before those associated with base
        # classes.
        sorted_resource_types = sorted(deregistrars.keys(),
                                       key=lambda cls: len(cls.mro()),
                                       reverse=True)
        # sorted_resource_types = reversed(sorted_resource_types)
        sorted_registrars = []

        # A list of registrars is made as deregistrars are invoked.
        # In the event a deregistrar fails, the registrars are invoked in
        # reverse method resolution order (base to leaf) in order to rollback
        # changes to the model.
        deregistrar_error = None
        problem_deregistrar = None
        while not deregistrar_error and sorted_resource_types:
            resource_type = sorted_resource_types.pop(0)
            deregistrar = deregistrars[resource_type]

            try:
                deregistrar(result)
            except ResourceNotReleasedError as e:
                deregistrar_error = e
                problem_deregistrar = deregistrar
                break
            except Exception as e:
                deregistrar_error = e
                problem_deregistrar = deregistrar

            sorted_registrars.append(deregistrars[resource_type])

        rollback_errors = []
        while deregistrar_error and sorted_registrars:
            registrar = sorted_registrars.pop()
            try:
                registrar(result)
            except Exception as r_e:
                msg = 'Registrar "{0}" failed - "{1}"'
                msg = msg.format(registrar.__name__, r_e)
                rollback_errors.append(msg)

        if deregistrar_error:
            if rollback_errors:
                msg = (
                    'Failed to release resource: '
                    'Deregistrar "{0}" failed - "{1}"\n'
                    'Model Integrity Compromised: '
                    'Deregistration rollback failed\n\t{2}'
                )
                msg = msg.format(problem_deregistrar.__name__,
                                 str(deregistrar_error),
                                 '\n\t'.join(rollback_errors))
            else:
                msg = (
                    'Failed to release resource: '
                    'Deregistrar "{0}" failed - "{1}"\n'
                    'Model integrity recovered: '
                    'Deregistration rollback succeeded'
                )
                msg = msg.format(problem_deregistrar.__name__,
                                 str(deregistrar_error))

            _LOG.error(msg)
            raise ResourceNotReleasedError(msg, resource_type=type(result),
                                           resource_id=resource_id)

        msg = 'Released resource: "{0}" - "{1}"'
        msg = msg.format(repr(type(result)), result.id)
        _LOG.info(msg)
        return result

    def _compute_resource_models(self, resource):
        result = {}

        for resource_cls, resource_model in self._resource_models.iteritems():
            if isinstance(resource, resource_cls):
                result[resource_cls] = resource_model

        return result

    def add_resource(self, resource):
        self._resources[resource.id] = resource

    def has_resource(self, resource):
        return resource.id in self._resources

    def get_resource(self, resource_id):
        return self._resources[resource_id]

    def remove_resource(self, resource):
        del self._resources[resource.id]

    def get_resource_index(self, key_type, value_type):
        index_key = (key_type, value_type)

        try:
            result = self._indexes[index_key]
        except KeyError:
            result = ResourceIndex()
            self._indexes[index_key] = result

        return result
