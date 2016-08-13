from ._resource_instance import ResourceInstance
from ._resource_reference import ResourceReference
from ._property_changed_hook import PropertyChangedHook


class SorterInstance(ResourceInstance):
    """
    Represents a value used to sort Content Instances when compared
    to the value of a Content Instance's Attribute Instance.

    A SorterInstance is used by the overall system to organize a collection
    of ContentInstances that share commonality.
    """
    @property
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
        original_value = self._kind_params
        if value != original_value:
            self._kind_params = value
            self._kind_params_changed(self, original_value, value)

    @property
    def kind_params_changed(self):
        return self._kind_params_changed

    @ResourceReference
    def view_instance(self):
        return self._id

    def __init__(self, id=None, type_id=None, kind_params=None):
        super(SorterInstance, self).__init__(id=id, type_id=type_id)

        self._kind_params = {}

        self._kind_params_changed = PropertyChangedHook()

        self.kind_params = kind_params
