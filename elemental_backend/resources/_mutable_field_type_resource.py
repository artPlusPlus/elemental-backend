from elemental_core import (
    Hook,
    ValueChangedHookData
)
from elemental_core.util import process_uuid_value

from ._mutable_type_resource import MutableTypeResource
from ._resource_reference import ResourceReference


class MutableFieldTypeResource(MutableTypeResource):
    @ResourceReference
    def modifiers_data(self):
        return self._modifiers_data_id

    @property
    def modifiers_data_id(self):
        return self._modifiers_data_id

    @modifiers_data_id.setter
    def modifiers_data_id(self, value):
        value = process_uuid_value(value)

        if value == self._modifiers_data_id:
            return

        original_value = self._modifiers_data_id
        self._modifiers_data_id = value

        self._on_modifiers_data_id_changed(original_value,
                                           self._modifiers_data_id)

    @ResourceReference
    def kind_id_data(self):
        return self._kind_id_data_id

    @property
    def kind_id_data_id(self):
        return self._kind_id_data_id

    @kind_id_data_id.setter
    def kind_id_data_id(self, value):
        value = process_uuid_value(value)

        if value == self._kind_id_data_id:
            return

        original_value = self._kind_id_data_id
        self._kind_id_data_id = value

        self._on_kind_id_data_id_changed(original_value,
                                         self._kind_id_data_id)

    @ResourceReference
    def kind_params_value(self):
        return self._kind_params_value_id

    @property
    def kind_params_value_id(self):
        return self._kind_params_value_id

    @kind_params_value_id.setter
    def kind_params_value_id(self, value):
        value = process_uuid_value(value)

        if value == self._kind_params_value_id:
            return

        original_value = self._kind_params_value_id
        self._kind_params_value_id = value

        self._on_kind_params_value_id_changed(original_value,
                                              self._kind_params_value_id)

    @ResourceReference
    def default_value_value(self):
        return self._default_value_value_id

    @property
    def default_value_value_id(self):
        return self._default_value_value_id

    @default_value_value_id.setter
    def default_value_value_id(self, value):
        value = process_uuid_value(value)

        if value == self._default_value_value_id:
            return

        original_value = self._default_value_value_id
        self._default_value_value_id = value

        self._on_default_value_value_id_changed(original_value,
                                                self._default_value_value_id)

    def __init__(self):
        super(MutableFieldTypeResource, self).__init__()

        self._modifiers_data_id = None
        self._kind_id_data_id = None
        self._kind_params_value_id = None
        self._default_value_value_id = None

        self.modifiers_data_id_changed = Hook()
        self.kind_id_data_id_changed = Hook()
        self.kind_params_value_id_changed = Hook()
        self.default_value_value_id_changed = Hook()

    def _on_modifiers_data_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.modifiers_data_id_changed(self, data)

    def _on_kind_id_data_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.kind_id_data_id_changed(self, data)

    def _on_kind_params_value_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.kind_params_value_id_changed(self, data)

    def _on_default_value_value_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.default_value_value_id_changed(self, data)
