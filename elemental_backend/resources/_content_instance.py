from elemental_core.util import process_uuids_value

from ._resource_instance import ResourceInstance
from ._resource_reference import ResourceReference
from ._property_changed_hook import PropertyChangedHook


class ContentInstance(ResourceInstance):
    """
    Represents a unique collection of `AttributeInstances`.
    """
    @property
    def attribute_ids(self):
        """
        List[uuid]: A sequence of Ids resolving to valid `AttributeInstance` Resources.
        """
        return self._attribute_ids

    @attribute_ids.setter
    def attribute_ids(self, value):
        try:
            value = process_uuids_value(value)
        except (TypeError, ValueError):
            msg = 'Failed to set attribute ids: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        original_value = self._attribute_ids
        if value != original_value:
            self._attribute_ids = value
            self._attribute_ids_changed(self, original_value, value)

    @property
    def attribute_ids_changed(self):
        return self._attribute_ids_changed

    @ResourceReference
    def attributes(self):
        return self._attribute_ids

    def __init__(self, id=None, type_id=None, attribute_ids=None):
        """
        Initializes a new `ContentInstance` instance.

        Args:
            id (str or uuid): The unique id of this `ContentInstance` instance.
            type_id (str or uuid): A valid id for an `ContentType` instance.
            attribute_ids (List[str or uuid]): A sequence of valid
                `AttributeInstances` Ids.
        """
        super(ContentInstance, self).__init__(id=id, type_id=type_id)

        self._attribute_ids = None

        self._attribute_ids_changed = PropertyChangedHook()

        self.attribute_ids = attribute_ids
