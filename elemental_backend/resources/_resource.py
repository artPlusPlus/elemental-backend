from elemental_core import ElementalBase
from elemental_core.util import process_uuid_value

from ._property_changed_hook import PropertyChangedHook


class Resource(ElementalBase):
    """
    Base class for content data.
    """

    @property
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

        original_value = self._id
        if value != original_value:
            self._id = value
            self.id_changed(self, original_value, value)

    @property
    def id_changed(self):
        return self._id_changed

    @id_changed.setter
    def id_changed(self, value):
        if value is not self._id_changed:
            raise TypeError('id_changed cannot be set')

    @id_changed.setter
    def id_changed(self, value):
        if value is not self._id_changed:
            raise TypeError('id_changed cannot be set')

    def __init__(self, id=None):
        """
        Initializes a new `Resource` instance.

        Args:
            id (str or uuid): The unique id of this `Resource` instance.
        """
        super(Resource, self).__init__()

        self._id = None
        self._stale = True

        self._id_changed = PropertyChangedHook()

        self.id = id
