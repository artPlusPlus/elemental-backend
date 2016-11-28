from ._field_value import FieldValue


class FieldDataValue(FieldValue):
    @property
    def value(self):
        self._is_dirty = False
        return self._value

    def __init__(self, value):
        super(FieldDataValue, self).__init__()

        self._value = value
