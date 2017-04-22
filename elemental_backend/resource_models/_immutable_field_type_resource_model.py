import logging
import weakref
from uuid import UUID
from typing import Optional

from .._resource_model_base import ResourceModelBase
from ..resources import ImmutableFieldTypeResource


_LOG = logging.getLogger(__name__)


class ImmutableFieldTypeResourceModel(ResourceModelBase):
    __resource_cls__ = ImmutableFieldTypeResource
    __resource_indexes__ = tuple()

    def __init__(self, resource_getter, index_getter):
        super(ImmutableFieldTypeResourceModel, self).__init__(
            resource_getter, index_getter)

        self._unresolved_kind_id_refs = weakref.WeakKeyDictionary()
        self._unresolved_kind_params_refs = weakref.WeakKeyDictionary()
        self._resolved_kind_id_refs = weakref.WeakKeyDictionary()
        self._resolved_kind_params_refs = weakref.WeakKeyDictionary()

        ImmutableFieldTypeResource.kind_id_data_ref.reference_resolver = self._get_resource
        ImmutableFieldTypeResource.kind_params_data_ref.reference_resolver = self._get_resource

    def register(self,
                 resource: ImmutableFieldTypeResource):
        hook = resource.data_id_changed
        hook += self._handle_data_id_changed

        if resource.kind_id_data_id:
            if resource.kind_id_data_ref():
                reference_map = self._resolved_kind_id_refs
            else:
                reference_map = self._unresolved_kind_id_refs
            self._track_forward_reference(resource.id,
                                          resource.kind_id_data_id,
                                          reference_map)

        if resource.kind_params_data_id:
            if resource.kind_params_data_ref():
                reference_map = self._resolved_kind_params_refs
            else:
                reference_map = self._unresolved_kind_params_refs
            self._track_forward_reference(resource.id,
                                          resource.kind_params_data_id,
                                          reference_map)

    def retrieve(self,
                 resource_id: UUID,
                 resource: ImmutableFieldTypeResource = None
                 ) -> Optional[ImmutableFieldTypeResource]:
        return resource

    def release(self,
                resource: ImmutableFieldTypeResource):
        hook = resource.data_id_changed
        hook -= self._handle_data_id_changed

    def _handle_resource_registered(self, sender, data):
        self._resolve_forward_reference(data, 'kind_id_data_ref',
                                        self._unresolved_kind_id_refs,
                                        self._resolved_kind_id_refs)

        self._resolve_forward_reference(data, 'kind_params_data_ref',
                                        self._unresolved_kind_params_refs,
                                        self._resolved_kind_params_refs)

    def _handle_resource_released(self, sender, data):
        self._break_forward_reference(data, 'kind_id_data_ref',
                                      self._resolved_kind_id_refs,
                                      self._unresolved_kind_id_refs)

        self._break_forward_reference(data, 'kind_params_data_ref',
                                      self._resolved_kind_params_refs,
                                      self._unresolved_kind_params_refs)

    def _handle_kind_id_data_id_changed(self, sender, data):
        self._forward_reference_target_changed(sender, 'kind_id_data_ref',
                                               self._unresolved_kind_id_refs,
                                               data.original_value)

    def _handle_kind_params_data_id_changed(self, sender, data):
        self._forward_reference_target_changed(sender, 'kind_params_data_ref',
                                               self._unresolved_kind_params_refs,
                                               data.original_value)
