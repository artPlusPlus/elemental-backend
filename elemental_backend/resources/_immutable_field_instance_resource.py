from typing import Union
from uuid import UUID

from elemental_core import (
    ForwardReference,
    Hook,
    ValueChangedHookData,
    NO_VALUE
)

from ._immutable_instance_resource import ImmutableInstanceResource


class ImmutableFieldInstanceResource(ImmutableInstanceResource):
    value_data_id_changed = Hook()
    value_changed = Hook()

    value_data_ref = ForwardReference()

    @property
    def value_data_id(self):
        return self._value_data_id

    @value_data_id.setter
    def value_data_id(self, value):
        self._set_data_id(value, '_value_data_id', self.value_data_ref,
                          self._handle_value_data_content_changed,
                          self._on_value_data_id_changed,
                          self._on_value_data_content_changed)

    @property
    def value(self):
        return self.value_data_ref().content

    @value.setter
    def value(self, value):
        field_type = self.type_resource_ref()
        field_kind_id = field_type.kind
        field_kind_params = field_type.kind_params

        kind = get_kind(field_kind_id)
        value = kind.process(value, field_kind_params)
        kind.validate(value, field_kind_params)

        self.value_data_ref().content = value

    def __init__(self,
                 id: Union[UUID, str] = None,
                 type_resource_id: Union[UUID, str] = None,
                 value_data_id: Union[UUID, str] = None):
        super(ImmutableFieldInstanceResource, self).__init__(
            id=id,
            type_resource_id=type_resource_id
        )

        self._value_data_id = None

        self.value_data_id = value_data_id

    @value_data_ref.key_getter
    def _value_data_ref_key_getter(self):
        return self._value_data_id

    @value_data_ref.populated
    def _value_data_ref_populated(self, value):
        value.content_changed += self._handle_value_data_content_changed
        self._on_value_data_content_changed(NO_VALUE, value.content)

    def _on_value_data_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.value_data_id_changed(self, data)

    def _on_value_data_content_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.value_changed(self, data)

    def _handle_value_data_content_changed(self, sender, data: ValueChangedHookData):
        self._on_value_data_content_changed(data.original_value, data.current_value)
