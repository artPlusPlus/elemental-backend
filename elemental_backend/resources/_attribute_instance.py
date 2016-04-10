from ._resource import Resource
from .._util import NO_VALUE, process_uuid_value


class AttributeInstance(Resource):
    """
    Represents an instance of an `AttributeType`.

    An AttributeInstance holds value data for an AttributeType relative to
    a ContentInstance.
    """
    @property
    def type_id(self):
        """
        uuid: An Id resolving to an `AttributeType` Resource.
        """
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
        """
        Data managed by the `AttributeInstance` instance.
        """
        return self._value

    @value.setter
    def value(self, value):
        if value == self._value:
            return

        self._value = value
        # TODO: AttributeInstance.value changed event

    @property
    def source_id(self):
        """
        uuid: An Id resolving to an `AttributeInstance` Resource.

        If `source_id` is valid, the value of this `AttributeInstance` will be
        that of the `AttributeInstance` with the `source_id`.
        """
        return self._source_id

    @source_id.setter
    def source_id(self, value):
        try:
            value = process_uuid_value(value)
        except ValueError:
            msg = 'Failed to set source id: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        if value == self._source_id:
            return

        self._source_id = value
        # TODO: AttributeInstance.source_id changed event

    def __init__(self, id=None, type_id=None, value=NO_VALUE, source_id=None):
        """
        Initializes a new `AttributeInstance` instance.

        Args:
            id (str or uuid): The unique id of this `AttributeInstance` instance.
            type_id (str or uuid): A valid id for an `AttributeType` instance.
            value: Data to associate with this `AttributeInstance` instance.
            source_id (str or uuid): A valid id for an `AttributeInstance`
                instance from which this instance's value should be pulled.
        """
        super(AttributeInstance, self).__init__(id=id)

        self._type_id = None
        self._value = None
        self._source_id = None

        self.type_id = type_id
        self.value = value
        self.source_id = source_id
