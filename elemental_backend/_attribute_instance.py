from ._resource import Resource
from ._util import NO_VALUE, process_uuid_value


class AttributeInstance(Resource):
    @property
    def type_id(self):
        return self._type_id

    @type_id.setter
    def type_id(self, value):
        try:
            value = process_uuid_value(value)
        except ValueError:
            msg = 'Failed to set type id: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        if value == self._type_id:
            return

        self._type_id = value
        # TODO: AttributeInstance.type_id changed event

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value == self._value:
            return

        self._value = value
        # TODO: AttributeInstance.value changed event

    def __init__(self, id=None, type_id=None, value=NO_VALUE):
        super(AttributeInstance, self).__init__(id=id)

        self._type_id = None
        self._value = None

        self.type_id = type_id
        self.value = value
