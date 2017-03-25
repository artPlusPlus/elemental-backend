import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    FilterInstance,
    ViewInstance
)


_LOG = logging.getLogger(__name__)


class FilterInstanceModel(ResourceModelBase):
    __resource_cls__ = FilterInstance
    __resource_indexes__ = (
        ResourceIndex(FilterInstance, ViewInstance, indexed_capacity=1)
    )

    def register(self, core_model, resource):
        idx_fi_vi = core_model.get_resource_index(FilterInstance, ViewInstance)
        idx_fi_vi.create_index(resource)

        # self._update_view_instance_content_instances()

        hook = resource.kind_params_changed
        handler = self._handler_filter_instance_kind_params_changed
        hook.add_handler(handler)

        ref = type(resource).view_instance
        resolver = self._resolve_filter_instance_view_instance
        ref.add_resolver(resource, resolver)

    def retrieve(self, core_model, resource_id, resource=None):
        return resource

    def release(self, core_model, resource):
        idx_fi_vi = core_model.get_resource_index(FilterInstance, ViewInstance)
        idx_fi_vi.pop_index(resource)

        # self._update_view_instance_content_instances()

        hook = resource.kind_params_changed
        handler = self._handler_filter_instance_kind_params_changed
        hook.remove_handler(handler)

        ref = type(resource).view_instance
        ref.remove_resolver(resource)

    def _handler_filter_instance_kind_params_changed(self, sender, event_data):
        idx_fi_vi = self._core_model.get_resource_index(FilterInstance, ViewInstance)

        try:
            view_inst_id = idx_fi_vi.get_indexed_value(sender)[0]
        except IndexError:
            return

        # self._update_view_instance_content_instances(view_inst_id)

    def _resolve_filter_instance_view_instance(self, filter_instance_id):
        idx_fi_vi = self._core_model.get_resource_index(FilterInstance, ViewInstance)

        try:
            result = idx_fi_vi.get_indexed_value(filter_instance_id)[0]
        except IndexError:
            result = None
        else:
            result = self._core_model.get_resource(result)

        return result
