from uuid import UUID

from elemental_core import (
    Hook,
    ValueChangedHookData
)
from elemental_core.util import process_uuid_value

from ._immutable_resource import ImmutableResource
from ._resource_reference import ResourceReference


class ImmutableInstanceResource(ImmutableResource):
    @ResourceReference
    def type_resource(self):
        return self._type_resource_id

    @property
    def type_resource_id(self):
        return self._type_resource_id

    @type_resource_id.setter
    def type_resource_id(self, value: UUID):
        value = process_uuid_value(value)
        if value == self._type_resource_id:
            return

        original_value = self._type_resource_id
        self._type_resource_id = value

        self._on_type_resource_id_changed(original_value, value)

    def __init__(self):
        super(ImmutableInstanceResource, self).__init__()

        self._type_resource_id = None

        self.type_resource_id_changed = Hook()

    def _on_type_resource_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.type_resource_id_changed(self, data)
