from elemental_core import (
    ElementalBase,
    Hook,
    ValueChangedHookData
)
from elemental_core.util import process_uuid_value


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

        if value == self._id:
            return

        original_value = self._id
        self._id = value

        self._on_id_changed(original_value, value)

    def __init__(self, id=None):
        """
        Initializes a new `Resource` instance.

        Args:
            id (str or uuid): The unique id of this `Resource` instance.
        """
        super(Resource, self).__init__()

        self._id = None

        self.id_changed = Hook()

        self.id = id

    def _on_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self._id_changed(self, data)
