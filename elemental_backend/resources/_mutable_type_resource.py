from elemental_core import (
    Hook,
    ValueChangedHookData
)
from elemental_core.util import process_uuid_value

from ._mutable_resource import MutableResource
from ._resource_reference import ResourceReference


class MutableTypeResource(MutableResource):
    @ResourceReference
    def label_value(self):
        return self._label_value_id

    @property
    def label_value_id(self):
        return self._label_value_id

    @label_value_id.setter
    def label_value_id(self, value):
        value = process_uuid_value(value)
        if value == self._label_value_id:
            return

        original_value = self._label_value_id
        self._label_value_id = value

        self._on_label_value_id_changed(original_value, value)

    @ResourceReference
    def doc_value(self):
        return self._doc_value_id

    @property
    def doc_value_id(self):
        return self._doc_value_id

    @doc_value_id.setter
    def doc_value_id(self, value):
        value = process_uuid_value(value)
        if value == self._doc_value_id:
            return

        original_value = self._doc_value_id
        self._doc_value_id = value

        self._on_doc_value_id_changed(original_value, value)

    def __init__(self):
        super(MutableResource, self).__init__()

        self._label_value_id = None
        self._doc_value_id = None

        self.label_value_id_changed = Hook()
        self.doc_value_id_changed = Hook()

    def _on_label_value_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.label_value_id_changed(self, data)

    def _on_doc_value_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.doc_value_id_changed(self, data)
