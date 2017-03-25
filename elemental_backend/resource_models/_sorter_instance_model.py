import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    SorterInstance
)


_LOG = logging.getLogger(__name__)


class SorterInstanceModel(ResourceModelBase):
    __resource_cls__ = SorterInstance
    __resource_indexes__ = ()


    def register(self, core_model, resource):
        map_si_vi = self._map__sorter_instance__view_instance
        self._fix_map_key(map_si_vi, sorter_instance.id)

        # self._update_view_instance_content_instances()

        hook = sorter_instance.kind_params_changed
        handler = self._handler_sorter_instance_kind_params_changed
        hook.add_handler(handler)

        ref = type(sorter_instance).view_instance
        resolver = self._resolve_sorter_instance_view_instance
        ref.add_resolver(sorter_instance, resolver)

    def release(self, core_model, resource):
        map_si_vi = self._map__sorter_instance__view_instance
        try:
            del map_si_vi[sorter_instance.id]
        except KeyError:
            pass

        # self._update_view_instance_content_instances()

        hook = sorter_instance.kind_params_changed
        handler = self._handler_sorter_instance_kind_params_changed
        hook.remove_handler(handler)

        ref = type(sorter_instance).view_instance
        ref.remove_resolver(sorter_instance)

    def _handler_sorter_instance_kind_params_changed(
            self, sender, event_data):
        map_si_vi = self._map__sorter_instance__view_instance

        view_inst_id = map_si_vi[sender.id]

        # self._update_view_instance_content_instances(view_inst_id)

    def _resolve_sorter_instance_view_instance(self, sorter_instance_id):
        map_si_vi = self._map__sorter_instance__view_instance

        result = map_si_vi.get(sorter_instance_id)
        if result:
            result = self._resources.get(result)

        return result