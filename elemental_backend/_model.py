"""
Todo
    implement ViewResults (in progress)
    implement stale state management
    use stale state to lazily recompute ViewResults
    use stale state to lazily recompute ResourceReferences
"""
import logging
import weakref

from elemental_core import Hook
from elemental_core.util import process_uuid_value

from ._resource_model_base import ResourceModelBase
from ._util import iter_subclasses
from .errors import (
    ResourceNotFoundError,
    ResourceNotRegisteredError,
    ResourceCollisionError,
    ResourceNotReleasedError,
    ResourceNotRetrievedError
)


_LOG = logging.getLogger(__name__)


class Model(object):
    """
    A `Model` manages `Resource` instances and their relationships.
    """
    resource_registered = Hook()
    resource_registration_failed = Hook()
    resource_retrieved = Hook()
    resource_retrieval_failed = Hook()
    resource_released = Hook()
    resource_release_failed = Hook()

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

        for resource_model_cls in iter_subclasses(ResourceModelBase):
            resource_cls = resource_model_cls.__resource_cls__
            resource_indexes = resource_model_cls.__resource_indexes__

            resource_model = resource_model_cls(
                weakref.WeakMethod(self._resources.get),
                weakref.WeakMethod(self._resource_indexes.get))
            self.resource_registered += resource_model.resource_registered_handler
            self.resource_registration_failed += resource_model.resource_registration_failed_handler
            self.resource_retrieved += resource_model.resource_retrieved_handler
            self.resource_retrieval_failed += resource_model.resource_retrieval_failed_handler
            self.resource_released += resource_model.resource_released_handler
            self.resource_release_failed += resource_model.resource_release_failed_handler
            self._resource_models[resource_cls] = resource_model

            for index in resource_indexes:
                if index.key_type is resource_cls:
                    self._resource_indexes[(index.key_type, index.value_type)] = index

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
            raise ResourceNotRegisteredError(msg,
                                             resource_type=type(resource))

        if not resource_id:
            msg = (
                'Failed to register resource: '
                'Object "{0}" has invalid id - "{1}"'
            )
            msg = msg.format(repr(resource), resource_id)

            _LOG.error(msg)
            raise ResourceNotRegisteredError(msg,
                                             resource_type=type(resource),
                                             resource_id=resource_id)
        elif resource_id in self._resources:
            msg = (
                'Failed to register resource with id "{0}": '
                'Resource already exists with id "{0}"'
            )
            msg = msg.format(resource.id)

            _LOG.error(msg)
            raise ResourceCollisionError(msg,
                                         resource_type=type(resource),
                                         resource_id=resource.id)

        self._resources[resource.id] = resource
        map_rc_rs = self._map__resource_cls__resources
        try:
            resource_type_resources = map_rc_rs[type(resource)]
        except KeyError:
            resource_type_resources = weakref.WeakSet()
        resource_type_resources.add(resource.id)

        # The registration process iterates through all appropriate
        # ResourceModel instances, calling each model's register method.
        # In the event a register method fails, all previous models are
        # given the opportunity to release the resource.
        resource_models = self._compute_resource_models(resource)
        resource_models = [
            resource_models[resource_cls]
            for resource_cls in sorted(resource_models.keys(),
                                       key=lambda cls: len(cls.mro()))
            ]

        problem_model = None
        registration_error = None
        release_errors = []

        model_idx = 0
        while -1 < model_idx < len(resource_models):
            resource_model = resource_models[model_idx]

            if not registration_error:
                try:
                    resource_model.register(resource)
                    model_idx += 1
                except ResourceCollisionError as e:
                    raise e
                except ResourceNotRegisteredError as e:
                    registration_error = e
                    problem_model = resource_model
                    break
                except Exception as e:
                    registration_error = e
                    problem_model = resource_model
            else:
                try:
                    resource_model.release(resource)
                except Exception as e:
                    msg = '"{0}" release failed - "{1}"'
                    msg = msg.format(resource_model.__name__, e)
                    release_errors.append(msg)
                model_idx -= 1

        if not registration_error:
            try:
                self.resource_registered(self, resource)
            except Exception as e:
                registration_error = e
                try:
                    self.resource_registration_failed(self, resource)
                except Exception as e:
                    release_errors.append(e)

        if registration_error:
            if release_errors:
                msg = (
                    'Failed to register resource: '
                    'ResourceModel "{0}" failed - {1}: "{2}"\n'
                    'Model Integrity Compromised: '
                    'Registration rollback failed\n\t{2}'
                )
                msg = msg.format(problem_model.__name__,
                                 type(registration_error).__name__,
                                 str(registration_error),
                                 '\n\t'.join(release_errors))
            else:
                msg = (
                    'Failed to register resource: '
                    'ResourceModel "{0}" failed - "{1}"\n'
                    'Model integrity recovered: '
                    'Registration rollback succeeded'
                )
                msg = msg.format(problem_model.__name__,
                                 str(registration_error))

            _LOG.error(msg)
            raise ResourceNotRegisteredError(msg,
                                             resource_type=type(resource),
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
            resource_id = self._process_requested_resource_id(resource_id)
        except ValueError:
            msg = (
                'Failed to retrieve resource with id "{0}":'
                'Invalid UUID value.'
            )
            msg = msg.format(resource_id)
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
            raise ResourceNotFoundError(msg,
                                        resource_type=None,
                                        resource_id=resource_id)

        resource_models = self._compute_resource_models(result)
        resource_models = [
            resource_models[resource_cls]
            for resource_cls in sorted(resource_models.keys(),
                                       key=lambda cls: len(cls.mro()))
        ]
        problem_model = None
        retrieval_errors = []

        while not retrieval_errors and resource_models:
            resource_model = resource_models.pop(0)

            try:
                result = resource_model.retrieve(resource_id, resource=result)
            except ResourceNotFoundError:
                raise
            except Exception as e:
                retrieval_errors.append(e)
                problem_model = resource_model

        if not retrieval_errors:
            try:
                self.resource_retrieved(self, result)
            except Exception as e:
                retrieval_errors.append(e)
                try:
                    self.resource_retrieval_failed(self, result)
                except Exception as e:
                    retrieval_errors.append(e)

        if retrieval_errors:
            msg = (
                'Failed to retrieve resource: '
                'Model "{0}" retrieval failed:\n\t{0}'
            )
            msg = msg.format(problem_model.__name__,
                             '\n\t'.join([str(e) for e in retrieval_errors]))

            _LOG.error(msg)
            raise ResourceNotRetrievedError(msg,
                                            resource_type=type(result),
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
        exist, the Resource instance will be garbage collected.

        Args:
            resource_id (str or uuid): The ID of the `Resource` to release.

        Returns:
            The released `Resource` instance.
        """
        msg = 'Releasing resource: "{0}"'.format(resource_id)
        _LOG.info(msg)

        try:
            resource_id = self._process_requested_resource_id(resource_id)
        except ValueError:
            msg = (
                'Failed to release resource with id "{0}": '
                'Invalid UUID value.'
            )
            msg = msg.format(resource_id)

            _LOG.error(msg)
            raise ValueError(msg)

        try:
            result = self._resources.pop(resource_id)
            self._map__resource_cls__resources[type(result)].discard(result)
        except KeyError:
            msg = (
                'Failed to release resource:'
                'No resource found matching id "{0}"'
            )
            msg = msg.format(resource_id)

            _LOG.error(msg)
            raise ResourceNotFoundError(msg,
                                        resource_type=None,
                                        resource_id=resource_id)

        # The release process iterates through all appropriate
        # ResourceModel instances, calling each model's release method.
        # In the event a release method fails, all previous models are
        # given the opportunity to re-register the resource.
        resource_models = self._compute_resource_models(result)
        resource_models = [
            resource_models[resource_cls]
            for resource_cls in sorted(resource_models.keys(),
                                       key=lambda cls: len(cls.mro()))
        ]

        problem_model = None
        release_error = None
        registration_errors = []

        model_idx = len(resource_models) - 1
        while -1 < model_idx < len(resource_models):
            resource_model = resource_models[model_idx]

            if not release_error:
                try:
                    resource_model.release(result)
                    model_idx -= 1
                except ResourceCollisionError as e:
                    raise e
                except ResourceNotRegisteredError as e:
                    release_error = e
                    problem_model = resource_model
                    break
                except Exception as e:
                    release_error = e
                    problem_model = resource_model
            else:
                try:
                    resource_model.register(result)
                except Exception as e:
                    msg = '"{0}" release failed - "{1}"'
                    msg = msg.format(resource_model.__name__, e)
                    registration_errors.append(msg)
                model_idx += 1

        if not release_error:
            try:
                self.resource_released(self, result)
            except Exception as e:
                release_error = e
                try:
                    self.resource_release_failed(self, result)
                except Exception as e:
                    registration_errors.append(e)

        if release_error:
            if registration_errors:
                msg = (
                    'Failed to release resource: '
                    'Model "{0}" failed - "{1}"\n'
                    'Model Integrity Compromised: '
                    'Release rollback failed\n\t{2}'
                )
                msg = msg.format(problem_model.__name__,
                                 str(release_error),
                                 '\n\t'.join(registration_errors))
            else:
                msg = (
                    'Failed to release resource: '
                    'ResourceModel "{0}" failed - "{1}"\n'
                    'Model integrity recovered: '
                    'Release rollback succeeded'
                )
                msg = msg.format(problem_model.__name__,
                                 str(release_error))

            _LOG.error(msg)
            raise ResourceNotReleasedError(msg, resource_type=type(result),
                                           resource_id=resource_id)

        msg = 'Released resource: "{0}" - "{1}"'
        msg = msg.format(repr(type(result)), result.id)
        _LOG.info(msg)
        return result

    @staticmethod
    def _process_requested_resource_id(resource_id):
        result = process_uuid_value(resource_id)

        if not result:
            raise ValueError()

        return result

    def _compute_resource_models(self, resource):
        result = {}

        for resource_cls, resource_model in self._resource_models.iteritems():
            if isinstance(resource, resource_cls):
                result[resource_cls] = resource_model

        return result
