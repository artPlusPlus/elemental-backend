import uuid

from ._util import NO_VALUE


class AttributeInstance(object):
    @property
    def type_id(self):
        return self._type_id

    @property
    def id(self):
        return self._id

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __init__(self, type_id, id=None, value=NO_VALUE):
        super(AttributeInstance, self).__init__()

        self._type_id = type_id
        self._id = id or uuid.uuid4()
        self._value = value
