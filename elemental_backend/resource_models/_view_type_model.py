import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    ViewType,
    ContentInstance,
    ContentType
)


_LOG = logging.getLogger(__name__)


class ViewTypeModel(ResourceModelBase):
    __resource_cls__ = ViewType
    __resource_indexes__ = (
        ResourceIndex(ViewType, ContentInstance),
        ResourceIndex(ContentType, ViewType)
    )

    def register(self, resource):
        idx_vt_cis = self._get_index(ViewType, ContentInstance)
        idx_vt_cis.create_index(resource)

        idx_ct_vts = self._get_index(ContentType, ViewType)
        for content_type_id in resource.content_type_ids:
            idx_ct_vts.push_index_value(content_type_id, resource)

        raise RuntimeError('TODO: Add ViewTypeModel Hook.')
        # self._update_view_type_content_instances(resource.id)

        hook = resource.content_type_ids_changed
        handler = self._handle_view_type_content_type_ids_changed
        hook.add_handler(handler)

        hook = resource.filter_type_ids_changed
        handler = self._handle_view_type_filter_type_ids_changed
        hook.add_handler(handler)

        hook = resource.sorter_type_ids_changed
        handler = self._handle_view_type_sorter_type_ids_changed
        hook.add_handler(handler)

        ref = type(resource).content_types
        resolver = self._get_resources
        ref.add_resolver(resource, resolver)

        ref = type(resource).filter_types
        resolver = self._get_resources
        ref.add_resolver(resource, resolver)

        ref = type(resource).sorter_types
        resolver = self._get_resources
        ref.add_resolver(resource, resolver)

        ref = type(resource).content_instances
        resolver = self._resolve_view_type_content_instances
        ref.add_resolver(resource, resolver)

    def retrieve(self, resource_id, resource=None):
        return resource

    def release(self, resource):
        idx_vt_cis = self._get_index(ViewType, ContentInstance)
        idx_vt_cis.pop_index(resource)

        idx_ct_vts = self._get_index(ContentType, ViewType)
        for content_type_id in resource.content_type_ids:
            idx_ct_vts.pop_index_value(content_type_id, resource)

        hook = resource.content_type_ids_changed
        handler = self._handle_view_type_content_type_ids_changed
        hook.remove_handler(handler)

        hook = resource.filter_type_ids_changed
        handler = self._handle_view_type_filter_type_ids_changed
        hook.remove_handler(handler)

        hook = resource.sorter_type_ids_changed
        handler = self._handle_view_type_sorter_type_ids_changed
        hook.remove_handler(handler)

        ref = type(resource).content_types
        ref.remove_resolver(resource)

        ref = type(resource).filter_types
        ref.remove_resolver(resource)

        ref = type(resource).sorter_types
        ref.remove_resolver(resource)

        ref = type(resource).content_instances
        ref.remove_resolver(resource)

    def _handle_view_type_filter_type_ids_changed(
            self, sender, event_data):
        map_rt_ri = self._map__resource_type__resource_instances
        # for view_inst_id in map_rt_ri[sender.id]:
        #     self._update_view_instance_content_instances(view_inst_id)

    def _handle_view_type_sorter_type_ids_changed(
            self, sender, event_data):
        pass

    def _resolve_view_type_content_instances(self, view_type_id):
        idx_vt_cis = self._get_index(ViewType, ContentInstance)

        result = idx_vt_cis.iter_indexed_values(view_type_id)
        result = self._get_resources(result)

        return result

    def _update_view_type_content_instances(self, view_type_id):
        """
        Builds a mapping of all ContentInstances that qualify for a ViewType.

        A ViewType holds references to ContentTypes. All ContentInstances
        of each of these ContentTypes form a base pool. This pool is used by
        the ViewType's ViewInstances. The ViewInstances apply the
        FilterInstances to each ContentInstance in the pool to compute the
        data for a corresponding ViewResult.
        """
        view_type = self._core_model.get_resource(view_type_id)
        idx_rt_ri = self._core_model.get_resource_index(ResourceType, ResourceInstance)
        idx_vt_cis = self._core_model.get_resource_index(ViewType, ContentInstance)

        content_inst_ids = map_vt_cis[view_type.id]
        content_inst_ids.clear()
        for type_id in view_type.content_type_ids:
            content_inst_ids.update(map_rt_ri.get(type_id, tuple()))

