from elemental_core import NO_VALUE

from ._resource import Resource


class AttributeType(Resource):
    """
    Represents a definition for `AttributeInstances`.

    `AttributeTypes` are referenced by `ContentTypes`.
    """
    @property
    def name(self):
        """
        str: Label identifying the intention of the `AttributeType's` data.
        """
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            value = None
        else:
            value = str(value)

        if value == self._name:
            return

        self._name = value
        # TODO: AttributeType.name changed event

    @property
    def default_value(self):
        """
        When a referring `AttributeInstance` is unset, this value is used.
        """
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        if value == self._default_value:
            return

        self._default_value = value
        # TODO: AttributeType.default_value changed event

    @property
    def kind_id(self):
        """
        str: The Kind backing this `AttributeType`.
        """
        return self._kind_id

    @kind_id.setter
    def kind_id(self, value):
        if value == self._kind_id:
            return

        self._kind_id = value
        # TODO: AttributeType.kind_id changed event

    @property
    def kind_properties(self):
        """
        Dict[str:str]: Data used by the `AttributeType's` Kind.
        """
        return self._kind_properties

    @kind_properties.setter
    def kind_properties(self, value):
        if not value:
            value = {}
        elif not isinstance(value, dict):
            msg = (
                'Failed to set kind properties: Value must be a dictionary - '
                'received "{0}"'
            )
            msg = msg.format(value)
            raise ValueError(msg)

        if value == self._kind_properties:
            return

        self._kind_properties = value
        # TODO: AttributeType.kind_properties changed event

    def __init__(self, id=None, name=None, default_value=NO_VALUE,
                 kind_id=None, kind_properties=None):
        """
        Initializes a new `AttributeType` instance.

        Args:
            id (str or uuid): The unique id of this `AttributeType` instance.
            name (str): A human-friendly label identifying the purpose of the
                data represented by referring `AttributeInstances`.
            default_value: Data used when referring `AttributeInstances` have
                no value set.
            kind_id (str): Identifier resolving to a valid `AttributeKind`.
            kind_properties (Dict[str:str]): Data used by the `AttributeKind`.
        """
        super(AttributeType, self).__init__(id=id)

        self._name = None
        self._default_value = None
        self._kind_id = None
        self._kind_properties = None

        self.name = name
        self.default_value = default_value
        self.kind_id = kind_id
        self.kind_properties = kind_properties or dict()
