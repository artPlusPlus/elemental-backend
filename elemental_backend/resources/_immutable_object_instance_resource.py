from elemental_core import (
    Hook,
    ValueChangedHookData
)
from elemental_core.util import process_uuids_value

from ._immutable_instance_resource import ImmutableInstanceResource
from ._resource_reference import ResourceReference


class ImmutableObjectInstanceResource(ImmutableInstanceResource):
    @ResourceReference
    def field_instances(self):
        return self._field_instance_ids

    @property
    def field_instance_ids(self):
        return self._field_instance_ids

    @field_instance_ids.setter
    def field_instance_ids(self, value):
        value = process_uuids_value(value)
        value = tuple(value)

        if value == self._field_instance_ids:
            return

        original_value = self._field_instance_ids
        self._field_instance_ids = value

        self._on_extends_resource_ids_changed(original_value, value)

    def __init__(self):
        super(ImmutableObjectInstanceResource, self).__init__()

        self._field_instance_ids = tuple()

        self.field_instance_ids_changed = Hook()

    def _on_field_instance_ids_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.field_instance_ids_changed(self, data)