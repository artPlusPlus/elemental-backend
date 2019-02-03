import logging

from elemental_core import NO_VALUE

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    AttributeInstance,
    ContentInstance
)


_LOG = logging.getLogger(__name__)


class AttributeInstanceModel(ResourceModelBase):
    __resource_cls__ = AttributeInstance
    __resource_indexes__ = (
        ResourceIndex(AttributeInstance, ContentInstance, indexed_capacity=1)
    )

    def register(self, resource):
        idx_ai_ci = self._get_index(AttributeInstance, ContentInstance)
        idx_ai_ci.push_index(resource)

        raise RuntimeError('TODO: Add ViewInstanceModel hook')
        # self._update_view_instance_content_instances()

        hook = resource.value_changed
        handler = self._handle_attribute_instance_value_changed
        hook.add_handler(handler)

        hook = resource.source_id_changed
        handler = self._handle_attribute_instance_source_id_changed
        hook.add_handler(handler)

        ref = type(resource).source
        resolver = self._get_resource
        ref.add_resolver(resource, resolver)

        ref = type(resource).content_instance
        resolver = self._resolve_attribute_instance_content_instance
        ref.add_resolver(resource, resolver)

    def retrieve(self, resource_id, resource=None):
        return resource

    def release(self, resource):
        idx_ai_ci = self._get_index(AttributeInstance, ContentInstance)
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

    def _handle_attribute_instance_value_changed(self):
        pass

    def _handle_attribute_instance_source_id_changed(self):
        pass

    def _resolve_attribute_instance_content_instance(self, attribute_instance_id):
        idx_ai_ci = self._get_index(AttributeInstance, ContentInstance)

        try:
            result = idx_ai_ci.get_indexed_value(attribute_instance_id)[0]
        except IndexError:
            result = NO_VALUE
        else:
            result = self._get_resource(result)

        return result
