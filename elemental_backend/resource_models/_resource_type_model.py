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

    def register(self, core_model, resource):
        idx_rt_ris = core_model.get_resource_index(ResourceType, ResourceInstance)
        idx_rt_ris.create_index(resource)

        hook = resource.name_changed
        handler = self._handle_resource_type_name_changed
        hook.add_handler(handler)

        ref = type(resource).resource_instances
        resolver = self._resolve_resource_type_resource_instances
        ref.add_resolver(resource, resolver)

    def retrieve(self, core_model, resource_id, resource=None):
        return resource

    def release(self, core_model, resource):
        idx_rt_ris = core_model.get_resource_index(ResourceType, ResourceInstance)

        try:
            idx_rt_ris.pop_index(resource)
        except KeyError:
            msg = (
                'ResourceType "{0}" not found in '
                'ResourceType:ResourceInstances map during deregistration.'
                'This is unexpected and could be a symptom of a problematic'
                'model.'
            )
            msg = msg.format(resource.id)

            _LOG.warning(msg)

        hook = resource.name_changed
        handler = self._handle_resource_type_name_changed
        hook.remove_handler(handler)

        ref = type(resource).resource_instances
        ref.remove_resolver(resource)

    def _handle_resource_type_name_changed(self, sender, data):
        pass

    def _resolve_resource_type_resource_instances(self, resource_type_id):
        idx_rt_ris = self._core_model.get_resource_index(ResourceType, ResourceInstance)
        result = self._resolve_resources(idx_rt_ris.iter_index(resource_type_id))

        return result
