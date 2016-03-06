import uuid


class ContentType(object):
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def base_ids(self):
        return self._base_ids[:]

    def __init__(self, name, id=None, base_ids=None):
        super(ContentType, self).__init__()

        self._id = id or uuid.uuid4()
        self._name = name

        self._base_ids = base_ids or tuple()
        try:
            self._base_ids = tuple(base_ids)
        except TypeError:
            self._base_ids = tuple(self._base_ids, )

