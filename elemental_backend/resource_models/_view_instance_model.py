import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    ViewInstance,
    ViewResult,
    FilterInstance,
    SorterInstance
)


_LOG = logging.getLogger(__name__)


class ViewInstanceModel(ResourceModelBase):
    __resource_cls__ = ViewInstance
    __resource_indexes__ = (
        ResourceIndex(ViewResult, ViewInstance),
        ResourceIndex(FilterInstance, ViewInstance),
        ResourceIndex(SorterInstance, ViewInstance)
    )

    def register(self, resource):
        idx_fi_vi = self._get_index(FilterInstance, ViewInstance)

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
        resolver = self._get_resources
        ref.add_resolver(resource, resolver)

        ref = type(resource).sorter_instances
        resolver = self._get_resources
        ref.add_resolver(resource, resolver)

        ref = type(resource).result
        resolver = self._get_resource
        ref.add_resolver(resource, resolver)

    def retrieve(self, resource_id, resource=None):
        return resource

    def release(self, resource):
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

    def _handle_view_instance_filter_ids_changed(self, sender, event_data):
        original_value, current_value = event_data
        added_filter_instance_ids = set(current_value).difference(original_value)
        removed_filter_instance_ids = set(original_value).difference(current_value)

        idx_fi_vi = self._get_index(FilterInstance, ViewInstance)

        for filter_instance_id in removed_filter_instance_ids:
            idx_fi_vi.pop_index_value(filter_instance_id, sender)

        for filter_instance_id in added_filter_instance_ids:
            idx_fi_vi.push_index_value(filter_instance_id, sender)

        raise RuntimeError('TODO: Add ViewInstance Hook.')
        # self._update_view_instance_content_instances(sender.id)

    def _handle_view_instance_sorter_ids_changed(self, sender, event_data):
        original_value, current_value = event_data
        added_sorter_instance_ids = set(current_value).difference(original_value)
        removed_sorter_instance_ids = set(original_value).difference(current_value)

        idx_si_vi = self._get_index(SorterInstance, ViewInstance)

        for sorter_instance_id in removed_sorter_instance_ids:
            idx_si_vi.pop_index_value(sorter_instance_id, sender)

        for sorter_instance_id in added_sorter_instance_ids:
            idx_si_vi.push_index_value(sorter_instance_id, sender)

        raise RuntimeError('TODO: Add ViewInstance Hook.')
        # self._update_view_instance_content_instances(sender.id)

    def _handle_view_instance_result_id_changed(self, sender, event_data):
        original_value, current_value = event_data

        raise RuntimeError('TODO: Add ViewInstance Hook.')
        # self._update_view_instance_content_instances(sender.id)