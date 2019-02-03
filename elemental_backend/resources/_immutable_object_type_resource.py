from typing import Union
from uuid import UUID

from elemental_core import (
    NO_VALUE,
    ForwardReference,
    Hook,
    ValueChangedHookData,
)

from ._immutable_type_resource import ImmutableTypeResource


class ImmutableObjectTypeResource(ImmutableTypeResource):
    extends_resource_ids_data_id_changed = Hook()
    extends_resource_ids_changed = Hook()
    field_type_ids_data_id_changed = Hook()
    field_type_ids_changed = Hook()

    extends_resource_ids_data_ref = ForwardReference()
    field_type_ids_data_ref = ForwardReference()

    @property
    def extends_resource_ids_data_id(self):
        return self._extends_resource_ids_data_id

    @extends_resource_ids_data_id.setter
    def extends_resource_ids_data_id(self, value):
        self._set_data_id(value, '_extends_resource_ids_data_id',
                          self.extends_resource_ids_data_ref,
                          self._handle_extends_resource_ids_data_content_changed,
                          self._on_extends_resource_ids_data_id_changed,
                          self._on_extends_resource_ids_data_content_changed)

    @property
    def field_type_ids(self):
        return self._field_type_ids

    @field_type_ids.setter
    def field_type_ids(self, value):
        self._set_data_id(value, '_field_type_ids_data_id',
                          self.field_type_ids_data_ref,
                          self._handle_field_type_ids_data_content_changed,
                          self._on_field_type_ids_data_id_changed,
                          self._on_field_type_ids_data_content_changed)

    @property
    def extends_resource_ids(self):
        return self.extends_resource_ids_data_ref().content

    @extends_resource_ids.setter
    def extends_resource_ids(self, value):
        self.extends_resource_ids_data_ref().content = value
        # value = process_uuids_value(value)
        # value = tuple(value)
        #
        # if value == self.extends_resource_ids:
        #     return
        #
        # original_value = self._extends_resource_ids
        # self._extends_resource_ids = value
        #
        # self._on_extends_resource_ids_changed(original_value, value)

    @property
    def field_type_ids(self):
        return self.field_type_ids_data_ref().content

    @field_type_ids.setter
    def field_type_ids(self, value):
        self.field_type_ids_data_ref().content = value

    def __init__(self,
                 extends_resource_ids_data_id: Union[UUID, str] = None,
                 field_type_ids_data_id: Union[UUID, str] = None):
        super(ImmutableObjectTypeResource, self).__init__()

        self._extends_resource_ids_data_id = None
        self._field_type_ids_data_id = None

        self.extends_resource_ids_data_id = extends_resource_ids_data_id
        self.field_type_ids_data_id = field_type_ids_data_id

    @extends_resource_ids_data_ref.key_getter
    def _extends_resource_ids_key_getter(self):
        return self._extends_resource_ids_data_id

    @extends_resource_ids_data_ref.populated
    def _extends_resource_ids_populated(self, value):
        value.content_changed += self._handle_extends_resource_ids_data_content_changed
        self._on_extends_resource_ids_data_content_changed(NO_VALUE, value.content)

    @field_type_ids_data_ref.key_getter
    def _field_type_ids_key_getter(self):
        return self._field_type_ids_data_id

    @field_type_ids_data_ref.populated
    def _field_type_ids_populated(self, value):
        value.content_changed += self._handle_field_type_ids_data_content_changed
        self._on_field_type_ids_data_content_changed(NO_VALUE, value.content)

    def _on_extends_resource_ids_data_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.extends_resource_ids_data_id_changed(self, data)

    def _on_extends_resource_ids_data_content_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.extends_resource_ids_changed(self, data)

    def _on_field_type_ids_data_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.field_type_ids_data_id_changed(self, data)

    def _on_field_type_ids_data_content_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.field_type_ids_changed(self, data)

    def _handle_extends_resource_ids_data_content_changed(self, sender, data):
        self._on_extends_resource_ids_data_content_changed(data.original_value,
                                                           data.current_value)

    def _handle_field_type_ids_data_content_changed(self, sender, data):
        self._on_field_type_ids_data_content_changed(data.original_value,
                                                     data.current_value)
