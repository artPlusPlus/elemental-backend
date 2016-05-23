from elemental_core.util import process_uuid_value, process_uuids_value

from ._resource_instance import ResourceInstance
from ._resource_property import ResourceProperty


class ContentInstance(ResourceInstance):
    """
    Represents a unique collection of `AttributeInstances`.
    """
    @ResourceProperty
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

        self._attribute_ids = value

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

        self.attribute_ids = attribute_ids
