from typing import Union
from uuid import UUID

from elemental_core import (
    ForwardReference,
    Hook,
    ValueChangedHookData
)

from elemental_core.util import process_uuid_value

from ._immutable_resource import ImmutableResource


class ImmutableInstanceResource(ImmutableResource):
    type_resource_id_changed = Hook()

    type_resource_ref = ForwardReference()

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

    def __init__(self,
                 id: Union[UUID, str] = None,
                 type_resource_id: Union[UUID, str] = None):
        super(ImmutableInstanceResource, self).__init__(id=id)

        self._type_resource_id = None

        self.type_resource_id = type_resource_id

    @type_resource_ref.key_getter
    def _type_resource_key_getter(self):
        return self._type_resource_id

    @type_resource_ref.populated
    def _type_resource_populated(self, value):
        pass

    def _on_type_resource_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.type_resource_id_changed(self, data)
