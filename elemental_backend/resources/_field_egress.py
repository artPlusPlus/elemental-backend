from ._field_value import FieldValue
from elemental_backend.resources._hook import Hook


class FieldEgress(object):
    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, value):
        if value is self._field:
            return
        elif self._field:
            self._field.value_changed.remove_handler(self._handle_field_changed)

        self._field = value
        self._field.value_changed.add_handler(self._handle_field_changed)

    @property
    def field_changed(self):
        return self._field_changed_hook

    def __init__(self, field):
        self._field = field
        self._field_changed = Hook()

    def _handle_field_changed(self, sender, data):
        self._field_changed(sender, data)
