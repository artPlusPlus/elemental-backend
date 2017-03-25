import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    ResourceType,
    ResourceInstance
)


_LOG = logging.getLogger(__name__)


class ResourceTypeModel(ResourceModelBase):
    __resource_cls__ = ResourceType
    __resource_indexes__ = (
        ResourceIndex(ResourceType, ResourceInstance),
    )

    def register(self, resource):
        idx_rt_ris = self._get_index(ResourceType, ResourceInstance)
        idx_rt_ris.create_index(resource)

        hook = resource.name_changed
        handler = self._handle_resource_type_name_changed
        hook.add_handler(handler)

        ref = type(resource).resource_instances
        resolver = self._resolve_resource_type_resource_instances
        ref.add_resolver(resource, resolver)

    def retrieve(self, resource_id, resource=None):
        return resource

    def release(self, resource):
        idx_rt_ris = self._get_index(ResourceType, ResourceInstance)
        idx_rt_ris.pop_index(resource)

        hook = resource.name_changed
        handler = self._handle_resource_type_name_changed
        hook.remove_handler(handler)

        ref = type(resource).resource_instances
        ref.remove_resolver(resource)

    def _handle_resource_type_name_changed(self, sender, data):
        pass

    def _resolve_resource_type_resource_instances(self, resource_type_id):
        idx_rt_ris = self._get_index(ResourceType, ResourceInstance)

        result = idx_rt_ris.iter_index_values(resource_type_id)
        result = self._get_resources(result)

        return result
