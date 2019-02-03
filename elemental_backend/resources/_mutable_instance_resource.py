from elemental_core import (
    ForwardReference,
    Hook,
    ValueChangedHookData
)
from elemental_core.util import process_uuid_value

from ._resource import Resource


class MutableInstanceResource(Resource):
    resource_type_id_changed = Hook()

    @ForwardReference
    def resource_type(self):
        return self._resource_type_id

    @property
    def resource_type_id(self):
        return self._resource_type_id

    @resource_type_id.setter
    def resource_type_id(self, value):
        value = process_uuid_value(value)

        if value == self._resource_type_id:
            return

        original_value = self._resource_type_id
        self._resource_type_id = value

        self._on_resource_type_id_changed(original_value,
                                          self._resource_type_id)

    def __init__(self):
        super(MutableInstanceResource, self).__init__()

        self._resource_type_id = None

    def _on_resource_type_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.resource_type_id_changed(self, data)

