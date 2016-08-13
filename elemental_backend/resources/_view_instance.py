from elemental_core.util import process_uuid_value, process_uuids_value

from ._resource_instance import ResourceInstance
from ._resource_reference import ResourceReference
from ._property_changed_hook import PropertyChangedHook


class ViewInstance(ResourceInstance):
    """
    Represents a stack of `FilterInstances` to be applied against a set of
    `ContentInstances` aggregated by the `ViewInstance's` `ViewType`.
    """
    @property
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

        original_value = self._filter_ids
        if value != original_value:
            self._filter_ids = value
            self._filter_ids_changed(self, original_value, value)

    @property
    def filter_ids_changed(self):
        return self._filter_ids_changed

    @ResourceReference
    def filter_instances(self):
        return self._filter_ids

    @property
    def sorter_ids(self):
        return self._sorter_ids

    @sorter_ids.setter
    def sorter_ids(self, value):
        try:
            value = process_uuids_value(value)
        except (TypeError, ValueError):
            msg = 'Failed to set attribute ids: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        original_value = self._sorter_ids
        if value != original_value:
            self._sorter_ids = value
            self._sorter_ids_changed(self, original_value, value)

    @property
    def sorter_ids_changed(self):
        return self._sorter_ids_changed

    @ResourceReference
    def sorter_instances(self):
        return self._sorter_ids

    @property
    def result_id(self):
        return self._result_id

    @result_id.setter
    def result_id(self, value):
        try:
            value = process_uuid_value(value)
        except (TypeError, ValueError):
            msg = 'Failed to set result id: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        self._result_id = value
        original_value = self._result_id
        if value != original_value:
            self._result_id = value
            self._result_id_changed(self, original_value, value)

    @property
    def result_id_changed(self):
        return self._result_id_changed

    @ResourceReference
    def result(self):
        return self._result_id

    def __init__(self, id=None, type_id=None, filter_ids=None, sorter_ids=None,
                 result_id=None):
        super(ViewInstance, self).__init__(id=id, type_id=type_id)

        self._filter_ids = tuple()
        self._sorter_ids = tuple()
        self._result_id = None

        self._filter_ids_changed = PropertyChangedHook()
        self._sorter_ids_changed = PropertyChangedHook()
        self._result_id_changed = PropertyChangedHook()

        self.filter_ids = filter_ids
        self.sorter_ids = sorter_ids
        self.result_id = result_id
