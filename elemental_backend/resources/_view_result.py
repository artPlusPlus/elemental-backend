import weakref
import collections

# from elemental_core.util import process_uuid_value

from ._resource import Resource
from ._resource_reference import ResourceReference
from ._property_changed_hook import PropertyChangedHook


class ViewResult(Resource):
    @property
    def content_instance_ids(self):
        return self._content_instance_ids

    @content_instance_ids.setter
    def content_instance_ids(self, value):
        if not value:
            value = tuple()
        elif not isinstance(value, collections.Iterable):
            value = [value]
        value = weakref.WeakSet(value)

        original_value = self._content_instance_ids
        if value != original_value:
            self._content_instance_ids = value
            self._content_instance_ids_changed(self, original_value, value)

    @property
    def content_instance_ids_changed(self):
        return self._content_instance_ids_changed

    @ResourceReference
    def content_instances(self):
        return self._content_instance_ids

    @ResourceReference
    def view_instance(self):
        """
        `ResourceType` instance from which this `ResourceInstance` is "derived".
        """
        return self._id

    def __init__(self, id=None):
        super(ViewResult, self).__init__(id=id)

        # self._view_instance_id = None
        self._content_instance_ids = weakref.WeakSet()

        self._content_instance_ids_changed = PropertyChangedHook()

