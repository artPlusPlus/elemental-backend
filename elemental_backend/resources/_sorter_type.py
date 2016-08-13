from elemental_core.util import process_uuids_value

from ._resource_type import ResourceType
from ._resource_reference import ResourceReference
from ._property_changed_hook import PropertyChangedHook


class SorterType(ResourceType):
    """
    Represents a collection of AttributeIds that should be sorted together.

    Content Instances of various types will have different Attribute Types that
    may represent the same high-level property, such as a name. SorterTypes's
    role is to represent this high-level association in order to easily sort
    different types of Content Instances using a single dimension.
    """
    @property
    def attribute_type_ids(self):
        return self._attribute_type_ids

    @attribute_type_ids.setter
    def attribute_type_ids(self, value):
        try:
            value = process_uuids_value(value)
        except (TypeError, ValueError):
            msg = (
                'Failed to set attribute type ids: '
                'Value contains invalid UUID values - {0}'
            )
            msg = msg.format(value)
            raise ValueError(msg)

        original_value = self._attribute_type_ids
        if value != original_value:
            self._attribute_type_ids = value
            self._attribute_type_ids_changed(self, original_value, value)

    @property
    def attribute_type_ids_changed(self):
        return self._attribute_type_ids_changed

    @ResourceReference
    def attribute_types(self):
        return self._attribute_type_ids

    def __init__(self, id=None, name=None, attribute_type_ids=None):
        super(SorterType, self).__init__(id=id, name=name)

        self._attribute_type_ids = []

        self._attribute_type_ids_changed = PropertyChangedHook()

        self.attribute_type_ids = attribute_type_ids
