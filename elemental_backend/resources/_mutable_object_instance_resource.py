from elemental_core import (
    ForwardReference,
    Hook,
    ValueChangedHookData
)
from elemental_core.util import process_uuid_value

from ._mutable_instance_resource import MutableInstanceResource


class MutableObjectInstanceResource(MutableInstanceResource):
    field_instance_ids_value_id_changed = Hook()

    @ForwardReference
    def field_instance_ids_value(self):
        return self._field_instance_ids_value_id

    @property
    def field_instance_ids_value_id(self):
        return self._field_instance_ids_value_id

    @field_instance_ids_value_id.setter
    def field_instance_ids_value_id(self, value):
        value = process_uuid_value(value)

        if value == self._field_instance_ids_value_id:
            return

        original_value = self._field_instance_ids_value_id
        self._field_instance_ids_value_id = value

        self._on_field_instance_ids_value_id_changed(original_value,
                                                     self._field_instance_ids_value_id)

    def __init__(self):
        super(MutableInstanceResource, self).__init__()

        self._field_instance_ids_value_id = None

    def _on_field_instance_ids_value_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.field_instance_ids_value_id_changed(self, data)
