from ._resource import Resource
from ._resource_property import ResourceProperty


class ResourceType(Resource):
    @ResourceProperty
    def name(self):
        """
        str: Label identifying the intention of the `AttributeType's` data.
        """
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            value = None
        else:
            value = str(value)

        self._name = value

    def __init__(self, id=None, name=None):
        super(ResourceType, self).__init__(id=id)

        self._name = None

        self.name = name
