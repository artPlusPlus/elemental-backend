from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    AttributeType,
    FilterType,
    SorterType
)


class AttributeTypeModel(ResourceModelBase):
    __resource_cls__ = AttributeType
    __resource_indexes__ = (
        ResourceIndex(AttributeType, FilterType),
        ResourceIndex(AttributeType, SorterType)
    )

    def register(self, core_model, resource):
        idx_at_fts = core_model.get_resource_index(AttributeType, FilterType)
        idx_at_fts.create_index(resource)

        idx_at_sts = core_model.get_resource_index(AttributeType, SorterType)
        idx_at_sts.create_index(resource)

        raise RuntimeError('TODO: Add ViewInstanceModel hook')
        # self._update_view_instance_content_instances()

        hook = resource.default_value_changed
        handler = self._handle_attribute_type_default_value_changed
        hook.add_handler(handler)

        hook = resource.kind_id_changed
        handler = self._handle_attribute_type_kind_id_changed
        hook.add_handler(handler)

        hook = resource.kind_properties_changed
        handler = self._handle_attribute_type_kind_properties_changed
        hook.add_handler(handler)

        ref = type(resource).filter_types
        resolver = self._resolve_attribute_type_filter_types
        ref.add_resolver(resource, resolver)

        ref = type(resource).sorter_types
        resolver = self._resolve_attribute_type_sorter_types
        ref.add_resolver(resource, resolver)

    def retrieve(self, core_model, resource_id, resource=None):
        return resource

    def release(self, core_model, resource):
        idx_at_fts = core_model.get_resource_index(AttributeType, FilterType)
        idx_at_fts.pop_index(resource)

        idx_at_sts = core_model.get_resource_index(AttributeType, SorterType)
        idx_at_sts.pop_index(resource)

        raise RuntimeError('TODO: Add ViewInstanceModel hook')
        # self._update_view_instance_content_instances()

        hook = resource.default_value_changed
        handler = self._handle_attribute_type_default_value_changed
        hook.remove_handler(handler)

        hook = resource.kind_id_changed
        handler = self._handle_attribute_type_kind_id_changed
        hook.remove_handler(handler)

        hook = resource.kind_properties_changed
        handler = self._handle_attribute_type_kind_properties_changed
        hook.remove_handler(handler)

        ref = type(resource).filter_types
        ref.remove_resolver(resource)

    def _handle_attribute_type_default_value_changed(
            self, sender, event_data):
        pass

    def _handle_attribute_type_kind_id_changed(
            self, sender, event_data):
        pass

    def _handle_attribute_type_kind_properties_changed(
            self, sender, event_data):
        pass

    def _resolve_attribute_type_filter_types(self, attribute_type_id):
        idx_at_fts = self._core_model.get_resource_index(AttributeType, FilterType)

        result = idx_at_fts.iter_index(attribute_type_id)
        result = self._resolve_resources(result)

        return result

    def _resolve_attribute_type_sorter_types(self, attribute_type_id):
        idx_at_sts = self._core_model.get_resource_index(AttributeType, SorterType)

        result = idx_at_sts.iter_index(attribute_type_id)
        result = self._resolve_resources(result)

        return result
