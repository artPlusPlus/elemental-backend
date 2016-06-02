from elemental_core import NO_VALUE
from elemental_core.util import process_elemental_class_value
import elemental_kinds  # Not directly used, allows classes to be resolved later

from ._resource_type import ResourceType
from ._resource_property import ResourceProperty
from ._resource_reference import ResourceReference


class AttributeType(ResourceType):
    """
    Represents a definition for `AttributeInstances`.

    `AttributeTypes` are referenced by `ContentTypes`.
    """
    @ResourceProperty
    def default_value(self):
        """
        When a referring `AttributeInstance` is unset, this value is used.
        """
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        self._default_value = value

    @ResourceProperty
    def kind_id(self):
        """
        str: The Kind backing this `AttributeType`.
        """
        return self._kind_id

    @kind_id.setter
    def kind_id(self, value):
        self._kind_id = value

    @ResourceProperty
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

        self._kind_properties = value

    @property
    def kind(self):
        if not self.kind_id:
            return None

        return process_elemental_class_value(self.kind_id)

    @ResourceReference
    def filter_types(self):
        """
        List of `FilterType`s that reference this `AttributeType`.
        """
        self._id

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
        super(AttributeType, self).__init__(id=id, name=name)

        self._default_value = None
        self._kind_id = None
        self._kind_properties = None

        self.default_value = default_value
        self.kind_id = kind_id
        self.kind_properties = kind_properties or dict()
