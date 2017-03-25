import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    ViewInstance,
    ViewResult,
    FilterInstance
)
from ..errors import (
    ResourceNotRegisteredError
)


_LOG = logging.getLogger(__name__)


class ViewInstanceModel(ResourceModelBase):
    __resource_cls__ = ViewInstance
    __resource_indexes__ = (
        ResourceIndex(ViewResult, ViewInstance),
        ResourceIndex(FilterInstance, ViewInstance)
    )

    def register(self, core_model, resource):
        if not resource.type_id:
            msg = (
                'Failed to register resource "{0}": '
                'Invalid type id - "{1}"'
            )
            msg = msg.format(repr(resource), resource.type_id)

            _LOG.error(msg)
            raise ResourceNotRegisteredError(
                msg, resource_type=type(resource),
                resource_id=resource.id)

        idx_fi_vi = core_model.get_resource_index(FilterInstance, ViewInstance)
        for filter_instance_id in resource.filter_ids:
            idx_fi_vi.push_index_value(filter_instance_id, resource)

        map_vr_vi = self._map__view_result__view_instance
        map_vr_vi[resource.result_id] = resource.id

        hook = resource.filter_ids_changed
        handler = self._handle_view_instance_filter_ids_changed
        hook.add_handler(handler)

        hook = resource.sorter_ids_changed
        handler = self._handle_view_instance_sorter_ids_changed
        hook.add_handler(handler)

        hook = resource.result_id_changed
        handler = self._handle_view_instance_result_id_changed
        hook.add_handler(handler)

        ref = type(resource).filter_instances
        resolver = self._resolve_resources
        ref.add_resolver(resource, resolver)

        ref = type(resource).sorter_instances
        resolver = self._resolve_resources
        ref.add_resolver(resource, resolver)

        ref = type(resource).result
        resolver = self._resolve_resource
        ref.add_resolver(resource, resolver)

    def retrieve(self, core_model, resource_id, resource=None):
        return resource

    def release(self, core_model, resource):
        hook = resource.filter_ids_changed
        handler = self._handle_view_instance_filter_ids_changed
        hook.remove_handler(handler)

        hook = resource.sorter_ids_changed
        handler = self._handle_view_instance_sorter_ids_changed
        hook.remove_handler(handler)

        hook = resource.result_id_changed
        handler = self._handle_view_instance_result_id_changed
        hook.remove_handler(handler)

        ref = type(resource).filter_instances
        ref.remove_resolver(resource)

        ref = type(resource).sorter_instances
        ref.remove_resolver(resource)

        ref = type(resource).result
        ref.remove_resolver(resource)

    def _handle_view_instance_filter_ids_changed(
            self, sender, event_data):
        original_value, current_value = event_data

        idx_fi_vi = self._core_model.get_resource_index(FilterInstance, ViewInstance)

        for filter_instance_id in set(original_value).difference(current_value):
            idx_fi_vi.pop_index(filter_instance_id)

        for filter_instance_id in current_value:
            idx_fi_vi.push_index_value(filter_instance_id, sender)

        # self._update_view_instance_content_instances(sender.id)

    def _handle_view_instance_sorter_ids_changed(
            self, sender, event_data):
        pass

    def _handle_view_instance_result_id_changed(
            self, sender, event_data):
        original_value, current_value = event_data

        # self._update_view_instance_content_instances(sender.id)