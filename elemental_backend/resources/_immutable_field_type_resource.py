from typing import Dict, Any

from elemental_core import (
    Hook,
    ValueChangedHookData
)

from ._immutable_type_resource import ImmutableTypeResource


class ImmutableFieldTypeResource(ImmutableTypeResource):
    @property
    def kind_id(self):
        return self._kind_id

    @kind_id.setter
    def kind_id(self, value):
        if value == self._kind_id:
            return

        original_value = self._kind_id
        self._kind_id = value

        self._on_kind_id_changed(original_value, value)

    @property
    def kind_params(self):
        return self._kind_params.copy()

    @kind_params.setter
    def kind_params(self, value: Dict(str, Any)):
        if value == self._kind_params:
            return

        original_value = self._kind_params.copy()
        self._kind_params = value.copy()

        self._on_kind_params_changed(original_value, self._kind_params.copy())

    def __init__(self):
        super(ImmutableFieldTypeResource, self).__init__()

        self._kind_id = None
        self._kind_params = {}

        self.kind_id_changed = Hook()
        self.kind_params_changed = Hook()

    def _on_kind_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.kind_id_changed(self, data)

    def _on_kind_params_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.kind_id_changed(self, data)
