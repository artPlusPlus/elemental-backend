from typing import Union
from uuid import UUID

from elemental_core import (
    ForwardReference,
    Hook,
    ValueChangedHookData,
    NO_VALUE
)

from ._immutable_resource import ImmutableResource


class ImmutableTypeResource(ImmutableResource):
    """
    Represents a type whose data is not tracked using the `Value` system.
    """
    label_data_id_changed = Hook()
    label_changed = Hook()
    doc_data_id_changed = Hook()
    doc_changed = Hook()

    label_data_ref = ForwardReference()
    doc_data_ref = ForwardReference()

    @property
    def label_data_id(self) -> UUID:
        return self._label_data_id

    @label_data_id.setter
    def label_data_id(self,
                      value: Union[UUID, str]):
        self._set_data_id(value, '_label_data_id', self.label_data_ref,
                          self._handle_label_content_changed,
                          self._on_label_data_id_changed,
                          self._on_label_data_content_changed)

    @property
    def label(self):
        return self.label_data_ref().content

    @label.setter
    def label(self, value):
        self.label_data_ref().content = value

    @property
    def doc_data_id(self) -> UUID:
        return self._doc_data_id

    @doc_data_id.setter
    def doc_data_id(self,
                    value: Union[UUID, str]):
        self._set_data_id(value, '_doc_data_id', self.doc_data_ref,
                          self._handle_doc_content_changed,
                          self._on_doc_data_id_changed,
                          self._on_doc_data_content_changed)

    @property
    def doc(self):
        return self.doc_data_ref().content

    @doc.setter
    def doc(self, value):
        self.doc_data_ref().content = value

    def __init__(self,
                 id: Union[UUID, str] = None,
                 label_data_id: Union[UUID, str] = None,
                 doc_data_id: Union[UUID, str] = None):
        super(ImmutableTypeResource, self).__init__(id=id)

        self._label_data_id = None
        self._doc_data_id = None

        self.label_data_id = label_data_id
        self.doc_data_id = doc_data_id

    @label_data_ref.key_getter
    def _label_data_key_getter(self):
        return self._label_data_id

    @label_data_ref.populated
    def _label_data_ref_populated(self, value):
        value.content_changed += self._handle_label_data_content_changed
        self._on_label_data_content_changed(NO_VALUE, value.content)

    @doc_data_ref.key_getter
    def _doc_data_key_getter(self):
        return self._doc_data_id

    @doc_data_ref.populated
    def _doc_data_ref_populated(self, value):
        value.content_changed += self._handle_doc_data_content_changed
        self._on_doc_data_content_changed(NO_VALUE, value.content)

    def _on_label_data_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.label_data_id_changed(self, data)

    def _on_label_data_content_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.label_changed(self, data)

    def _on_doc_data_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.doc_data_id_changed(self, data)

    def _on_doc_data_content_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.doc_changed(self, data)

    def _handle_label_data_content_changed(self, sender, data: ValueChangedHookData):
        self._on_label_data_content_changed(data.original_value, data.current_value)

    def _handle_doc_data_content_changed(self, sender, data: ValueChangedHookData):
        self._on_doc_data_content_changed(data.original_value, data.current_value)