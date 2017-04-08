from elemental_core import (
    Hook,
    ValueChangedHookData
)
from elemental_core.util import process_uuid_value

from ._mutable_instance_resource import MutableInstanceResource
from ._resource_reference import ResourceReference


class MutableFieldInstanceResource(MutableInstanceResource):
    @ResourceReference
    def value(self):
        return self._value_id

    @property
    def value_id(self):
        return self._value_id

    @value_id.setter
    def value_id(self, value):
        value = process_uuid_value(value)

        if value == self._value_id:
            return

        original_value = self._value_id
        self._value_id = value

        self._on_value_id_changed(original_value, value)

    def __init__(self, value_id=None):
        super(MutableFieldInstanceResource, self).__init__()

        self._value_id = None

        self.value_id_changed = Hook()

        self.value_id = value_id

    def _on_value_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.value_id_changed(self, data)
