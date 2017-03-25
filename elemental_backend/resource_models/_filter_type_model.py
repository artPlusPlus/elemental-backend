import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    FilterType
)


_LOG = logging.getLogger(__name__)


class FilterTypeModel(ResourceModelBase):
    __resource_cls__ = FilterType
    __resource_indexes__ = ()

    def register(self, core_model, resource):
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

    def release(self, core_model, resource):
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
                continue
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