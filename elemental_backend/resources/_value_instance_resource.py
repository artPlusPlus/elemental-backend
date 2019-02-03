from elemental_core import (
    Hook,
    ValueChangedHookData
)
from elemental_core.util import process_uuid_value

from ._immutable_instance_resource import ImmutableInstanceResource
from ._resource_reference import ResourceReference


class ValueInstanceResource(ImmutableInstanceResource):
    start_fragment_changed = Hook()



    @ResourceReference
    def start_fragment(self):
        return self._start_fragment_id

    @property
    def start_fragment_id(self):
        return self._start_fragment_id

    @start_fragment_id.setter
    def start_fragment_id(self, value):
        value = process_uuid_value(value)

        if value == self._start_fragment_id:
            return

        original_value = self._start_fragment_id
        self._start_fragment_id = value

        self._on_start_fragment_id_changed(original_value, value)

    def __init__(self):
        super(ValueInstanceResource, self).__init__()

        self._start_fragment_id = None



    def _on_start_fragment_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self.start_fragment_changed(self, data)
