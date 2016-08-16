from elemental_core import NO_VALUE

from elemental_backend.resources import ResourceType
from elemental_backend.resources._property_changed_hook import PropertyChangedHook


class FieldType(ResourceType):
    @property
    def value_resolution_order(self):
        return self._value_resolution_order

    @value_resolution_order.setter
    def value_resolution_order(self, value):
        if not value or not isinstance(value, (list, tuple)):
            msg = 'Value Resolution Order must be a list or tuple.'
            raise ValueError(msg)

        original_value = self._value_resolution_order
        if value != original_value:
            self._value_resolution_order = value
            self._value_resolution_order_changed(self, original_value, value)

    @property
    def value_resolution_order_changed(self):
        return self._value_resolution_order_changed

    @property
    def default_value(self):
        """
        str: Label identifying the intention of the `AttributeType's` data.
        """
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        if not value:
            value = None
        else:
            value = str(value)

        original_value = self._default_value
        if value != original_value:
            self._default_value = value
            self._default_value_changed(self, original_value, value)

    @property
    def default_value_changed(self):
        return self._default_value_changed

    @property
    def false_value(self):
        return self._false_value

    @false_value.setter
    def false_value(self, value):
        if not value:
            value = None
        else:
            value = str(value)

        original_value = self._name
        if value != original_value:
            self._false_value = value
            self._false_value_changed(self, original_value, value)

    @property
    def false_value_changed(self):
        return self._false_value_changed

    def __init__(self, id=None, name=None, value_resolution_order=None,
                 default_value=NO_VALUE, false_value=NO_VALUE):
        super(FieldType, self).__init__(id=id, name=name)

        self._value_resolution_order = None
        self._value_resolution_order_changed = PropertyChangedHook()

        self._default_value = NO_VALUE
        self._default_value_changed = PropertyChangedHook()

        self._false_value = NO_VALUE
        self._false_value_changed = PropertyChangedHook()

        self.value_resolution_order = value_resolution_order or tuple()
        self.default_value = default_value
        self.false_value = false_value

    def process_value(self, value):
        raise NotImplementedError()
