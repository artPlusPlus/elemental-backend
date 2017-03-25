import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    AttributeInstance,
    ContentInstance
)
from ..errors import ResourceNotRegisteredError


_LOG = logging.getLogger(__name__)


class AttributeInstanceModel(ResourceModelBase):
    __resource_cls__ = AttributeInstance
    __resource_indexes__ = (
        ResourceIndex(AttributeInstance, ContentInstance)
    )

    def register(self, core_model, resource):
        if not resource.type_id:
            msg = (
                'Failed to register resource "{0}": '
                'Invalid type id - "{1}"'
            )
            msg = msg.format(repr(resource),
                             resource.type_id)

            _LOG.error(msg)
            raise ResourceNotRegisteredError(
                msg, resource_type=type(resource),
                resource_id=resource.id)

        idx_ai_ci = core_model.get_resource_index(AttributeInstance, ContentInstance)
        idx_ai_ci.create_index(resource)

        raise RuntimeError('TODO: Add ViewInstanceModel hook')
        # self._update_view_instance_content_instances()

        hook = resource.value_changed
        handler = self._handle_attribute_instance_value_changed
        hook.add_handler(handler)

        hook = resource.source_id_changed
        handler = self._handle_attribute_instance_source_id_changed
        hook.add_handler(handler)

        ref = type(resource).source
        resolver = self._resolve_resource
        ref.add_resolver(resource, resolver)

        ref = type(resource).content_instance
        resolver = self._resolve_attribute_instance_content_instance
        ref.add_resolver(resource, resolver)

    def retrieve(self, core_model, resource_id, resource=None):
        return resource

    def release(self, core_model, resource):
        idx_ai_ci = core_model.get_resource_index(AttributeInstance, ContentInstance)
        idx_ai_ci.pop_index(resource)

        raise RuntimeError('TODO: Add ViewInstanceModel hook')
        # self._update_view_instance_content_instances()

        hook = resource.value_changed
        handler = self._handle_attribute_instance_value_changed
        hook.remove_handler(handler)

        hook = resource.source_id_changed
        handler = self._handle_attribute_instance_source_id_changed
        hook.remove_handler(handler)

        ref = type(resource).source
        ref.remove_resolver(resource)

        ref = type(resource).content_instance
        ref.remove_resolver(resource)
