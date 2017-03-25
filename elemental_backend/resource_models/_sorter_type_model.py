import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    SorterType,
    AttributeType
)


_LOG = logging.getLogger(__name__)


class SorterTypeModel(ResourceModelBase):
    __resource_cls__ = SorterType
    __resource_indexes__ = (
        ResourceIndex(AttributeType, SorterType)
    )

    def register(self, core_model, resource):
        idx_at_sts = core_model.get_resource_index(AttributeType, SorterType)

        for attribute_type_id in resource.attribute_type_ids:
            idx_at_sts.push_index_value(attribute_type_id, resource)

        # self._update_view_instance_content_instances()

        hook = resource.attribute_type_ids_changed
        handler = self._handle_sorter_type_attribute_type_ids_changed
        hook.add_handler(handler)

        ref = type(resource).attribute_types
        resolver = self._resolve_resources
        ref.add_resolver(resource, resolver)

    def retrieve(self, core_model, resource_id, resource=None):
        return resource

    def release(self, core_model, resource):
        idx_at_sts = core_model.get_resource_index(AttributeType, SorterType)

        for attribute_type_id in resource.attribute_type_ids:
            idx_at_sts.pop_index_value(attribute_type_id, resource)

        # self._update_view_instance_content_instances()

        hook = resource.attribute_type_ids_changed
        handler = self._handle_sorter_type_attribute_type_ids_changed
        hook.remove_handler(handler)

        ref = type(resource).attribute_types
        ref.remove_resolver(resource)

    def _handle_sorter_type_attribute_type_ids_changed(self, sender, event_data):
        original_value, current_value = event_data

        added_attr_type_ids = set(current_value).difference(current_value)
        removed_attr_type_ids = set(original_value).difference(current_value)

        idx_at_sts = self._core_model.get_resource_index(AttributeType, SorterType)

        for attribute_type_id in removed_attr_type_ids:
            idx_at_sts.pop_index_value(attribute_type_id, sender)

        for attribute_type_id in added_attr_type_ids:
            idx_at_sts.push_index_value(attribute_type_id, sender)

        map_rt_ri = self._map__resource_type__resource_instances
        map_si_vi = self._map__sorter_instance__view_instance
        for sorter_inst_id in map_rt_ri[sender.id]:
            view_inst_id = map_si_vi[sorter_inst_id]
            # self._update_view_instance_content_instances(view_inst_id)