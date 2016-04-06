from .._util import process_uuid_value


class Resource(object):
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        try:
            value = process_uuid_value(value)
        except (TypeError, ValueError):
            msg = 'Failed to set id: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        if value == self._id:
            return

        self._id = value
        #TODO: Resource.id changed event

    def __init__(self, id=None):
        super(Resource, self).__init__()

        self._id = None

        self.id = id
