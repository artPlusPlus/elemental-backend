from typing import Union
from uuid import UUID

from elemental_core import (
    ForwardReference,
    Hook,
    ValueChangedHookData,
    NO_VALUE
)

from ._immutable_type_resource import ImmutableTypeResource


class ImmutableFieldTypeResource(ImmutableTypeResource):
    kind_id_data_id_changed = Hook()
    kind_id_changed = Hook()
    kind_params_data_id_changed = Hook()
    kind_params_changed = Hook()

    kind_id_data_ref = ForwardReference()
    kind_params_data_ref = ForwardReference()

    @property
    def kind_id_data_id(self):
        return self._kind_id_data_id

    @kind_id_data_id.setter
    def kind_id_data_id(self, value: UUID):
        self._set_data_id(value, '_kind_id_data_id', self.kind_id_data_ref,
                          self._handle_kind_id_content_changed,
                          self._on_kind_id_data_id_changed,
                          self._on_kind_id_content_changed)

    @property
    def kind_params_data_id(self):
        return self._kind_params_data_id

    @kind_params_data_id.setter
    def kind_params_data_id(self, value: UUID):
        self._set_data_id(value, '_kind_params_data_id', self.kind_params_data_ref,
                          self._handle_kind_params_content_changed,
                          self._on_kind_params_data_id_changed,
                          self._on_kind_params_content_changed)

    @property
    def kind_id(self):
        return self.kind_id_data_ref().content

    @kind_id.setter
    def kind_id(self, value):
        self.kind_id_data_ref().content = value

    @property
    def kind_params(self):
        return self.kind_params_data_ref().content

    @kind_params.setter
    def kind_params(self, value):
        self.kind_params_data_ref().content = value

    def __init__(self,
                 id: Union[UUID, str] = None,
                 label_data_id: Union[UUID, str] = None,
                 doc_data_id: Union[UUID, str] = None,
                 kind_id_data_id: Union[UUID, str] = None,
                 kind_params_data_id: Union[UUID, str] = None):
        super(ImmutableFieldTypeResource, self).__init__(
            id=id,
            label_data_id=label_data_id,
            doc_data_id=doc_data_id
        )

        self._kind_id_data_id = None
        self._kind_params_data_id = None

        self.kind_id_data_id = kind_id_data_id
        self.kind_params_data_id = kind_params_data_id

    @kind_id_data_ref.key_getter
    def _kind_id_data_ref_key_getter(self):
        return self._kind_id_data_id

    @kind_id_data_ref.populated
    def _kind_id_data_ref_populated(self, value):
        value.content_changed += self._handle_kind_id_content_changed
        self._on_kind_id_content_changed(NO_VALUE, value.content)

    @kind_params_data_ref.key_getter
    def _kind_params_data_ref_key_getter(self):
        return self._kind_params_data_id

    @kind_params_data_ref.populated
    def _kind_params_data_ref_populated(self, value):
        value.content_changed += self._handle_kind_params_content_changed
        self._on_kind_params_content_changed(NO_VALUE, value.content)

    def _on_kind_id_data_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.kind_id_data_id_changed(self, data)

    def _on_kind_id_content_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.kind_id_changed(self, data)

    def _on_kind_params_data_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.kind_params_data_id_changed(self, data)

    def _on_kind_params_content_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.kind_params_changed(self, data)

    def _handle_kind_id_content_changed(self, sender, data: ValueChangedHookData):
        self._on_kind_id_content_changed(data.original_value, data.current_value)

    def _handle_kind_params_content_changed(self, sender, data: ValueChangedHookData):
        self._on_kind_params_content_changed(data.original_value, data.current_value)
