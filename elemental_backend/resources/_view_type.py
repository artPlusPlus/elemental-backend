from elemental_core.util import process_uuids_value

from ._resource_type import ResourceType
from ._resource_property import ResourceProperty


class ViewType(ResourceType):
    """
    Represents a data used to aggregate and filter `ContentInstances`.

    A ViewType defines a collection of `ContentTypes` used to generate a base
    set of `ContentInstances`. Additionally, a collection of `FilterTypes` can
    be used to provide an optional means of reducing the base set of
    `ContentInstances`.
    """
    @ResourceProperty
    def content_type_ids(self):
        return self._content_type_ids

    @content_type_ids.setter
    def content_type_ids(self, value):
        try:
            value = process_uuids_value(value)
        except (TypeError, ValueError):
            msg = (
                'Failed to set content type ids: '
                'Value contains invalid UUID values - {0}'
            )
            msg = msg.format(value)
            raise ValueError(msg)

        self._content_type_ids = value

    @ResourceProperty
    def filter_type_ids(self):
        return self._source_content_type_ids

    @filter_type_ids.setter
    def filter_ids(self, value):
        try:
            value = process_uuids_value(value)
        except (TypeError, ValueError):
            msg = (
                'Failed to set filter type ids: '
                'Value contains invalid UUID values - {0}'
            )
            msg = msg.format(value)
            raise ValueError(msg)

        self._filter_type_ids = value

    def __init__(self, id=None, name=None, content_type_ids=None,
                 filter_type_ids=None):
        super(ViewType, self).__init__(id=id, name=name)

        self._content_type_ids = set()
        self._filter_type_ids = []

        self.content_type_ids = content_type_ids
        self.filter_type_ids = filter_type_ids
