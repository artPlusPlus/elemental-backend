import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    SorterType
)


_LOG = logging.getLogger(__name__)


class SorterTypeModel(ResourceModelBase):
    __resource_cls__ = SorterType
    __resource_indexes__ = ()


    def register(self, core_model, resource):
        map_at_sts = self._map__attribute_type__sorter_types
        for attribute_type_id in sorter_type.attribute_type_ids:
            try:
                sorter_types = map_at_sts[attribute_type_id]
            except KeyError:
                sorter_types = weakref.WeakSet()
            sorter_types.add(sorter_type.id)

        # self._update_view_instance_content_instances()

        hook = sorter_type.attribute_type_ids_changed
        handler = self._handle_sorter_type_attribute_type_ids_changed
        hook.add_handler(handler)

        ref = type(sorter_type).attribute_types
        resolver = self._resolve_resources
        ref.add_resolver(sorter_type, resolver)

    def release(self, core_model, resource):
        map_at_sts = self._map__attribute_type__sorter_types
        for attribute_type_id in sorter_type.attribute_type_ids:
            try:
                map_at_sts[attribute_type_id].discard(sorter_type.id)
            except KeyError:
                pass

        # self._update_view_instance_content_instances()

        hook = sorter_type.attribute_type_ids_changed
        handler = self._handle_sorter_type_attribute_type_ids_changed
        hook.remove_handler(handler)

        ref = type(sorter_type).attribute_types
        ref.remove_resolver(sorter_type)

    def _handle_sorter_type_attribute_type_ids_changed(
            self, sender, event_data):
        original_value, current_value = event_data

        added_attr_type_ids = set(current_value).difference(current_value)
        removed_attr_type_ids = set(original_value).difference(current_value)

        map_at_sts = self._map__attribute_type__sorter_types
        for attr_type_id in removed_attr_type_ids:
            try:
                sorter_type_ids = map_at_sts[attr_type_id]
            except KeyError:
                continue
            else:
                sorter_type_ids.discard(sender.id)

        for attr_type_id in added_attr_type_ids:
            sorter_type_ids = map_at_sts.setdefault(attr_type_id,
                                                    weakref.WeakSet())
            sorter_type_ids.add(sender.id)

        map_rt_ri = self._map__resource_type__resource_instances
        map_si_vi = self._map__sorter_instance__view_instance
        for sorter_inst_id in map_rt_ri[sender.id]:
            view_inst_id = map_si_vi[sorter_inst_id]
            # self._update_view_instance_content_instances(view_inst_id)