import logging

from .._resource_model_base import ResourceModelBase
from ..resources import ImmutableObjectInstanceResource


_LOG = logging.getLogger(__name__)


class ImmutableFieldInstanceResourceModel(ResourceModelBase):
    __resource_cls__ = ImmutableObjectInstanceResource
    __resource_indexes__ = tuple()

    def _init_hook_forward_reference_map(self):
        super(ImmutableFieldInstanceResourceModel, self)._init_hook_forward_reference_map()

        hook = self.__resource_cls__.data_id_changed
        ref = self.__resource_cls__.value_data_ref
        self._map__hook__forward_reference[hook] = ref

    def _init_forward_reference_resolver_map(self):
        super(ImmutableFieldInstanceResourceModel, self)._init_forward_reference_resolver_map()

        ref = self.__resource_cls__.value_data_ref
        resolver = self._get_resource
        self._map__forward_reference__resolver[ref] = resolver
