from elemental_core.util import process_uuid_value

from ._resource import Resource
from ._resource_reference import ResourceReference
from ._property_changed_hook import PropertyChangedHook


class ResourceInstance(Resource):
    @property
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

        original_value = self._type_id
        if value != original_value:
            self._type_id = value
            self._type_id_changed(self, original_value, value)

    @property
    def type_id_changed(self):
        return self._type_id_changed

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

        self._type_id_changed = PropertyChangedHook()

        self.type_id = type_id
