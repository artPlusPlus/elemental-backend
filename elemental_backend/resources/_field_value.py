import time

from elemental_core import NO_VALUE, Hook


class FieldValue(object):
    @property
    def value(self):
        raise NotImplementedError()

    @property
    def is_dirty(self):
        return self._is_dirty

    @property
    def was_dirtied(self):
        return self._was_dirtied

    def __init__(self):
        self._timestamp = time.clock()
        self._value = NO_VALUE
        self._is_dirty = True
        self._was_dirtied = Hook()

    def dirty(self):
        self._is_dirty = True
        self._was_dirtied(self)

    def __repr__(self):
        result = '<{0} object at {1}, value: {2}, is_dirty: {3}>'
        result = result.format(__name__, id(self), self._value, self._is_dirty)
        return result
