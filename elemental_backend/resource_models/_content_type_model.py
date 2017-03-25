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

    def register(self, core_model, resource):
        assert (isinstance(resource, ContentType))

        idx_ct_vts = core_model.get_resource_index(ContentType, ViewType)
        idx_ct_vts.create_index(resource)

        for view_type_id in idx_ct_vts.iter_index(resource):
            view_type = self._core_model.get_resource(view_type_id)
            if view_type:
                view_type.stale = True

        hook = resource.base_ids_changed
        handler = self._handle_content_type_base_ids_changed
        hook.add_handler(handler)

        hook = resource.attribute_type_ids_changed
        handler = self._handle_content_type_attribute_type_ids_changed
        hook.add_handler(handler)

        ref = type(resource).attribute_types
        resolver = self._resolve_resources
        ref.add_resolver(resource, resolver)

        ref = type(resource).view_types
        resolver = self._resolve_content_type_view_types
        ref.add_resolver(resource, resolver)

    def retrieve(self, core_model, resource_id, resource=None):
        return resource

    def release(self, core_model, resource):
        assert (isinstance(resource, ContentType))

        idx_ct_vts = core_model.get_resource_index(ContentType, ViewType)

        view_type_ids = idx_ct_vts.pop_collection(resource.id)
        for view_type_id in view_type_ids:
            view_type = self._core_model.get_resource(view_type_id)
            if view_type:
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
        idx_ct_vts = self._core_model.get_resource_index(ContentType, ViewType)

        result = idx_ct_vts.get(content_type_id, tuple())
        if result:
            result = self._resolve_resources(result)

        return result
