import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    ResourceType,
    ResourceInstance
)
from ..errors import (
    ResourceNotRegisteredError
)


_LOG = logging.getLogger(__name__)


class ResourceInstanceModel(ResourceModelBase):
    __resource_cls__ = ResourceInstance
    __resource_indexes__ = (
        ResourceIndex(ResourceType, ResourceInstance),
    )

    def register(self, resource):
        idx_rt_ris = self._get_index(ResourceType, ResourceInstance)
        idx_rt_ris.push_index_value(resource.type_id, resource)

        hook = resource.type_id_changed
        handler = self._handle_resource_instance_type_id_changed
        hook.add_handler(handler)

        ref = type(resource).type
        resolver = self._get_resource
        ref.add_resolver(resource, resolver)

    def retrieve(self, resource_id, resource=None):
        return resource

    def release(self, resource):
        idx_rt_ris = self._get_index(ResourceType, ResourceInstance)
        idx_rt_ris.pop_index_value(resource.type_id, resource)

        hook = resource.type_id_changed
        handler = self._handle_resource_instance_type_id_changed
        hook.remove_handler(handler)

        ref = type(resource).type
        ref.remove_resolver(resource)

    def _handle_resource_instance_type_id_changed(self, sender, data):
        original_value, current_value = data

        idx_rt_ris = self._get_index(ResourceType, ResourceInstance)
        idx_rt_ris.move_index_value(sender.id, original_value, current_value)
