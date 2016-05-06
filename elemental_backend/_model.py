import logging
import weakref
from functools import partial

from elemental_core.util import process_uuid_value

from .errors import (
    ResourceNotFoundError,
    ResourceNotRegisteredError,
    ResourceCollisionError,
    ResourceNotReleasedError
)
from .resources import (
    Resource,
    ContentType,
    AttributeType,
    AttributeInstance,
    ContentInstance
)
from ._util import (
    _resolve_attr_type,
    _Dict
)


_LOG = logging.getLogger(__name__)


class Model(object):
    """
    A `Model` manages `Resource` instances and their relationships.
    """
    def __init__(self):
        """
        Constructor for a `Model` instance.
        """
        super(Model, self).__init__()

        self._resources = _Dict()  # not dict() to allow for weak reffing
        self._map__resource_type__resources = {}
        self._map__content_type__content_instances = weakref.WeakKeyDictionary()
        self._map__content_instance__attribute_instances = weakref.WeakKeyDictionary()
        self._map__target_attr__source_attr = weakref.WeakKeyDictionary()
        self._map__attribute_type__content_type = weakref.WeakKeyDictionary()
        self._map__attribute_type__attribute_instances = weakref.WeakKeyDictionary()
        self._map__attribute_instance__content_instance = weakref.WeakKeyDictionary()
        self._map__resource_type__registrar = {
            Resource: self._register_resource,
            ContentType: self._register_content_type,
            ContentInstance: self._register_content_instance,
            AttributeType: self._register_attribute_type,
            AttributeInstance: self._register_attribute_instance
        }
        self._map__resource_type__deregistrar = {
            Resource: self._deregister_resource,
            ContentType: self._deregister_content_type,
            ContentInstance: self._deregister_content_instance,
            AttributeType: self._deregister_attribute_type,
            AttributeInstance: self._deregister_attribute_instance
        }

    def register_resource(self, resource):
        """
        Registers an elemental Resource instance.

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
                    'Registrar "{0}" failed - "{1}"\n'
                    'Model Integrity Compromised: '
                    'Registration rollback failed\n\t{2}'
                )
                msg = msg.format(problem_registrar.__name__,
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

        msg = 'Retrieved resource: "{0}" - "{1}"'
        msg = msg.format(repr(type(result)), result.id)
        _LOG.info(msg)
        return result

    def release_resource(self, resource_id):
        """
        Releases a previously registered elemental Resource instance.

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

    def _compute_resource_registrars(self, resource):
        result = {}
        for resource_type, registrar in self._map__resource_type__registrar.items():
            if isinstance(resource, resource_type):
                result[resource_type] = registrar
        return result

    def _compute_resource_deregistrars(self, resource):
        result = {}
        for resource_type, deregistrar in self._map__resource_type__deregistrar.items():
            if isinstance(resource, resource_type):
                result[resource_type] = deregistrar
        return result

    def _register_resource(self, resource):
        if resource.id in self._resources:
            msg = (
                'Failed to register resource with id "{0}": '
                'Resource already exists with id "{0}"'
            )
            msg = msg.format(resource.id)

            _LOG.error(msg)
            raise ResourceCollisionError(msg, resource_type=type(resource),
                                         resource_id=resource.id)

        try:
            type_resources = self._map__resource_type__resources[type(resource)]
        except KeyError:
            type_resources = weakref.WeakValueDictionary()
            self._map__resource_type__resources[type(resource)] = type_resources

        self._resources[resource.id] = resource
        type_resources[resource.id] = resource

    def _deregister_resource(self, resource):
        try:
            type_resources = self._map__resource_type__resources[type(resource)]
        except KeyError:
            msg = (
                'Failed to deregister resource with id "{0}": '
                'Unrecognized resource type "{1}".'
            )
            msg = msg.format(resource.id, repr(type(resource)))

            _LOG.error(msg)
            raise ResourceNotFoundError(msg, resource_type=type(resource),
                                        resource_id=resource.id)

        try:
            del self._resources[resource.id]
        except KeyError:
            msg = (
                'Failed to deregister resource: '
                'No resource found matching id "{0}"'
            )
            msg = msg.format(resource.id)

            _LOG.error(msg)
            raise ResourceNotFoundError(msg, resource_type=type(resource),
                                        resource_id=resource.id)

        try:
            del type_resources[resource.id]
        except KeyError:
            msg = (
                'Failed to deregister resource: '
                'No resource of type "{0}" found matching id "{1}".'
            )
            msg = msg.format(repr(type(resource)), resource.id)

            _LOG.error(msg)
            raise ResourceNotFoundError(msg, resource_type=type(resource),
                                        resource_id=resource.id)

    def _register_content_type(self, content_type):
        map_type_instances = self._map__content_type__content_instances
        if content_type.id not in map_type_instances:
            map_type_instances[content_type.id] = weakref.WeakSet()

        map_at_ct = self._map__attribute_type__content_type
        for attribute_type_id in content_type.attribute_type_ids:
            map_at_ct[attribute_type_id] = content_type.id

    def _deregister_content_type(self, content_type):
        del self._map__content_type__content_instances[content_type.id]

        map_at_ct = self._map__attribute_type__content_type
        for attribute_type_id in content_type.attribute_type_ids:
            del map_at_ct[attribute_type_id]

    def _register_content_instance(self, content_instance):
        if not content_instance.type_id:
            msg = (
                'Failed to register resource "{0}": '
                'Invalid type id - "{1}"'
            )
            msg = msg.format(repr(content_instance), content_instance.type_id)

            _LOG.error(msg)
            raise ResourceNotRegisteredError(
                msg, resource_type=type(content_instance),
                resource_id=content_instance.id)

        map_type_instances = self._map__content_type__content_instances
        try:
            content_instances = map_type_instances[content_instance.type_id]
        except KeyError:
            content_instances = weakref.WeakSet()
            map_type_instances[content_instance.type_id] = content_instances
        content_instances.add(content_instance.id)

        map_ai_ci = self._map__attribute_instance__content_instance
        for attribute_id in content_instance.attribute_ids:
            map_ai_ci[attribute_id] = content_instance.id

    def _deregister_content_instance(self, content_instance):
        map_type_instances = self._map__content_type__content_instances
        try:
            content_instances = map_type_instances[content_instance.type_id]
        except KeyError:
            pass
        else:
            try:
                content_instances.remove(content_instance.id)
            except KeyError:
                pass

        map_ai_ci = self._map__attribute_instance__content_instance
        for attribute_id in content_instance.attribute_ids:
            try:
                del map_ai_ci[attribute_id]
            except KeyError:
                pass

    def _register_attribute_type(self, attribute_type):
        map_type_instances = self._map__attribute_type__attribute_instances
        if attribute_type.id not in map_type_instances:
            map_type_instances[attribute_type.id] = weakref.WeakSet()

    def _deregister_attribute_type(self, attribute_type):
        del self._map__attribute_type__attribute_instances[attribute_type.id]

    def _register_attribute_instance(self, attribute_instance):
        """
        Note: No entry should be made to _map__attribute_instance__content_instance.
            Only when a ContentInstance is registered should an entry be made.
        """
        if not attribute_instance.type_id:
            msg = (
                'Failed to register resource "{0}": '
                'Invalid type id - "{1}"'
            )
            msg = msg.format(repr(attribute_instance),
                             attribute_instance.type_id)

            _LOG.error(msg)
            raise ResourceNotRegisteredError(
                msg, resource_type=type(attribute_instance),
                resource_id=attribute_instance.id)

        # The intention here is to set the value of the `attribute_instance`'s
        # `attribute_type` property to a callback. This callback will retrieve
        # the AttributeType resource using the value of
        # `attribute_instance.type_id` at the time of callback invocation.
        #
        # This is done so the order in which the `AttributeType` and
        # `AttributeInstance` come into existence will not matter. The
        # `AttributeType` only has to exist when the `attribute_type` property
        # is hit.
        attribute_instance.attribute_type = partial(
            _resolve_attr_type,
            weakref.proxy(attribute_instance),
            weakref.proxy(self._resources)
        )

        map_type_instances = self._map__attribute_type__attribute_instances
        try:
            attribute_instances = map_type_instances[attribute_instance.type_id]
        except KeyError:
            attribute_instances = weakref.WeakSet()
            map_type_instances[attribute_instance.type_id] = attribute_instances
        attribute_instances.add(attribute_instance)

    def _deregister_attribute_instance(self, attribute_instance):
        map_type_instances = self._map__attribute_type__attribute_instances
        try:
            attribute_instances = map_type_instances[attribute_instance.type_id]
        except KeyError:
            return
        try:
            attribute_instances.remove(attribute_instance)
        except KeyError:
            pass

        map_ai_ci = self._map__attribute_instance__content_instance
        try:
            del map_ai_ci[attribute_instance.id]
        except KeyError:
            pass
