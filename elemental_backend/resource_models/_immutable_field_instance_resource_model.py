import logging
import weakref
from uuid import UUID
from typing import Optional

from .._resource_model_base import ResourceModelBase
from ..resources import ImmutableFieldInstanceResource


_LOG = logging.getLogger(__name__)


class ImmutableFieldInstanceResourceModel(ResourceModelBase):
    __resource_cls__ = ImmutableFieldInstanceResource
    __resource_indexes__ = tuple()

    def __init__(self, resource_getter, index_getter):
        super(ImmutableFieldInstanceResourceModel, self).__init__(
            resource_getter, index_getter)

        self._unresolved_data_refs = weakref.WeakKeyDictionary()
        self._resolved_data_refs = weakref.WeakKeyDictionary()

        ImmutableFieldInstanceResource.data.reference_resolver = self._get_resource

    def register(self,
                 resource: ImmutableFieldInstanceResource):
        hook = resource.data_id_changed
        hook += self._handle_data_id_changed

        if resource.data_id:
            if resource.data_ref():
                reference_map = self._resolved_data_refs
            else:
                reference_map = self._unresolved_data_refs
            self._track_forward_reference(resource.id, resource.data_id,
                                          reference_map)

    def retrieve(self,
                 resource_id: UUID,
                 resource: ImmutableFieldInstanceResource = None
                 ) -> Optional[ImmutableFieldInstanceResource]:
        return resource

    def release(self,
                resource: ImmutableFieldInstanceResource):
        hook = resource.data_id_changed
        hook -= self._handle_data_id_changed

    def _handle_resource_registered(self, sender, data):
        self._resolve_forward_reference(data, 'data_ref',
                                        self._unresolved_data_refs,
                                        self._resolved_data_refs)

    def _handle_resource_released(self, sender, data):
        self._break_forward_reference(data, 'data_ref',
                                      self._resolved_data_refs,
                                      self._unresolved_data_refs)

    def _handle_data_id_changed(self, sender, data):
        self._forward_reference_target_changed(sender, 'data_ref',
                                               self._unresolved_data_refs,
                                               data.original_value)
