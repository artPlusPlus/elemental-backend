import logging

from .._resource_model_base import ResourceModelBase
from ..resources import ImmutableFieldTypeResource


_LOG = logging.getLogger(__name__)


class ImmutableFieldTypeResourceModel(ResourceModelBase):
    __resource_cls__ = ImmutableFieldTypeResource
    __resource_indexes__ = tuple()

    def _init_hook_forward_reference_map(self):
        super(ImmutableFieldTypeResourceModel, self)._init_hook_forward_reference_map()

        hook = self.__resource_cls__.kind_id_data_id_changed
        handler = self._handle_kind_id_data_id_changed
        self._map__hook__handler[hook] = handler

        hook = self.__resource_cls__.kind_params_data_id_changed
        handler = self._handle_kind_params_data_id_changed
        self._map__hook__handler[hook] = handler

    def _init_forward_reference_resolver_map(self):
        super(ImmutableFieldTypeResourceModel, self)._init_forward_reference_resolver_map()

        ref = self.__resource_cls__.kind_id_data_ref
        resolver = self._get_resource
        self._map__forward_reference__resolver[ref] = resolver

        ref = self.__resource_cls__.kind_params_data_ref
        resolver = self._get_resource
        self._map__forward_reference__resolver[ref] = resolver
