import weakref

from elemental_core.util import process_uuid_value

from ._resource import Resource
from ._resource_property import ResourceProperty
from ._resource_reference import ResourceReference


class ViewResult(Resource):
    @ResourceProperty
    def content_instance_ids(self):
        return self._content_instance_ids

    @content_instance_ids.setter
    def content_instance_ids(self, value):
        self._content_instance_ids = value

    @ResourceProperty
    def view_instance_id(self):
        return self._view_instance_id

    @view_instance_id.setter
    def view_instance_id(self, value):
        try:
            value = process_uuid_value(value)
        except ValueError:
            msg = 'Failed to set type id: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        self._view_instance_id = value

    @ResourceReference
    def view_instance(self):
        """
        `ResourceType` instance from which this `ResourceInstance` is "derived".
        """
        self._view_instance_id

    def __init__(self, id=None):
        super(ViewResult, self).__init__(id=id)

        self._view_instance_id = None
        self._content_instance_ids = weakref.WeakSet()
