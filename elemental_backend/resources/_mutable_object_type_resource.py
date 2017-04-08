from elemental_core import (
    Hook,
    ValueChangedHookData
)
from elemental_core.util import process_uuid_value

from ._mutable_type_resource import MutableTypeResource
from ._resource_reference import ResourceReference


class MutableObjectTypeResource(MutableTypeResource):
    @ResourceReference
    def extends_type_ids_value(self):
        return self._extends_type_ids_value_id

    @property
    def extends_type_ids_value_id(self):
        return self._extends_type_ids_value_id

    @extends_type_ids_value_id.setter
    def extends_type_ids_value_id(self, value):
        value = process_uuid_value(value)

        if value == self._extends_type_ids_value_id:
            return

        original_value = self._extends_type_ids_value_id
        self._extends_type_ids_value_id = value

        self._on_extends_type_ids_value_id_changed(original_value,
                                                   self._extends_type_ids_value_id)

    @ResourceReference
    def field_type_ids_value(self):
        return self._field_type_ids_value_id

    @property
    def field_type_ids_value_id(self):
        return self._field_type_ids_value_id

    @field_type_ids_value_id.setter
    def field_type_ids_value_id(self, value):
        value = process_uuid_value(value)

        if value == self._field_type_ids_value_id:
            return

        original_value = self._field_type_ids_value_id
        self._field_type_ids_value_id = value

        self._on_field_type_ids_value_id_changed(original_value,
                                                 self._field_type_ids_value_id)

    def __init__(self):
        super(MutableTypeResource, self).__init__()

        self._extends_type_ids_value_id = None
        self._field_type_ids_value_id = None

        self.extends_type_ids_value_id_changed = Hook()
        self.field_type_ids_value_id_changed = Hook()

    def _on_extends_type_ids_value_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.extends_type_ids_value_id_changed(self, data)

    def _on_field_type_ids_value_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.field_type_ids_value_id_changed(self, data)