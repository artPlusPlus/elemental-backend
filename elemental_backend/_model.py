import logging
import weakref
import collections
from functools import partial

from elemental_core.util import process_uuid_value

from .errors import (
    ResourceError,
    ResourceNotFoundError,
    ResourceNotRegisteredError,
    ResourceCollisionError,
    ResourceNotReleasedError
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
    FilterType,
    FilterInstance
)
from ._util import _resolve_attr_type


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

        self._resources = weakref.WeakKeyDictionary()
        self._map__resource_class__resources = {}  # Will contain weak refs.
        self._map__resource_type__resource_instances = weakref.WeakKeyDictionary()
        self._map__target_attr__source_attr = weakref.WeakKeyDictionary()
        self._map__attribute_type__content_type = weakref.WeakValueDictionary()
        self._map__attribute_type__filter_types = weakref.WeakKeyDictionary()
        self._map__attribute_instance__content_instance = weakref.WeakValueDictionary()
        self._map__view_type__content_instances = weakref.WeakKeyDictionary()
        self._map__view_instance__content_instances = weakref.WeakKeyDictionary()
        self._map__content_type__view_types = weakref.WeakValueDictionary()
        self._map__filter_instance__view_instance = weakref.WeakKeyDictionary()

        self._map__resource_type__registrar = {
            Resource: self._register_resource,
            ResourceType: self._register_resource_type,
            ResourceInstance: self._register_resource_instance,
            ContentType: self._register_content_type,
            ContentInstance: self._register_content_instance,
            AttributeType: self._register_attribute_type,
            AttributeInstance: self._register_attribute_instance,
            ViewType: self._register_view_type,
            ViewInstance: self._register_view_instance,
            FilterType: self._register_filter_type,
            FilterInstance: self._register_filter_instance
        }

        self._map__resource_type__deregistrar = {
            Resource: self._deregister_resource,
            ResourceType: self._deregister_resource_type,
            ResourceInstance: self._deregister_resource_instance,
            ContentType: self._deregister_content_type,
            ContentInstance: self._deregister_content_instance,
            AttributeType: self._deregister_attribute_type,
            AttributeInstance: self._deregister_attribute_instance,
            ViewType: self._deregister_view_type,
            ViewInstance: self._deregister_view_instance,
            FilterType: self._deregister_filter_type,
            FilterInstance: self._deregister_filter_instance
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
            type_resources = self._map__resource_class__resources[type(resource)]
        except KeyError:
            type_resources = weakref.WeakValueDictionary()
            self._map__resource_class__resources[type(resource)] = type_resources

        self._resources[resource.id] = resource
        type_resources[resource.id] = resource

        handler = (resource, self._handle_resource_id_changed)
        type(resource).id += handler

    def _deregister_resource(self, resource):
        try:
            type_resources = self._map__resource_class__resources[type(resource)]
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

        handler = (resource, self._handle_resource_id_changed)
        type(resource).id -= handler

    def _register_resource_type(self, resource_type):
        # When registering a ResourceType, the UUID instance owned by
        # resource_type should be used as the key. However, it is possible
        # for a ResourceInstance to be registered prior to the ResourceType
        # instance.
        map_type_instances = self._map__resource_type__resource_instances

        try:
            instance_ids = map_type_instances[resource_type.id]
        except KeyError:
            instance_ids = weakref.WeakSet()

        # Here, the uuid object used as a key is explicitly set to be the
        # `ResourceType`'s `id` object.
        try:
            del map_type_instances[resource_type.id]
        except KeyError:
            pass
        finally:
            map_type_instances[resource_type.id] = instance_ids

        handler = (resource_type, self._handle_resource_type_name_changed)
        type(resource_type).name += handler

    def _deregister_resource_type(self, resource_type):
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

        handler = (resource_type, self._handle_resource_type_name_changed)
        type(resource_type).name -= handler

    def _register_resource_instance(self, resource_instance):
        map_type_instances = self._map__resource_type__resource_instances

        try:
            instance_ids = map_type_instances[resource_instance.type_id]
        except KeyError:
            instance_ids = weakref.WeakSet()
            map_type_instances[resource_instance.type_id] = instance_ids

        instance_ids.add(resource_instance.id)

        handler = (resource_instance,
                   self._handle_resource_instance_type_id_changed)
        type(resource_instance).type_id += handler

    def _deregister_resource_instance(self, resource_instance):
        map_type_instances = self._map__resource_type__resource_instances

        try:
            instance_ids = map_type_instances[resource_instance.type_id]
        except KeyError:
            return

        instance_ids.remove(resource_instance.id)

        handler = (resource_instance,
                   self._handle_resource_instance_type_id_changed)
        type(resource_instance).type_id -= handler

    def _register_content_type(self, content_type):
        map_at_ct = self._map__attribute_type__content_type
        for attribute_type_id in content_type.attribute_type_ids:
            map_at_ct[attribute_type_id] = content_type.id

        handler = (content_type,
                   self._handle_content_type_base_ids_changed)
        type(content_type).base_ids += handler

        handler = (content_type,
                   self._handle_content_type_attribute_type_ids_changed)
        type(content_type).attribute_type_ids += handler

    def _deregister_content_type(self, content_type):
        map_at_ct = self._map__attribute_type__content_type
        for attribute_type_id in content_type.attribute_type_ids:
            del map_at_ct[attribute_type_id]

        handler = (content_type,
                   self._handle_content_type_base_ids_changed)
        type(content_type).base_ids -= handler

        handler = (content_type,
                   self._handle_content_type_attribute_type_ids_changed)
        type(content_type).attribute_type_ids -= handler

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

        handler = (content_instance,
                   self._handle_content_instance_attribute_ids_changed)
        type(content_instance).attribute_ids += handler

    def _deregister_content_instance(self, content_instance):
        map_ai_ci = self._map__attribute_instance__content_instance
        for attribute_id in content_instance.attribute_ids:
            try:
                del map_ai_ci[attribute_id]
            except KeyError:
                pass

        handler = (content_instance,
                   self._handle_content_instance_attribute_ids_changed)
        type(content_instance).attribute_ids -= handler

    def _register_attribute_type(self, attribute_type):
        map_at_ct = self._map__attribute_type__content_type
        try:
            content_type_id = map_at_ct[attribute_type.id]
        except KeyError:
            pass
        else:
            del map_at_ct[attribute_type.id]
            map_at_ct[attribute_type.id] = content_type_id

        map_at_fts = self._map__attribute_type__filter_types
        try:
            filter_type_ids = map_at_fts[attribute_type.id]
        except KeyError:
            pass
        else:
            del map_at_fts[attribute_type.id]
            map_at_fts[attribute_type.id] = filter_type_ids

        handler = (attribute_type,
                   self._handle_attribute_type_default_value_changed)
        type(attribute_type).default_value += handler

        handler = (attribute_type,
                   self._handle_attribute_type_kind_id_changed)
        type(attribute_type).kind_id += handler

        handler = (attribute_type,
                   self._handle_attribute_type_kind_properties_changed)
        type(attribute_type).kind_properties += handler

    def _deregister_attribute_type(self, attribute_type):
        handler = (attribute_type,
                   self._handle_attribute_type_default_value_changed)
        type(attribute_type).default_value -= handler

        handler = (attribute_type,
                   self._handle_attribute_type_kind_id_changed)
        type(attribute_type).kind_id -= handler

        handler = (attribute_type,
                   self._handle_attribute_type_kind_properties_changed)
        type(attribute_type).kind_properties -= handler

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

        map_ai_ci = self._map__attribute_instance__content_instance
        try:
            content_instance_id = map_ai_ci[attribute_instance.id]
        except KeyError:
            pass
        else:
            del map_ai_ci[attribute_instance.id]
            map_ai_ci[attribute_instance.id] = content_instance_id

        handler = (attribute_instance,
                   self._handle_attribute_instance_value_changed)
        type(attribute_instance).value += handler

        handler = (attribute_instance,
                   self._handle_attribute_instance_source_id_changed)
        type(attribute_instance).source_id += handler

    def _deregister_attribute_instance(self, attribute_instance):
        map_ai_ci = self._map__attribute_instance__content_instance
        try:
            del map_ai_ci[attribute_instance.id]
        except KeyError:
            pass

        handler = (attribute_instance,
                   self._handle_attribute_instance_value_changed)
        type(attribute_instance).value -= handler

        handler = (attribute_instance,
                   self._handle_attribute_instance_source_id_changed)
        type(attribute_instance).source_id -= handler

    def _register_view_type(self, view_type):
        map_vt_cis = self._map__view_type__content_instances
        if view_type.id not in map_vt_cis:
            map_vt_cis[view_type.id] = weakref.WeakSet()

        map_ct_vt = self._map__content_type__view_types
        for content_type_id in view_type.content_type_ids:
            try:
                view_types = map_ct_vt[content_type_id]
            except KeyError:
                view_types = weakref.WeakSet()
            view_types.add(view_type.id)

        self._update_view_type_content_instances(
            view_type, view_type.content_type_ids, set())

        handler = (view_type,
                   self._handle_view_type_content_type_ids_changed)
        type(view_type).content_type_ids += handler

        handler = (view_type,
                   self._handle_view_type_filter_type_ids_changed)
        type(view_type).filter_type_ids += handler

    def _deregister_view_type(self, view_type):
        del self._map__view_type__content_instances[view_type.id]

        handler = (view_type,
                   self._handle_view_type_content_type_ids_changed)
        type(view_type).content_type_ids -= handler

        handler = (view_type,
                   self._handle_view_type_filter_type_ids_changed)
        type(view_type).filter_type_ids -= handler

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

        map_vi_cis = self._map__view_instance__content_instances
        try:
            content_instance_ids = map_vi_cis[view_instance.id]
        except KeyError:
            content_instance_ids = weakref.WeakSet()
        else:
            del map_vi_cis[view_instance.id]
        map_vi_cis[view_instance.id] = content_instance_ids

        handler = (view_instance,
                   self._handle_view_instance_filter_ids_changed)
        type(view_instance).filter_ids += handler

    def _deregister_view_instance(self, view_instance):
        map_vi_cis = self._map__view_instance__content_instances
        try:
            del map_vi_cis[view_instance.id]
        except KeyError:
            msg = (
                'ViewInstance "{0}" not found in '
                'ViewInstance:ContentInstances map during deregistration.'
                'This is unexpected and could be a symptom of a problematic'
                'model.'
            )
            msg = msg.format(view_instance.id)

            _LOG.warn(msg)

        handler = (view_instance,
                   self._handle_view_instance_filter_ids_changed)
        type(view_instance).filter_ids -= handler

    def _register_filter_type(self, filter_type):
        map_at_fts = self._map__attribute_type__filter_types
        for attribute_type_id in filter_type.attribute_type_ids:
            try:
                filter_types = map_at_fts[attribute_type_id]
            except KeyError:
                filter_types = weakref.WeakSet()
            filter_types.add(filter_type)

        handler = (filter_type,
                   self._handle_filter_type_attribute_type_ids_changed)
        type(filter_type).attribute_type_ids += handler

    def _deregister_filter_type(self, filter_type):
        handler = (filter_type,
                   self._handle_filter_type_attribute_type_ids_changed)
        type(filter_type).attribute_type_ids -= handler

    def _register_filter_instance(self, filter_instance):
        handler = (filter_instance,
                   self._handler_filter_instance_kind_params_changed)
        type(filter_instance).kind_params += handler

    def _deregister_filter_instance(self, filter_instance):
        handler = (filter_instance,
                   self._handler_filter_instance_kind_params_changed)
        type(filter_instance).kind_params -= handler

    def _handle_resource_id_changed(
            self, resource, original_value, current_value):
        msg = 'Mutable Ids are not supported.'

        _LOG.error(msg)
        raise ResourceError(msg, resource_type=type(resource),
                            resource_id=resource.id)

    def _handle_resource_type_name_changed(
            self, resource_type, original_value, current_value):
        pass

    def _handle_resource_instance_type_id_changed(
            self, resource_instance, original_value, current_value):
        map_rt_ris = self._map__resource_type__resource_instances
        try:
            map_rt_ris[original_value].discard(resource_instance.id)
        except KeyError:
            pass

        try:
            resource_instance_ids = map_rt_ris[current_value]
        except KeyError:
            resource_instance_ids = weakref.WeakSet()
            map_rt_ris[current_value] = resource_instance_ids
        resource_instance_ids.add(resource_instance.id)

    def _handle_content_type_base_ids_changed(
            self, content_type, original_value, current_value):
        pass

    def _handle_content_type_attribute_type_ids_changed(
            self, content_type, original_value, current_value):

        map_at_ct = self._map__attribute_type__content_type

        for attribute_type_id in original_value:
            del map_at_ct[attribute_type_id]

        for attribute_type_id in current_value:
            map_at_ct[attribute_type_id] = content_type.id

    def _handle_content_instance_attribute_ids_changed(
            self, content_instance, original_value, current_value):
        pass

    def _handle_attribute_type_default_value_changed(
            self, attribute_type, original_value, current_value):
        pass

    def _handle_attribute_type_kind_id_changed(
            self, attribute_type, original_value, current_value):
        pass

    def _handle_attribute_type_kind_properties_changed(
            self, attribute_type, original_value, current_value):
        pass

    def _handle_attribute_instance_value_changed(
            self, attribute_instance, original_value, current_value):
        map_at_fts = self._map__attribute_type__filter_types

        filter_type_ids = map_at_fts.get(attribute_instance.type_id)
        if not filter_type_ids:
            return

        map_ai_ci = self._map__attribute_instance__content_instance
        content_instance = self._resources[map_ai_ci[attribute_instance.id]]
        content_type_id = content_instance.type_id

        map_ct_vts = self._map__content_type__view_types
        view_type_ids = map_ct_vts[content_type_id]

        map_rt_ris = self._map__resource_type__resource_instances
        for view_type_id in view_type_ids:
            view_instance_ids = map_rt_ris[view_type_id]
            for view_instance_id in view_instance_ids:
                self._update_view_instance_content_instances(
                    view_instance_id, content_instance_ids=content_instance.id)

    def _handle_attribute_instance_source_id_changed(
            self, attribute_instance, original_value, current_value):
        map_sa_tas = self._map__source_attr__target_attrs
        try:
            map_sa_tas[original_value].discard(attribute_instance.id)
        except KeyError:
            pass

        try:
            target_ids = map_sa_tas[current_value]
        except KeyError:
            target_ids = weakref.WeakSet()
            map_sa_tas[current_value] = target_ids
        target_ids.add(attribute_instance.id)

    def _handle_view_type_content_type_ids_changed(
            self, view_type, original_value, current_value):
        added = current_value.difference(original_value)
        removed = original_value.difference(current_value)
        self._update_view_type_content_instances(view_type, added, removed)

        map_rt_ri = self._map__resource_type__resource_instances
        for view_inst_id in map_rt_ri[view_type.id]:
            self._update_view_instance_content_instances(view_inst_id)

    def _handle_view_type_filter_type_ids_changed(
            self, view_type, original_value, current_value):
        map_rt_ri = self._map__resource_type__resource_instances
        for view_inst_id in map_rt_ri[view_type.id]:
            self._update_view_instance_content_instances(view_inst_id)

    def _handle_view_instance_filter_ids_changed(
            self, view_instance, original_value, current_value):

        map_fi_vi = self._map__filter_instance__view_instance

        for filter_instance_id in set(original_value).difference(current_value):
            map_fi_vi[filter_instance_id] = None

        for filter_instance_id in current_value:
            map_fi_vi[filter_instance_id] = view_instance.id

        self._update_view_instance_content_instances(view_instance.id)

    def _handle_filter_type_attribute_type_ids_changed(
            self, filter_type, original_value, current_value):
        map_rt_ri = self._map__resource_type__resource_instances
        map_fi_vi = self._map__filter_instance__view_instance
        for filter_inst_id in map_rt_ri[filter_type.id]:
            view_inst_id = map_fi_vi[filter_inst_id]
            self._update_view_instance_content_instances(view_inst_id)

    def _handler_filter_instance_kind_params_changed(
            self, filter_instance, original_value, current_value):
        map_fi_vi = self._map__filter_instance__view_instance
        view_inst_id = map_fi_vi[filter_instance.id]
        self._update_view_instance_content_instances(view_inst_id)

    def _update_view_type_content_instances(
            self, view_type, add_content_type_ids, remove_content_type_ids):
        map_rt_ri = self._map__resource_type__resource_instances
        map_vt_cis = self._map__view_type__content_instances
        content_inst_ids = map_vt_cis[view_type.id]

        for type_id in remove_content_type_ids:
            content_inst_ids.difference_update(map_rt_ri[type_id])

        for type_id in add_content_type_ids:
            content_inst_ids.update(map_rt_ri[type_id])

    def _update_view_instance_content_instances(
            self, view_instance_id, content_instance_ids=None, filter_data=None):
        view_instance = self._resources[view_instance_id]

        if not filter_data:
            filter_data = self._resolve_view_instance_filter_data(view_instance)

        if not content_instance_ids:
            map_vt_cis = self._map__view_type__content_instances
            content_instance_ids = map_vt_cis[view_instance.type_id]
        elif not isinstance(content_instance_ids, collections.Iterable):
            content_instance_ids = [content_instance_ids]

        map_vi_cis = self._map__view_instance__content_instances
        view_inst_content_inst_ids = map_vi_cis[view_instance.id]

        for content_inst_id in content_instance_ids:
            content_inst = self._resources[content_inst_id]
            if self._apply_filter(content_inst, filter_data):
                view_inst_content_inst_ids.add(content_inst_id)
            else:
                view_inst_content_inst_ids.discard(content_inst_id)

    def _apply_filter(self, content_instance, filter_data):
        result = True

        for filter_type, filter_inst in filter_data:
            attr_inst_id = None
            for attr_type_id in filter_type.attribute_type_ids:
                attr_inst_id = self._resolve_attribute_instance_id(
                    content_instance, attr_type_id)
                if attr_inst_id is not None:
                    break

            attr_inst = self._resources[attr_inst_id]
            attr_type = self._resources[attr_type_id]
            attr_kind = attr_type.kind
            attr_value = attr_inst.value

            result = attr_kind.filter(attr_value, **filter_inst.kind_params)
            if not result:
                break

        return result

    def _resolve_view_instance_filter_data(self, view_instance):
        """
        Resolves `view_instance`'s filter ids with `FilterInstance` objects.
        """
        result = [self._resources[f_id] for f_id in view_instance.filter_ids]
        result = [(self._resources[f.type_id], f) for f in result]

        return result

    def _resolve_attribute_instance_id(
            self, content_instance, attribute_type_id):
        """
        Attempts to find an `AttributeInstance` associated with
            `content_instance` of type `attribute_type_id`.
        """
        map_rt_ris = self._map__resource_type__resource_instances
        attr_type_inst_ids = map_rt_ris[attribute_type_id]
        content_inst_attr_ids = content_instance.attribute_ids

        result = content_inst_attr_ids.intersection(attr_type_inst_ids)
        try:
            result = result.pop()
        except KeyError:
            result = None

        return result
