import weakref
from functools import partial

from elemental_core.util import process_uuid_value

from ._resource import Resource
from ._resource_property import ResourceProperty
from ._resource_reference import ResourceReference


class ResourceInstance(Resource):
    @ResourceProperty
    def type_id(self):
        """
        uuid: An Id resolving to an `AttributeType` Resource.
        """
        return self._type_id

    @type_id.setter
    def type_id(self, value):
        try:
            value = process_uuid_value(value)
        except ValueError:
            msg = 'Failed to set type id: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        self._type_id = value

    @ResourceReference
    def type(self):
        """
        `ResourceType` instance from which this `ResourceInstance` is "derived".

        Warnings:
            Care should be taken when setting this value. `Model` instances
            use it to provide a callback which will resolve a registered
            `ResourceType` instance when this property is hit. Changes to this
            value are not persisted back to any `Model` instances.
        """
        return self._type_id

    def __init__(self, id=None, type_id=None):
        super(ResourceInstance, self).__init__(id=id)

        self._type_id = None
        self._type = None

        self.type_id = type_id
