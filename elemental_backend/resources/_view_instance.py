from elemental_core.util import process_uuids_value

from ._resource_instance import ResourceInstance
from ._resource_property import ResourceProperty


class ViewInstance(ResourceInstance):
    """
    Represents a stack of `FilterInstances` to be applied against a set of
    `ContentInstances` aggregated by the `ViewInstance's` `ViewType`.
    """
    @ResourceProperty
    def filter_ids(self):
        return self._filter_ids

    @filter_ids.setter
    def filter_ids(self, value):
        try:
            value = process_uuids_value(value)
        except (TypeError, ValueError):
            msg = 'Failed to set attribute ids: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        self._filter_ids = value

    def __init__(self, id=None, type_id=None):
        super(ViewInstance, self).__init__(id=id, type_id=type_id)

        self._filter_ids = None
