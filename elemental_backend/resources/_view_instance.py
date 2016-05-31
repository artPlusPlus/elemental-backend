import weakref
from functools import partial

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

    @property
    def content_instances(self):
        """
        `ContentInstance`s matching the filters of this view.

        Warnings:
            Care should be taken when setting this value. `Model` instances
            use it to provide a callback which will resolve list of
            `ContentInstance` instances when this property is hit.
            Changes to this value are not persisted back to any `Model`
            instances.

        See Also:
            `AttributeInstance.value`
        """
        result = self._content_instances or None
        if isinstance(result, (weakref.ref, partial)):
            result = result()
        return result

    @content_instances.setter
    def content_instances(self, value):
        if not isinstance(value, partial):
            try:
                value = weakref.ref(value)
            except TypeError:
                value = value

        self._content_instances = value

    def __init__(self, id=None, type_id=None, filter_ids=None):
        super(ViewInstance, self).__init__(id=id, type_id=type_id)

        self._filter_ids = None
        self._content_instances = None

        self.filter_ids = filter_ids
