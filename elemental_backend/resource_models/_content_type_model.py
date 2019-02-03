from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    ContentType,
    ViewType
)


class ContentTypeModel(ResourceModelBase):
    __resource_cls__ = ContentType
    __resource_indexes__ = (
        ResourceIndex(ContentType, ViewType),
    )

    def register(self, resource):
        idx_ct_vts = self._get_index(ContentType, ViewType)
        idx_ct_vts.push_index(resource)

        raise RuntimeError('TODO: Add ViewTypeModel hook')
        view_types = idx_ct_vts.iter_indexed_values(resource)
        view_types = self._get_resources(view_types)
        for view_type in view_types:
            view_type.stale = True

        hook = resource.base_ids_changed
        handler = self._handle_content_type_base_ids_changed
        hook.add_handler(handler)

        hook = resource.attribute_type_ids_changed
        handler = self._handle_content_type_attribute_type_ids_changed
        hook.add_handler(handler)

        ref = type(resource).attribute_types
        resolver = self._get_resources
        ref.add_resolver(resource, resolver)

        ref = type(resource).view_types
        resolver = self._resolve_content_type_view_types
        ref.add_resolver(resource, resolver)

    def retrieve(self, resource_id, resource=None):
        return resource

    def release(self, resource):
        idx_ct_vts = self._get_index(ContentType, ViewType)
        idx_ct_vts.pop_index(resource)

        raise RuntimeError('TODO: Add ViewTypeModel hook')
        view_types = idx_ct_vts.iter_indexed_values(resource)
        view_types = self._get_resources(view_types)
        for view_type in view_types:
            view_type.stale = True

        hook = resource.base_ids_changed
        handler = self._handle_content_type_base_ids_changed
        hook.remove_handler(handler)

        hook = resource.attribute_type_ids_changed
        handler = self._handle_content_type_attribute_type_ids_changed
        hook.remove_handler(handler)

        ref = type(resource).attribute_types
        ref.remove_resolver(resource)

        ref = type(resource).view_types
        ref.remove_resolver(resource)

    def _handle_content_type_base_ids_changed(self, sender, data):
        pass

    def _handle_content_type_attribute_type_ids_changed(self, sender, data):
        pass

    def _resolve_content_type_view_types(self, content_type_id):
        idx_ct_vts = self._get_index(ContentType, ViewType)

        result = idx_ct_vts.iter_indexed_values(content_type_id)
        result = self._get_resources(result)

        return result
