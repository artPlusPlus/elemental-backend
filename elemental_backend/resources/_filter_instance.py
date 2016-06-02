from ._resource_instance import ResourceInstance
from ._resource_property import ResourceProperty
from ._resource_reference import ResourceReference


class FilterInstance(ResourceInstance):
    """
    Represents a value used to eliminate Content Instances when compared
    to the value of a Content Instance's Attribute Instance.

    A FilterInstance is used by the overall system to create a collection
    of ContentInstances that share commonality. For example, a FilterInstance
    my provide a value for a regular expression that is matched against the
    a 'name' attribute on set of Content Instances.
    """
    @ResourceProperty
    def kind_params(self):
        return self._kind_params

    @kind_params.setter
    def kind_params(self, value):
        if not value:
            value = {}
        elif not isinstance(value, dict):
            msg = (
                'Failed to set kind properties: Value must be a dictionary - '
                'received "{0}"'
            )
            msg = msg.format(value)
            raise ValueError(msg)

        self._kind_params = value

    @ResourceReference
    def view_instance(self):
        return self._id

    def __init__(self, id=None, type_id=None, kind_params=None):
        super(FilterInstance, self).__init__(id=id, type_id=type_id)

        self._kind_params = kind_params or {}
