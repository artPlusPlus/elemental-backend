from ._resource import Resource
from ._resource_reference import ResourceReference
from ._property_changed_hook import PropertyChangedHook


class ResourceType(Resource):
    @property
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

        original_value = self._name
        if value != original_value:
            self._name = value
            self._name_changed(self, original_value, value)

    @property
    def name_changed(self):
        return self._name_changed

    @ResourceReference
    def resource_instances(self):
        return self._id

    def __init__(self, id=None, name=None):
        super(ResourceType, self).__init__(id=id)

        self._name = None
        self._name_changed = PropertyChangedHook()

        self.name = name
