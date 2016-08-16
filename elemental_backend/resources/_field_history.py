from elemental_core import NO_VALUE


class FieldHistory(object):
    @property
    def current(self):
        try:
            return self._values[self._cursor]
        except IndexError:
            return NO_VALUE

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        if value == self._cursor:
            return

        if len(self._values) > value >= len(self._values) * -1:
            self._cursor = value
        else:
            msg = 'Cursor out of range.'
            raise ValueError(msg)

    def __init__(self):
        self._cursor = -1
        self._values = []

    def append(self, value):
        if self._cursor != -1:
            self._values = self._values[:self._cursor]
        self._values.append(value)

    def squash(self, start=0, end=-1):
        if len(self._values) >= start:
            msg = 'start out of range.'
            raise ValueError(msg)
        elif len(self._values) >= end:
            msg = 'end out of range.'
            raise ValueError(msg)

        self._values = self._values[start:end]
