from elemental_core import ElementalBase
from elemental_core.util import process_uuid_value

from ._resource_property import ResourceProperty


class Resource(ElementalBase):
    """
    Base class for content data.
    """
    @ResourceProperty
    def id(self):
        """
        Uniquely identifies a `Resource`.
        """
        return self._id

    @id.setter
    def id(self, value):
        try:
            value = process_uuid_value(value)
        except (TypeError, ValueError):
            msg = 'Failed to set id: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        self._id = value

    def __init__(self, id=None):
        """
        Initializes a new `Resource` instance.

        Args:
            id (str or uuid): The unique id of this `Resource` instance.
        """
        super(Resource, self).__init__()

        self._id = None

        self.id = id
