from elemental_core import (
    Hook,
    ValueChangedHookData
)
from elemental_core.util import process_uuid_value

from ._immutable_instance_resource import ImmutableInstanceResource
from ._resource_reference import ResourceReference


class ImmutableFieldInstanceResource(ImmutableInstanceResource):
    @ResourceReference
    def data(self):
        return self._data_id

    @property
    def data_id(self):
        return self._data_id

    @data_id.setter
    def data_id(self, value):
        value = process_uuid_value(value)

        if value == self._data_id:
            return

        original_value = self._data_id
        self._data_id = value

        original_value.content_changed -= self._handle_data_content_changed
        self._data_id.content_changed += self._handle_data_content_changed

        self._on_data_id_changed(original_value, value)

    def __init__(self):
        super(ImmutableFieldInstanceResource, self).__init__()

        self._data_id = None

        self.data_id_changed = Hook()
        self.content_changed = Hook()

    def _on_data_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.data_id_changed(self, data)

    def _handle_data_content_changed(self, sender, data: ValueChangedHookData):
        self.content_changed(self, data)
