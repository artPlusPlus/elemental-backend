from ._resource import Resource
from .._util import process_uuids_value


class ContentType(Resource):
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            value = None
        else:
            value = str(value)

        if value == self._name:
            return

        self._name = value
        # TODO: ContentType.name changed event

    @property
    def base_ids(self):
        return self._base_ids

    @base_ids.setter
    def base_ids(self, value):
        try:
            value = process_uuids_value(value)
        except (ValueError, TypeError):
            msg = (
                'Failed to set base ids: '
                'Value contains invalid UUID values - {0}'
            )
            msg = msg.format(value)
            raise ValueError(msg)

        if value == self._base_ids:
            return

        self._base_ids = value
        # TODO: ContentType.base_ids changed event

    @property
    def attribute_type_ids(self):
        return self._attribute_type_ids

    @attribute_type_ids.setter
    def attribute_type_ids(self, value):
        try:
            value = process_uuids_value(value)
        except (TypeError, ValueError):
            msg = (
                'Failed to set attribute type ids: '
                'Value contains invalid UUID values - {0}'
            )
            msg = msg.format(value)
            raise ValueError(msg)

        if value == self._attribute_type_ids:
            return

        self._attribute_type_ids = value
        # TODO: ContentType.attribute_type_ids changed event

    def __init__(self, id=None, name=None, base_ids=None,
                 attribute_type_ids=None):
        super(ContentType, self).__init__(id=id)

        self._name = None
        self._base_ids = None
        self._attribute_type_ids = None

        self.name = name
        self.base_ids = base_ids
        self.attribute_type_ids = attribute_type_ids
