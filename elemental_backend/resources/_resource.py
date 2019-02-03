from elemental_core import (
    ElementalBase,
    Hook,
    ValueChangedHookData,
    NO_VALUE
)
from elemental_core.util import process_uuid_value


class Resource(ElementalBase):
    """
    Base class for content data.
    """
    id_changed = Hook()

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

        self.id = id

    @classmethod
    def iter_hooks(cls):
        pass

    @classmethod
    def iter_forward_references(cls):
        pass

    def _on_id_changed(self, original_value, current_value):
        data = ValueChangedHookData(original_value, current_value)
        self._id_changed(self, data)

    def _set_data_id(
            self, value, data_id_attr, data_ref,
            content_changed_handler, on_data_id_changed, on_data_content_changed):
        value = process_uuid_value(value)

        if value == getattr(self, data_id_attr):
            return

        original_data_content = self._disconnect_from_data_ref(
            data_ref, content_changed_handler)

        original_value = getattr(self, data_id_attr)
        setattr(self, data_id_attr, value)

        current_data_content = self._connect_to_data_ref(
            data_ref, content_changed_handler)

        on_data_id_changed(original_value, value)
        if original_data_content != current_data_content:
            on_data_content_changed(original_data_content, current_data_content)

    @staticmethod
    def _disconnect_from_data_ref(ref, content_changed_handler):
        data_content = NO_VALUE
        data = ref()
        if data:
            data.content_changed -= content_changed_handler
            data_content = data.content

        return data_content

    @staticmethod
    def _connect_to_data_ref(ref, content_changed_handler):
        data_content = NO_VALUE
        data = ref()
        if data:
            data.content_changed += content_changed_handler
            data_content = data.content

        return data_content
