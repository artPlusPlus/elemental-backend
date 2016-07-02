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

from elemental_core import NO_VALUE
from elemental_core.util import process_uuid_value

from .errors import (
    ResourceError,
    ResourceNotFoundError,
    ResourceNotRegisteredError,
    ResourceCollisionError,
    ResourceNotReleasedError,
    ResourceNotRetrievedError
)
from .resources import (
    Resource,
    ResourceType,
    ResourceInstance,
    ContentType,
    ContentInstance,
    AttributeType,
    AttributeInstance,
    ViewType,
    ViewInstance,
    ViewResult,
    FilterType,
    FilterInstance
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

        # The values of self._resources should be the only strong reference
        # Model makes to Resource objects.
        self._resources = weakref.WeakKeyDictionary()

        # These collections represent associations between different types
        # of resources. These associations exist only in runtime and should not
        # be persisted beyond the lifetime of the Model instance.
        #
        # The keys and values of these collections are UUIDs that should be
        # resolvable to Resource objects found in self._resources.
        # The exception to this rule is _map__resource_cls__resources, whose
        # keys are (Resource) class objects.
        self._map__resource_cls__resources = weakref.WeakKeyDictionary()
        self._map__resource_type__resource_instances = weakref.WeakKeyDictionary()
        self._map__attribute_type__filter_types = weakref.WeakKeyDictionary()
        self._map__content_type__view_types = weakref.WeakKeyDictionary()
        self._map__view_type__content_instances = weakref.WeakKeyDictionary()
        self._map__attribute_instance__content_instance = weakref.WeakValueDictionary()
        self._map__filter_instance__view_instance = weakref.WeakKeyDictionary()
        self._map__view_result__view_instance = weakref.WeakKeyDictionary()

        self._map__resource__stale_dependencies = weakref.WeakKeyDictionary()

        # Registrar methods handle initial setup when a Resource instance
        # becomes managed by the Model.
        #
        # See Model.register_resource()
        self._map__resource_cls__registrar = weakref.WeakKeyDictionary()

        self._map__resource_cls__registrar[Resource] = self._register_resource

        self._map__resource_cls__registrar[ResourceType] = self._register_resource_type
        self._map__resource_cls__registrar[ContentType] = self._register_content_type
        self._map__resource_cls__registrar[AttributeType] = self._register_attribute_type
        self._map__resource_cls__registrar[ViewType] = self._register_view_type
        self._map__resource_cls__registrar[FilterType] = self._register_filter_type

        self._map__resource_cls__registrar[ResourceInstance] = self._register_resource_instance
        self._map__resource_cls__registrar[ContentInstance] = self._register_content_instance
        self._map__resource_cls__registrar[AttributeInstance] = self._register_attribute_instance
        self._map__resource_cls__registrar[ViewInstance] = self._register_view_instance
        self._map__resource_cls__registrar[FilterInstance] = self._register_filter_instance

        self._map__resource_cls__registrar[ViewResult] = self._register_view_result

        # Responder methods handle evaluation of resource data at the time of
        # retrieval.
        self._map__resource_cls__retriever = weakref.WeakKeyDictionary()

        # self._map__resource_cls__retriever[Resource] = self._retrieve_resource

        self._map__resource_cls__retriever[ViewResult] = self._retrieve_view_result

        # Releaser methods handle handle final teardown when a Resource
        # instance released from management by the Model.
        #
        # See Model.release_resource()
        self._map__resource_cls__releaser = weakref.WeakKeyDictionary()

        self._map__resource_cls__releaser[Resource] = self._release_resource

        self._map__resource_cls__releaser[ResourceType] = self._release_resource_type
        self._map__resource_cls__releaser[ContentType] = self._release_content_type
        self._map__resource_cls__releaser[AttributeType] = self._release_attribute_type
        self._map__resource_cls__releaser[ViewType] = self._release_view_type
        self._map__resource_cls__releaser[FilterType] = self._release_filter_type

        self._map__resource_cls__releaser[ResourceInstance] = self._release_resource_instance
        self._map__resource_cls__releaser[ContentInstance] = self._release_content_instance
        self._map__resource_cls__releaser[AttributeInstance] = self._release_attribute_instance
        self._map__resource_cls__releaser[ViewInstance] = self._release_view_instance
        self._map__resource_cls__releaser[FilterInstance] = self._release_filter_instance

        self._map__resource_cls__releaser[ViewResult] = self._release_view_result

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

    def _compute_resource_registrars(self, resource):
        result = {}
        for resource_class, registrar in self._map__resource_cls__registrar.items():
            if isinstance(resource, resource_class):
                result[resource_class] = registrar
        return result

    def _compute_resource_retrievers(self, resource):
        result = {}
        for resource_class, registrar in self._map__resource_cls__retriever.items():
            if isinstance(resource, resource_class):
                result[resource_class] = registrar
        return result

    def _compute_resource_deregistrars(self, resource):
        result = {}
        for resource_type, deregistrar in self._map__resource_cls__releaser.items():
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

        self._resources[resource.id] = resource

        map_rc_rs = self._map__resource_cls__resources
        cls_resources = map_rc_rs.setdefault(type(resource), weakref.WeakSet())
        cls_resources.add(resource.id)

        hook = resource.id_changed
        handler = self._handle_resource_id_changed
        hook.add_handler(handler)

    # def _retrieve_resource(self, resource_id, resource):
        # try:
        #     return self._resources[resource_id]
        # except KeyError:
        #     msg = (
        #         'Failed to retrieve resource:'
        #         'No resource found matching id "{0}"'
        #     )
        #     msg = msg.format(resource_id)
        #
        #     _LOG.error(msg)
        #     raise ResourceNotFoundError(msg, resource_type=None,
        #                                 resource_id=resource_id)

    def _release_resource(self, resource):
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

        map_rc_rs = self._map__resource_cls__resources
        try:
            map_rc_rs[type(resource)].discard(resource.id)
        except KeyError:
            msg = (
                'Failed to deregister resource with id "{0}": '
                'Unrecognized resource type "{1}".'
            )
            msg = msg.format(resource.id, repr(type(resource)))

            _LOG.error(msg)
            raise ResourceNotFoundError(msg, resource_type=type(resource),
                                        resource_id=resource.id)

        hook = resource.id_changed
        handler = self._handle_resource_id_changed
        hook.remove_handler(handler)

    def _register_resource_type(self, resource_type):
        map_type_instances = self._map__resource_type__resource_instances
        self._fix_map_key(map_type_instances, resource_type.id, weakref.WeakSet)

        hook = resource_type.name_changed
        handler = self._handle_resource_type_name_changed
        hook.add_handler(handler)

        ref = type(resource_type).resource_instances
        resolver = self._resolve_resource_type_resource_instances
        ref.add_resolver(resource_type, resolver)

    def _release_resource_type(self, resource_type):
        map_type_instances = self._map__resource_type__resource_instances

        try:
            del map_type_instances[resource_type.id]
        except KeyError:
            msg = (
                'ResourceType "{0}" not found in '
                'ResourceType:ResourceInstances map during deregistration.'
                'This is unexpected and could be a symptom of a problematic'
                'model.'
            )
            msg = msg.format(resource_type.id)

            _LOG.warn(msg)

        hook = resource_type.name_changed
        handler = self._handle_resource_type_name_changed
        hook.remove_handler(handler)

        ref = type(resource_type).resource_instances
        ref.remove_resolver(resource_type)

    def _register_resource_instance(self, resource_instance):
        map_type_instances = self._map__resource_type__resource_instances

        instance_ids = map_type_instances.setdefault(resource_instance.type_id,
                                                     weakref.WeakSet())
        instance_ids.add(resource_instance.id)

        hook = resource_instance.type_id_changed
        handler = self._handle_resource_instance_type_id_changed
        hook.add_handler(handler)

        ref = type(resource_instance).type
        resolver = self._resolve_resource
        ref.add_resolver(resource_instance, resolver)

    def _release_resource_instance(self, resource_instance):
        map_type_instances = self._map__resource_type__resource_instances

        try:
            instance_ids = map_type_instances[resource_instance.type_id]
        except KeyError:
            return
        else:
            instance_ids.remove(resource_instance.id)

        hook = resource_instance.type_id_changed
        handler = self._handle_resource_instance_type_id_changed
        hook.remove_handler(handler)

        ref = type(resource_instance).type
        ref.remove_resolver(resource_instance)

    def _register_content_type(self, content_type):
        map_ct_vts = self._map__content_type__view_types
        self._fix_map_key(map_ct_vts, content_type.id, weakref.WeakSet)

        for view_type_id in map_ct_vts[content_type.id]:
            try:
                view_type = self._resources[view_type_id]
            except KeyError:
                pass
            else:
                view_type.stale = True

        hook = content_type.base_ids_changed
        handler = self._handle_content_type_base_ids_changed
        hook.add_handler(handler)

        hook = content_type.attribute_type_ids_changed
        handler = self._handle_content_type_attribute_type_ids_changed
        hook.add_handler(handler)

        ref = type(content_type).attribute_types
        resolver = self._resolve_resources
        ref.add_resolver(content_type, resolver)

        ref = type(content_type).view_types
        resolver = self._resolve_content_type_view_types
        ref.add_resolver(content_type, resolver)

    def _release_content_type(self, content_type):
        map_ct_vts = self._map__content_type__view_types
        try:
            view_type_ids = map_ct_vts.pop(content_type.id)
        except KeyError:
            pass
        else:
            for view_type_id in view_type_ids:
                try:
                    view_type = self._resources[view_type_id]
                except KeyError:
                    pass
                else:
                    view_type.stale = True

        hook = content_type.base_ids_changed
        handler = self._handle_content_type_base_ids_changed
        hook.remove_handler(handler)

        hook = content_type.attribute_type_ids_changed
        handler = self._handle_content_type_attribute_type_ids_changed
        hook.remove_handler(handler)

        ref = type(content_type).attribute_types
        ref.remove_resolver(content_type)

        ref = type(content_type).view_types
        ref.remove_resolver(content_type)

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

        map_ai_ci = self._map__attribute_instance__content_instance
        for attribute_id in content_instance.attribute_ids:
            map_ai_ci[attribute_id] = content_instance.id

        map_ct_vts = self._map__content_type__view_types
        map_rt_ris = self._map__resource_type__resource_instances

        view_type_ids = map_ct_vts.get(content_instance.type_id, [])
        for view_type_id in view_type_ids:
            self._update_view_type_content_instances(view_type_id)
            view_instance_ids = map_rt_ris[view_type_id]
            # for view_instance_id in view_instance_ids:
            #     self._update_view_instance_content_instances(
            #         view_instance_id, content_instance_ids=content_instance)

        hook = content_instance.attribute_ids_changed
        handler = self._handle_content_instance_attribute_ids_changed
        hook.add_handler(handler)

        ref = type(content_instance).attributes
        resolver = self._resolve_resources
        ref.add_resolver(content_instance, resolver)

    def _release_content_instance(self, content_instance):
        map_ai_ci = self._map__attribute_instance__content_instance
        for attribute_id in content_instance.attribute_ids:
            try:
                del map_ai_ci[attribute_id]
            except KeyError:
                pass

        # self._update_view_instance_content_instances()

        hook = content_instance.attribute_ids_changed
        handler = self._handle_content_instance_attribute_ids_changed
        hook.remove_handler(handler)

        ref = type(content_instance).attributes
        ref.remove_resolver(content_instance)

    def _register_attribute_type(self, attribute_type):
        map_at_fts = self._map__attribute_type__filter_types
        self._fix_map_key(map_at_fts, attribute_type.id,
                          items_container_type=weakref.WeakSet)

        # self._update_view_instance_content_instances()

        hook = attribute_type.default_value_changed
        handler = self._handle_attribute_type_default_value_changed
        hook.add_handler(handler)

        hook = attribute_type.kind_id_changed
        handler = self._handle_attribute_type_kind_id_changed
        hook.add_handler(handler)

        hook = attribute_type.kind_properties_changed
        handler = self._handle_attribute_type_kind_properties_changed
        hook.add_handler(handler)

        ref = type(attribute_type).filter_types
        resolver = self._resolve_attribute_type_filter_types
        ref.add_resolver(attribute_type, resolver)

    def _release_attribute_type(self, attribute_type):
        map_at_fts = self._map__attribute_type__filter_types
        try:
            del map_at_fts[attribute_type.id]
        except KeyError:
            pass

        # self._update_view_instance_content_instances()
        hook = attribute_type.default_value_changed
        handler = self._handle_attribute_type_default_value_changed
        hook.remove_handler(handler)

        hook = attribute_type.kind_id_changed
        handler = self._handle_attribute_type_kind_id_changed
        hook.remove_handler(handler)

        hook = attribute_type.kind_properties_changed
        handler = self._handle_attribute_type_kind_properties_changed
        hook.remove_handler(handler)

        ref = type(attribute_type).filter_types
        ref.remove_resolver(attribute_type)

    def _register_attribute_instance(self, attribute_instance):
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

        map_ai_ci = self._map__attribute_instance__content_instance
        self._fix_map_key(map_ai_ci, attribute_instance.id)

        # self._update_view_instance_content_instances()

        hook = attribute_instance.value_changed
        handler = self._handle_attribute_instance_value_changed
        hook.add_handler(handler)

        hook = attribute_instance.source_id_changed
        handler = self._handle_attribute_instance_source_id_changed
        hook.add_handler(handler)

        ref = type(attribute_instance).source
        resolver = self._resolve_resource
        ref.add_resolver(attribute_instance, resolver)

        ref = type(attribute_instance).content_instance
        resolver = self._resolve_attribute_instance_content_instance
        ref.add_resolver(attribute_instance, resolver)

    def _release_attribute_instance(self, attribute_instance):
        map_ai_ci = self._map__attribute_instance__content_instance
        try:
            del map_ai_ci[attribute_instance.id]
        except KeyError:
            pass

        # self._update_view_instance_content_instances()

        hook = attribute_instance.value_changed
        handler = self._handle_attribute_instance_value_changed
        hook.remove_handler(handler)

        hook = attribute_instance.source_id_changed
        handler = self._handle_attribute_instance_source_id_changed
        hook.remove_handler(handler)

        ref = type(attribute_instance).source
        ref.remove_resolver(attribute_instance)

        ref = type(attribute_instance).content_instance
        ref.remove_resolver(attribute_instance)

    def _register_view_type(self, view_type):
        map_vt_cis = self._map__view_type__content_instances
        if view_type.id not in map_vt_cis:
            map_vt_cis[view_type.id] = weakref.WeakSet()

        map_ct_vts = self._map__content_type__view_types
        for content_type_id in view_type.content_type_ids:
            view_type_ids = map_ct_vts.setdefault(content_type_id,
                                                  weakref.WeakSet())
            view_type_ids.add(view_type.id)

        self._update_view_type_content_instances(view_type.id)

        hook = view_type.content_type_ids_changed
        handler = self._handle_view_type_content_type_ids_changed
        hook.add_handler(handler)

        hook = view_type.filter_type_ids_changed
        handler = self._handle_view_type_filter_type_ids_changed
        hook.add_handler(handler)

        ref = type(view_type).content_types
        resolver = self._resolve_resources
        ref.add_resolver(view_type, resolver)

        ref = type(view_type).filter_types
        resolver = self._resolve_resources
        ref.add_resolver(view_type, resolver)

        ref = type(view_type).content_instances
        resolver = self._resolve_view_type_content_instances
        ref.add_resolver(view_type, resolver)

    def _release_view_type(self, view_type):
        del self._map__view_type__content_instances[view_type.id]

        hook = view_type.content_type_ids_changed
        handler = self._handle_view_type_content_type_ids_changed
        hook.remove_handler(handler)

        hook = view_type.filter_type_ids_changed
        handler = self._handle_view_type_filter_type_ids_changed
        hook.remove_handler(handler)

        ref = type(view_type).content_types
        ref.remove_resolver(view_type)

        ref = type(view_type).filter_types
        ref.remove_resolver(view_type)

        ref = type(view_type).content_instances
        ref.remove_resolver(view_type)

    def _register_view_instance(self, view_instance):
        if not view_instance.type_id:
            msg = (
                'Failed to register resource "{0}": '
                'Invalid type id - "{1}"'
            )
            msg = msg.format(repr(view_instance), view_instance.type_id)

            _LOG.error(msg)
            raise ResourceNotRegisteredError(
                msg, resource_type=type(view_instance),
                resource_id=view_instance.id)

        map_fi_vi = self._map__filter_instance__view_instance
        for filter_instance_id in view_instance.filter_ids:
            map_fi_vi[filter_instance_id] = view_instance.id

        map_vr_vi = self._map__view_result__view_instance
        map_vr_vi[view_instance.result_id] = view_instance.id

        hook = view_instance.filter_ids_changed
        handler = self._handle_view_instance_filter_ids_changed
        hook.add_handler(handler)

        hook = view_instance.result_id_changed
        handler = self._handle_view_instance_result_id_changed
        hook.add_handler(handler)

        ref = type(view_instance).filter_instances
        resolver = self._resolve_resources
        ref.add_resolver(view_instance, resolver)

        ref = type(view_instance).result
        resolver = self._resolve_resource
        ref.add_resolver(view_instance, resolver)

    def _release_view_instance(self, view_instance):
        hook = view_instance.filter_ids_changed
        handler = self._handle_view_instance_filter_ids_changed
        hook.remove_handler(handler)

        hook = view_instance.result_id_changed
        handler = self._handle_view_instance_result_id_changed
        hook.remove_handler(handler)

        ref = type(view_instance).filter_instances
        ref.remove_resolver(view_instance)

        ref = type(view_instance).result
        ref.remove_resolver(view_instance)

    def _register_view_result(self, view_result):
        hook = view_result.content_instance_ids_changed
        handler = self._handle_view_result_content_instance_ids_changed
        hook.add_handler(handler)

        ref = type(view_result).view_instance
        resolver = self._resolve_view_result_view_instance
        ref.add_resolver(view_result, resolver)

        ref = type(view_result).content_instances
        resolver = self._resolve_resources
        ref.add_resolver(view_result, resolver)

    def _retrieve_view_result(self, view_result):
        result = view_result

        self._update_view_result_content_instances(view_result.id)

        return result

    def _release_view_result(self, view_result):
        map_vr_vi = self._map__view_result__view_instance
        try:
            del map_vr_vi[view_result.id]
        except KeyError:
            pass

        hook = view_result.content_instance_ids_changed
        handler = self._handle_view_result_content_instance_ids_changed
        hook.remove_handler(handler)

        ref = type(view_result).view_instance
        ref.remove_resolver(view_result)

        ref = type(view_result).content_instances
        ref.remove_resolver(view_result)

    def _register_filter_type(self, filter_type):
        map_at_fts = self._map__attribute_type__filter_types
        for attribute_type_id in filter_type.attribute_type_ids:
            try:
                filter_types = map_at_fts[attribute_type_id]
            except KeyError:
                filter_types = weakref.WeakSet()
            filter_types.add(filter_type.id)

        # self._update_view_instance_content_instances()

        hook = filter_type.attribute_type_ids_changed
        handler = self._handle_filter_type_attribute_type_ids_changed
        hook.add_handler(handler)

        ref = type(filter_type).attribute_types
        resolver = self._resolve_resources
        ref.add_resolver(filter_type, resolver)

    def _release_filter_type(self, filter_type):
        map_at_fts = self._map__attribute_type__filter_types
        for attribute_type_id in filter_type.attribute_type_ids:
            try:
                map_at_fts[attribute_type_id].discard(filter_type.id)
            except KeyError:
                pass

        # self._update_view_instance_content_instances()

        hook = filter_type.attribute_type_ids_changed
        handler = self._handle_filter_type_attribute_type_ids_changed
        hook.remove_handler(handler)

        ref = type(filter_type).attribute_types
        ref.remove_resolver(filter_type)

    def _register_filter_instance(self, filter_instance):
        map_fi_vi = self._map__filter_instance__view_instance
        self._fix_map_key(map_fi_vi, filter_instance.id)

        # self._update_view_instance_content_instances()

        hook = filter_instance.kind_params_changed
        handler = self._handler_filter_instance_kind_params_changed
        hook.add_handler(handler)

        ref = type(filter_instance).view_instance
        resolver = self._resolve_filter_instance_view_instance
        ref.add_resolver(filter_instance, resolver)

    def _release_filter_instance(self, filter_instance):
        map_fi_vi = self._map__filter_instance__view_instance
        try:
            del map_fi_vi[filter_instance.id]
        except KeyError:
            pass

        # self._update_view_instance_content_instances()

        hook = filter_instance.kind_params_changed
        handler = self._handler_filter_instance_kind_params_changed
        hook.remove_handler(handler)

        ref = type(filter_instance).view_instance
        ref.remove_resolver(filter_instance)

    def _handle_resource_id_changed(
            self, sender, event_data):
        msg = 'Mutable Ids are not supported.'

        _LOG.error(msg)
        raise ResourceError(msg, resource_type=type(sender),
                            resource_id=sender.id)

    def _handle_resource_type_name_changed(
            self, sender, event_data):
        pass

    def _handle_resource_instance_type_id_changed(
            self, sender, event_data):
        original_value, current_value = event_data
        map_rt_ris = self._map__resource_type__resource_instances
        try:
            map_rt_ris[original_value].discard(sender.id)
        except KeyError:
            pass

        try:
            resource_instance_ids = map_rt_ris[current_value]
        except KeyError:
            resource_instance_ids = weakref.WeakSet()
            map_rt_ris[current_value] = resource_instance_ids
        resource_instance_ids.add(sender.id)

    def _handle_content_type_base_ids_changed(
            self, sender, event_data):
        pass

    def _handle_content_type_attribute_type_ids_changed(
            self, sender, event_data):
        pass

    def _handle_content_instance_attribute_ids_changed(
            self, sender, event_data):
        pass

    def _handle_attribute_type_default_value_changed(
            self, sender, event_data):
        pass

    def _handle_attribute_type_kind_id_changed(
            self, sender, event_data):
        pass

    def _handle_attribute_type_kind_properties_changed(
            self, sender, event_data):
        pass

    def _handle_attribute_instance_value_changed(
            self, sender, event_data):
        map_at_fts = self._map__attribute_type__filter_types

        filter_type_ids = map_at_fts.get(sender.type_id)
        if not filter_type_ids:
            return

        map_ai_ci = self._map__attribute_instance__content_instance
        content_instance = self._resources[map_ai_ci[sender.id]]
        content_type_id = content_instance.type_id

        map_ct_vts = self._map__content_type__view_types
        view_type_ids = map_ct_vts[content_type_id]

        map_rt_ris = self._map__resource_type__resource_instances
        for view_type_id in view_type_ids:
            view_instance_ids = map_rt_ris[view_type_id]
            # for view_instance_id in view_instance_ids:
                # self._update_view_instance_content_instances(
                #     view_instance_id, content_instance_ids=content_instance.id)

    def _handle_attribute_instance_source_id_changed(
            self, sender, event_data):
        original_value, current_value = event_data

        map_sa_tas = self._map__source_attr__target_attrs
        try:
            map_sa_tas[original_value].discard(sender.id)
        except KeyError:
            pass

        try:
            target_ids = map_sa_tas[current_value]
        except KeyError:
            target_ids = weakref.WeakSet()
            map_sa_tas[current_value] = target_ids
        target_ids.add(sender.id)

    def _handle_view_type_content_type_ids_changed(
            self, sender, event_data):
        self._update_view_type_content_instances(sender.id)

        map_rt_ri = self._map__resource_type__resource_instances
        # for view_inst_id in map_rt_ri[sender.id]:
        #     self._update_view_instance_content_instances(view_inst_id)

    def _handle_view_type_filter_type_ids_changed(
            self, sender, event_data):
        map_rt_ri = self._map__resource_type__resource_instances
        # for view_inst_id in map_rt_ri[sender.id]:
        #     self._update_view_instance_content_instances(view_inst_id)

    def _handle_view_instance_filter_ids_changed(
            self, sender, event_data):
        original_value, current_value = event_data

        map_fi_vi = self._map__filter_instance__view_instance

        for filter_instance_id in set(original_value).difference(current_value):
            map_fi_vi[filter_instance_id] = None

        for filter_instance_id in current_value:
            map_fi_vi[filter_instance_id] = sender.id

        # self._update_view_instance_content_instances(sender.id)

    def _handle_view_instance_result_id_changed(
            self, sender, event_data):
        original_value, current_value = event_data

        # self._update_view_instance_content_instances(sender.id)

    def _handle_view_result_content_instance_ids_changed(
            self, sender, event_data):
        pass

    def _handle_filter_type_attribute_type_ids_changed(
            self, sender, event_data):
        original_value, current_value = event_data

        added_attr_type_ids = set(current_value).difference(current_value)
        removed_attr_type_ids = set(original_value).difference(current_value)

        map_at_fts = self._map__attribute_type__filter_types
        for attr_type_id in removed_attr_type_ids:
            try:
                filter_type_ids = map_at_fts[attr_type_id]
            except KeyError:
                pass
            else:
                filter_type_ids.discard(sender.id)

        for attr_type_id in added_attr_type_ids:
            filter_type_ids = map_at_fts.setdefault(attr_type_id, weakref.WeakSet())
            filter_type_ids.add(sender.id)

        map_rt_ri = self._map__resource_type__resource_instances
        map_fi_vi = self._map__filter_instance__view_instance
        for filter_inst_id in map_rt_ri[sender.id]:
            view_inst_id = map_fi_vi[filter_inst_id]
            # self._update_view_instance_content_instances(view_inst_id)

    def _handler_filter_instance_kind_params_changed(
            self, sender, event_data):
        map_fi_vi = self._map__filter_instance__view_instance
        view_inst_id = map_fi_vi[sender.id]
        # self._update_view_instance_content_instances(view_inst_id)

    def _update_view_type_content_instances(self, view_type_id):
        """
        Builds a mapping of all ContentInstances that qualify for a ViewType.

        A ViewType holds references to ContentTypes. All ContentInstances
        of each of these ContentTypes form a base pool. This pool is used by
        the ViewType's ViewInstances. The ViewInstances apply the
        FilterInstances to each ContentInstance in the pool to compute the
        data for a corresponding ViewResult.
        """
        view_type = self._resources[view_type_id]
        map_rt_ri = self._map__resource_type__resource_instances
        map_vt_cis = self._map__view_type__content_instances

        content_inst_ids = map_vt_cis[view_type.id]
        content_inst_ids.clear()
        for type_id in view_type.content_type_ids:
            content_inst_ids.update(map_rt_ri.get(type_id, tuple()))

    def _update_view_result_content_instances(
            self, view_result_id, content_instance_ids=None,
            filter_instance_ids=None):
        """
        Computes the ContentInstances referenced by a ViewResult.

        A ViewResult references ContentInstances that match criteria defined
        by FilterInstances that are managed by the ViewResult's corresponding
        ViewInstance.
        """
        view_result = self._resources.get(view_result_id)
        if not view_result:
            return

        view_instance = view_result.view_instance
        if not view_instance:
            return

        view_result_content_instance_ids = view_result.content_instance_ids.copy()

        if filter_instance_ids:
            if isinstance(filter_instance_ids, collections.Iterable):
                filter_instances = self._resolve_resources(filter_instance_ids)
            else:
                try:
                    filter_instances = self._resources[filter_instance_ids]
                except KeyError:
                    msg = 'Invalid value for filter_instance_ids: {0}'
                    msg = msg.format(filter_instance_ids)

                    _LOG.error(msg)
                    raise ValueError(msg)
                else:
                    filter_instances = [filter_instances]
        else:
            filter_instances = view_instance.filter_instances

        if not filter_instances:
            return

        if not content_instance_ids:
            map_vt_cis = self._map__view_type__content_instances
            content_instance_ids = map_vt_cis.get(view_instance.type_id, set())

            # This intersection update accounts for when a ViewType no longer
            # references a ContentType. The ContentInstance Ids of the discarded
            # ContentType need to be purged from the ViewResult.
            view_result_content_instance_ids.intersection_update(content_instance_ids)
        elif not isinstance(content_instance_ids, collections.Iterable):
            content_instance_ids = [content_instance_ids]

        for content_inst_id in content_instance_ids:
            try:
                content_inst = self._resources[content_inst_id]
            except KeyError:
                view_result_content_instance_ids.discard(content_inst_id)
                continue

            if self._apply_filters(content_inst, filter_instances):
                view_result_content_instance_ids.add(content_inst_id)
            else:
                view_result_content_instance_ids.discard(content_inst_id)
        view_result.content_instance_ids = view_result_content_instance_ids

    def _apply_filters(self, content_instance, filter_instances):
        attr_inst_resolver = self._resolve_content_instance_attribute_instance_from_attribute_type

        for filter_inst in filter_instances:
            filter_type = filter_inst.type
            for attr_type_id in filter_type.attribute_type_ids:
                attr_inst = attr_inst_resolver(content_instance.id, attr_type_id)
                if attr_inst:
                    attr_type = self._resources.get(attr_type_id)
                    break
            else:
                attr_inst = None
                attr_type = None

            if not all((attr_type, attr_inst)):
                return False

            attr_kind = attr_type.kind
            attr_value = attr_inst.value
            filter_params = filter_inst.kind_params
            if not attr_kind.filter_value(attr_value, **filter_params):
                return False

        return True

    def _resolve_resource(self, resource_id):
        return self._resources.get(resource_id)

    def _resolve_resources(self, resource_ids):
        result = [self._resources.get(r_id) for r_id in resource_ids]
        result = [attr for attr in result if attr]
        if len(result) == len(resource_ids):
            return result
        return tuple()

    def _resolve_resource_type_resource_instances(self, resource_type_id):
        map_rt_ris = self._map__resource_type__resource_instances

        resource_instance_ids = map_rt_ris.get(resource_type_id, tuple())
        result = self._resolve_resources(resource_instance_ids)

        return result

    def _resolve_content_type_view_types(self, content_type_id):
        map_ct_vts = self._map__content_type__view_types

        view_type_ids = map_ct_vts.get(content_type_id)
        if view_type_ids:
            result = self._resolve_resources(view_type_ids)
        else:
            result = tuple()

        return result

    def _resolve_view_type_content_instances(self, view_type_id):
        map_vt_cis = self._map__view_type__content_instances

        content_instance_ids = map_vt_cis.get(view_type_id)
        if content_instance_ids:
            result = self._resolve_resources(content_instance_ids)
        else:
            result = tuple()

        return result

    def _resolve_attribute_type_filter_types(self, attribute_type_id):
        map_at_fts = self._map__attribute_type__filter_types

        filter_type_ids = map_at_fts.get(attribute_type_id)
        if filter_type_ids:
            result = self._resolve_resources(filter_type_ids)
        else:
            result = tuple()

        return result

    def _resolve_attribute_instance_content_instance(self, attribute_instance_id):
        map_ai_ci = self._map__attribute_instance__content_instance

        try:
            result = map_ai_ci[attribute_instance_id]
        except KeyError:
            result = None
        else:
            result = self._resources.get(result)

        return result

    def _resolve_filter_instance_view_instance(self, filter_instance_id):
        map_fi_vi = self._map__filter_instance__view_instance

        try:
            result = map_fi_vi[filter_instance_id]
        except KeyError:
            result = None
        else:
            result = self._resources.get(result)

        return result

    def _resolve_content_instance_attribute_instance_from_attribute_type(
            self, content_instance_id, attribute_type_id):
        """
        Attempts to find an `AttributeInstance` of type `attribute_type_id`
            associated with `content_instance` .
        """
        content_instance = self._resources[content_instance_id]
        content_inst_attr_ids = content_instance.attribute_ids

        map_rt_ris = self._map__resource_type__resource_instances
        attr_type_inst_ids = map_rt_ris[attribute_type_id]

        result = set(content_inst_attr_ids).intersection(attr_type_inst_ids)
        try:
            result = result.pop()
        except KeyError:
            result = None
        else:
            result = self._resources.get(result)

        return result

    def _resolve_view_result_view_instance(self, view_result_id):
        map_vr_vi = self._map__view_result__view_instance

        try:
            result = map_vr_vi[view_result_id]
        except KeyError:
            result = None
        else:
            result = self._resources.get(result)

        return result

    @staticmethod
    def _fix_map_key(map, key, items_container_type=None):
        """
        Helper function for ensuring a specific object instance is used
        as the key for a map entry.

        Model is intended to support unordered registration of `Resources`.
        There are cases where a dependent `Resource` will create an entry
        in a map because the dependency has not yet been registered. This
        function allows the dependency to insert its own object as the key.
        This is especially important when using a WeakKeyDictionary as the map.
        """
        try:
            value = map[key]
        except KeyError:
            if items_container_type:
                value = items_container_type()
            else:
                value = NO_VALUE
        else:
            del map[key]

        map[key] = value
