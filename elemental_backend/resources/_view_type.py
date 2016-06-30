from elemental_core.util import process_uuids_value

from ._resource_type import ResourceType
from ._resource_reference import ResourceReference
from ._property_changed_hook import PropertyChangedHook


class ViewType(ResourceType):
    """
    Represents a data used to aggregate and filter `ContentInstances`.

    A ViewType defines a collection of `ContentTypes` used to generate a base
    set of `ContentInstances`. Additionally, a collection of `FilterTypes` can
    be used to provide an optional means of reducing the base set of
    `ContentInstances`.
    """
    @property
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

        original_value = self._content_type_ids
        if value != original_value:
            self._content_type_ids = value
            self._content_type_ids_changed(self, original_value, value)

    @property
    def content_type_ids_changed(self):
        return self._content_type_ids_changed

    @ResourceReference
    def content_types(self):
        return self._content_type_ids

    @property
    def filter_type_ids(self):
        return self._filter_type_ids

    @filter_type_ids.setter
    def filter_type_ids(self, value):
        try:
            value = process_uuids_value(value)
        except (TypeError, ValueError):
            msg = (
                'Failed to set filter type ids: '
                'Value contains invalid UUID values - {0}'
            )
            msg = msg.format(value)
            raise ValueError(msg)

        original_value = self._filter_type_ids
        if value != original_value:
            self._filter_type_ids = value
            self._filter_type_ids_changed(self, original_value, value)

    @property
    def filter_type_ids_changed(self):
        return self._filter_type_ids_changed

    @ResourceReference
    def filter_types(self):
        return self._filter_type_ids

    @ResourceReference
    def content_instances(self):
        return self._id

    def __init__(self, id=None, name=None, content_type_ids=None,
                 filter_type_ids=None):
        super(ViewType, self).__init__(id=id, name=name)

        self._content_type_ids = set()
        self._filter_type_ids = []

        self._content_type_ids_changed = PropertyChangedHook()
        self._filter_type_ids_changed = PropertyChangedHook()

        self.content_type_ids = content_type_ids
        self.filter_type_ids = filter_type_ids
