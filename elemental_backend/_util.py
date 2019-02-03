import logging
from collections import deque

from elemental_core.util import (
    process_elemental_class_value,
    process_data_format_value
)


_LOG = logging.getLogger(__name__)


def process_serializer_key(resource_type, data_format):
    """
    Computes a hashable value based on a `Resource` type and data format.

    Args:
        resource_type (str or Resource): A `Resource` subclass.
        data_format (str): A valid data format label.

    Returns:
        Tuple(`Resource`, str) if successful, None otherwise.
    """
    resource_type = process_elemental_class_value(resource_type)
    data_format = process_data_format_value(data_format)

    if resource_type and data_format:
        return resource_type, data_format
    return None


def process_deserializer_key(resource_type, data_format):
    """
    Computes a hashable value based on a `Resource` type and data format.

    Args:
        resource_type (str or Resource): A `Resource` subclass.
        data_format (str): A valid data format label.

    Returns:
        Tuple(`Resource`, str) if successful, None otherwise.
    """
    resource_type = process_elemental_class_value(resource_type)
    data_format = process_data_format_value(data_format)

    if resource_type and data_format:
        return resource_type, data_format

    return None


def process_handler_key(event, action, resource_type):
    """
    Computes a hashable value based on a `ControllerEvent`, `Action`,
        and `Resource` type.

    Args:
        event (ControllerEvents): A `ControllerEvents` value.
        action (Actions): A `Actions` value.
        resource_type (str or Resource): A `Resource` subclass.

    Returns:
        Tuple(ControllerEvent, Action, Resource) if successful, None otherwise.
    """
    resource_type = process_elemental_class_value(resource_type)

    if event:
        return event, action, resource_type

    return None


def iter_subclasses(base_class):
    classes = deque()
    classes.append(base_class)

    while classes:
        cls = classes.popleft()
        classes.extend(cls.__subclassess__())
        if cls is base_class:
            continue
        yield cls


# def resolve_resource_type(resource_inst_proxy, model_resources_proxy):
#     """
#     Used internally to allow `ResourceInstances` to resolve their `ResourceType`.
#
#     Args:
#         resource_inst_proxy (weakref.proxy): proxy to a ResourceInstance object.
#         model_resources_proxy (weakref.proxy): proxy to the _resources map of
#             a Model instance.
#
#     Returns:
#         `ResourceType` instance if proxies are alive and a `ResourceType`
#         instance with an id matching the value of the `ResourceInstance`
#         object's `type_id` has been registered with the same `Model` instance.
#     """
#     result = None
#
#     if not resource_inst_proxy:
#         msg = (
#             'Failed to resolve ResourceType: '
#             'AttributeInstance reference is dead.'
#         )
#         _LOG.warn(msg)
#
#         return result
#
#     if not model_resources_proxy:
#         msg = (
#             'Failed to resolve ResourceType: '
#             'Model._resources reference is dead.'
#         )
#         _LOG.warn(msg)
#
#         return result
#
#     type_id = resource_inst_proxy.type_id
#     result = model_resources_proxy.get(type_id)
#
#     if result:
#         msg = 'Resolved ResourceType: "{0}"'
#         msg = msg.format(result)
#     else:
#         msg = 'Failed to resolve ResourceType "{0}"'
#         msg = msg.format(type_id)
#     _LOG.debug(msg)
#
#     return result


# def resolve_view_instance_content_instances(
#         view_inst_proxy, model_map__view_instance__content_instances_proxy):
#     """
#     Used internally to allow a `ViewInstance` to resolve its `ContentInstance` collection.
#
#     Args:
#         view_inst_proxy (weakref.proxy): proxy to a ``ViewInstance`` instance.
#         model_map__view_instance__content_instances_proxy (weakref.proxy): proxy
#             to the `_map__view_instance__content_instances` map of a Model
#             instance.
#
#     Returns:
#         `uuid` collection if proxies are alive and an `
#     """
#     result = None
#
#     if not view_inst_proxy:
#         msg = (
#             'Failed to resolve ContentInstances: '
#             'ViewInstance reference is dead.'
#         )
#         _LOG.warn(msg)
#
#         return result
#
#     if not model_map__view_instance__content_instances_proxy:
#         msg = (
#             'Failed to resolve ContentInstances: '
#             'ViewInstance: ContentInstances map reference is dead.'
#         )
#         _LOG.warn(msg)
#
#         return result
#
#     view_inst_id = view_inst_proxy.id
#     map_vi_cis = model_map__view_instance__content_instances_proxy
#     try:
#         result = map_vi_cis[view_inst_id]
#     except KeyError:
#         pass
#     else:
#         result = result.copy()
#
#     if result:
#         msg = 'Resolved ContentInstances'
#     else:
#         msg = 'Failed to resolve ContentInstances'
#     _LOG.debug(msg)
#
#     return result


# def resolve_attribute_instance_source(
#         target_attribute_instance_proxy, model_resources_proxy):
#     """
#     Used internally to allow an `AttributeInstance` to resolve a source
#         `AttributeInstance`.
#
#     Args:
#         target_attribute_instance_proxy (weakref.proxy): proxy to an
#             `AttributeInstance` that pulls its value from another
#             `AttributeInstance`.
#         model_resources_proxy: proxy to a mapping of all resources
#             managed by a `Model`.
#
#     Returns:
#         None if `target_attribute_instance` has no value for a `source_id` or
#         a weakref.proxy referencing an `AttributeInstance`.
#     """
#     result = None
#
#     if not target_attribute_instance_proxy:
#         msg = (
#             'Failed to resolve AttributeInstance source: '
#             'target AttributeInstance reference is dead.'
#         )
#         _LOG.warn(msg)
#
#         return result
#
#     if not model_resources_proxy:
#         msg = (
#             'Failed to AttributeInstance source: '
#             'Model._resources reference is dead.'
#         )
#         _LOG.warn(msg)
#
#         return result
#
#     source_id = target_attribute_instance_proxy.source_id
#     if source_id:
#         result = model_resources_proxy.get(source_id)
#
#         if result:
#             msg = 'Resolved AttributeInstance source: "{0}"'
#             msg = msg.format(result)
#         else:
#             msg = 'Failed to resolve AttributeInstance "{0}"'
#             msg = msg.format(source_id)
#         _LOG.debug(msg)
#
#     return result


class _Dict(dict):
    """
    Weak referenceable dict: https://docs.python.org/3/library/weakref.html

    Used by a `Model` to allow for resolving of an `AttributeInstance`'s
    `AttributeType`.

    See Also:
        Model._register_attribute_instance
    """
    pass
