from elemental_core.util import process_uuids_value

from ._resource_instance import ResourceInstance
from ._resource_property import ResourceProperty
from ._resource_reference import ResourceReference


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

    @ResourceReference
    def filter_instances(self):
        self._filter_ids

    @ResourceReference
    def result(self):
        return self._id

    def __init__(self, id=None, type_id=None, filter_ids=None, result_id=None):
        super(ViewInstance, self).__init__(id=id, type_id=type_id)

        self._filter_ids = tuple()

        self.filter_ids = filter_ids
        self.result_id = result_id
