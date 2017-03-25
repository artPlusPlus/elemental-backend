import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    SorterInstance,
    ViewInstance
)


_LOG = logging.getLogger(__name__)


class SorterInstanceModel(ResourceModelBase):
    __resource_cls__ = SorterInstance
    __resource_indexes__ = (
        ResourceIndex(SorterInstance, ViewInstance, indexed_capacity=1)
    )

    def register(self, core_model, resource):
        idx_si_vi = core_model.get_resource_index(SorterInstance, ViewInstance)
        idx_si_vi.create_index(resource)

        # self._update_view_instance_content_instances()

        hook = resource.kind_params_changed
        handler = self._handler_sorter_instance_kind_params_changed
        hook.add_handler(handler)

        ref = type(resource).view_instance
        resolver = self._resolve_sorter_instance_view_instance
        ref.add_resolver(resource, resolver)

    def retrieve(self, core_model, resource_id, resource=None):
        return resource

    def release(self, core_model, resource):
        idx_si_vi = core_model.get_resource_index(SorterInstance, ViewInstance)
        idx_si_vi.pop_index(resource)

        # self._update_view_instance_content_instances()

        hook = resource.kind_params_changed
        handler = self._handler_sorter_instance_kind_params_changed
        hook.remove_handler(handler)

        ref = type(resource).view_instance
        ref.remove_resolver(resource)

    def _handler_sorter_instance_kind_params_changed(self, sender, event_data):
        idx_si_vi = self._core_model.get_resource_index(SorterInstance, ViewInstance)

        try:
            view_inst_id = idx_si_vi.get_indexed_value(sender)[0]
        except IndexError:
            return

        # self._update_view_instance_content_instances(view_inst_id)

    def _resolve_sorter_instance_view_instance(self, sorter_instance_id):
        idx_si_vi = self._core_model.get_resource_index(SorterInstance, ViewInstance)

        try:
            result = idx_si_vi.get_indexed_value(sender)[0]
        except IndexError:
            result = None
        else:
            result = self._resolve_resource(result)

        return result
