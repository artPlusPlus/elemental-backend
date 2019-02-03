from typing import Union
from uuid import UUID

from elemental_core import (
    Hook,
    ValueChangedHookData,
    ForwardReference,
    NO_VALUE
)
from elemental_core.util import process_uuid_value

from .value_fragment_type_resource import ValueFragmentTypeResource


class PostValueFragmentTypeResource(ValueFragmentTypeResource):
    data_id_changed = Hook()

    data_ref = ForwardReference()

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

        self._on_data_id_changed(original_value, self._data_id)

    def __init__(self,
                 id: Union[UUID, str] = None,
                 data_id: Union[UUID, str] = None):
        super(PostValueFragmentTypeResource, self).__init__(id=id)

        self._data_id = None

        self.data_id = data_id

    @data_ref.key_getter
    def _data_ref_key_getter(self):
        return self._data_id

    @data_ref.populated
    def _data_ref_populated(self, value):
        value.content_changed += self._handle_value_data_content_changed
        self._on_value_data_content_changed(NO_VALUE, value.content)

    def _on_data_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.data_id_changed(self, data)

    def _compute(self, previous):
        return self.data_ref().content
