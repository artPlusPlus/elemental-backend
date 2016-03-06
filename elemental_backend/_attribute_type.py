import uuid

from ._util import NO_VALUE


class AttributeType(object):
    @property
    def kind_id(self):
        return self._kind_id

    @property
    def id(self):
        return self._id

    @property
    def default_value(self):
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        self._default_value = value

    def __init__(self, kind_id, name, id=None, default_value=NO_VALUE,
                 kind_properties=None):
        super(AttributeType, self).__init__()

        self._kind_id = kind_id
        self._id = id or uuid.uuid4()
        self._name = name
        self._default_value = default_value
        self._kind_properties = kind_properties or dict()
