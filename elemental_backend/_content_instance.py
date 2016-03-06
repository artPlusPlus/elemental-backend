import uuid


class ContentInstance(object):
    @property
    def type_id(self):
        return self._type_id

    @property
    def id(self):
        return self._id

    def __init__(self, type_id, id=None):
        super(ContentInstance, self).__init__()

        self._type_id = type_id
        self._id = id or uuid.uuid4()
