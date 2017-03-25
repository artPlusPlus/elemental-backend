import logging

from .._resource_model_base import ResourceModelBase
from .._resource_index import ResourceIndex
from ..resources import (
    FilterInstance
)


_LOG = logging.getLogger(__name__)


class FilterInstanceModel(ResourceModelBase):
    __resource_cls__ = FilterInstance
    __resource_indexes__ = ()

    def register(self, core_model, resource):
        map_fi_vi = self._map__filter_instance__view_instance
        self._fix_map_key(map_fi_vi, filter_instance.id)

        # self._update_view_instance_content_instances()

        hook = filter_instance.kind_params_changed
        handler = self._handler_filter_instance_kind_params_changed
        hook.add_handler(handler)

        ref = type(filter_instance).view_instance
        resolver = self._resolve_filter_instance_view_instance
        ref.add_resolver(filter_instance, resolver)

    def release(self, core_model, resource):
        map_fi_vi = self._map__filter_instance__view_instance
        try:
            del map_fi_vi[filter_instance.id]
        except KeyError:
            pass

        # self._update_view_instance_content_instances()

        hook = filter_instance.kind_params_changed
        handler = self._handler_filter_instance_kind_params_changed
        hook.remove_handler(handler)

        ref = type(filter_instance).view_instance
        ref.remove_resolver(filter_instance)

    def _handler_filter_instance_kind_params_changed(
            self, sender, event_data):
        map_fi_vi = self._map__filter_instance__view_instance
        view_inst_id = map_fi_vi[sender.id]
        # self._update_view_instance_content_instances(view_inst_id)

    def _resolve_filter_instance_view_instance(self, filter_instance_id):
        map_fi_vi = self._map__filter_instance__view_instance

        result = map_fi_vi.get(filter_instance_id)
        if result:
            result = self._resources.get(result)

        return result