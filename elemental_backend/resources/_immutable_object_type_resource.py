from typing import List
from uuid import UUID

from elemental_core import (
    Hook,
    ValueChangedHookData
)
from elemental_core.util import process_uuids_value

from ._immutable_type_resource import ImmutableTypeResource


class ImmutableObjectTypeResource(ImmutableTypeResource):
    @property
    def extends_resource_ids(self):
        return self._extends_resource_ids

    @extends_resource_ids.setter
    def extends_resource_ids(self, value):
        value = process_uuids_value(value)
        value = tuple(value)

        if value == self._extends_resource_ids:
            return

        original_value = self._extends_resource_ids
        self._extends_resource_ids = value

        self._on_extends_resource_ids_changed(original_value, value)

    @property
    def field_type_ids(self):
        return self._field_type_ids

    @field_type_ids.setter
    def field_type_ids(self, value):
        value = process_uuids_value(value)
        value = tuple(value)

        if value == self._field_type_ids:
            return

        original_value = self._field_type_ids
        self._field_type_ids = value

        self._on_field_type_ids_changed(original_value, value)

    def __init__(self,
                 extends_resource_ids: List(UUID) = None,
                 field_type_ids: List(UUID) = None):
        super(ImmutableObjectTypeResource, self).__init__()

        self._extends_resource_ids = tuple()
        self._field_type_ids = tuple()

        self.extends_resource_ids_changed = Hook()
        self.field_type_ids_changed = Hook()

        self.extends_resource_ids = extends_resource_ids
        self.field_type_ids = field_type_ids

    def _on_extends_resource_ids_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.extends_resource_ids_changed(self, data)

    def _on_field_type_ids_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.field_type_ids_changed(self, data)