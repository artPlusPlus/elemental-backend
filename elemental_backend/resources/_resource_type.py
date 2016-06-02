from ._resource import Resource
from ._resource_property import ResourceProperty
from ._resource_reference import ResourceReference


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

    @ResourceReference
    def resource_instances(self):
        return self._id

    def __init__(self, id=None, name=None):
        super(ResourceType, self).__init__(id=id)

        self._name = None

        self.name = name
