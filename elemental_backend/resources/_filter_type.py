from elemental_core.util import process_uuids_value

from ._resource_type import ResourceType
from ._resource_property import ResourceProperty


class FilterType(ResourceType):
    """
    Represents a collection of AttributeIds that should be filtered together.

    Content Instances of various types will have different Attribute Types that
    may represent the same high-level property, such as a name. FilterType's
    role is to represent this high-level association in order to easily filter
    different types of Content Instances using a single dimension.
    """
    @ResourceProperty
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

        self._attribute_type_ids = value

    def __init__(self, id=None, name=None, attribute_type_ids=None):
        super(FilterType, self).__init__(id=id, name=name)

        self._attribute_type_ids = []

        self.attribute_type_ids = attribute_type_ids
