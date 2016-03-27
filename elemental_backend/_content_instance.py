from ._resource import Resource
from ._util import process_uuid_value, process_uuids_value


class ContentInstance(Resource):
    @property
    def type_id(self):
        return self._type_id

    @type_id.setter
    def type_id(self, value):
        try:
            value = process_uuid_value(value)
        except ValueError:
            msg = 'Failed to set type id: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        if value == self._type_id:
            return

        self._type_id = value
        # TODO: ContentInstance.type_id changed event

    @property
    def attribute_ids(self):
        return self._attribute_ids

    @attribute_ids.setter
    def attribute_ids(self, value):
        try:
            value = process_uuids_value(value)
        except (TypeError, ValueError):
            msg = 'Failed to set attribute ids: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        if value == self._attribute_ids:
            return

        self._attribute_ids = value
        # TODO: ContentInstance.attribute_ids changed event

    def __init__(self, id=None, type_id=None, attribute_ids=None):
        super(ContentInstance, self).__init__(id=id)

        self._type_id = None
        self._attribute_ids = None

        self.type_id = type_id
        self.attribute_ids = attribute_ids
