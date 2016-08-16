from elemental_core import NO_VALUE
from elemental_core.util import process_elemental_class_value

from ._resource_type import ResourceType
from ._property_changed_hook import PropertyChangedHook
from ._resource_reference import ResourceReference


class FieldType(ResourceType):
    @property
    def value_resolution_order(self):
        """
        The value resolution order defines how a FieldInstance's final value
        will be computed.

        The value of a field can exist at multiple, developer-defined strata.
        Consider the case where a developer wishes to offer users the ability
        to override default values. `FieldType's` `value_resolution_order`
        provides this ability.

        The `value_resolution_order` defines an ordered collection of keys
        which can be used to look up and store value data. In the example above,
        a sequence of two keys would be needed, [`default`, `user`]. When a
        value is request for a `FieldInstance`, the `user` key is checked first.
        If its value is `NO_VALUE`, the value associated with `default` will
        be used.

        Returns:
            A list of objects.
        """
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
        """
        Provides a mechanism for reacting to changes to the value resolution
        order.

        Returns:
            A `PropertyChangedHook`
        """
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
        """
        Provides a mechanism for reacting to changes to the default value.

        Returns:
            A `PropertyChangedHook`
        """
        return self._default_value_changed

    @property
    def false_value(self):
        """
        When the data of a new value tests false, this value will be used
        instead.

        Returns:
            An object.
        """
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
        """
        Provides a mechanism for reacting to changes to the false value.

        Returns:
            A `PropertyChangedHook`.
        """
        return self._false_value_changed

    @property
    def kind_id(self):
        """
        str: The Kind backing this `AttributeType`.
        """
        return self._kind_id

    @kind_id.setter
    def kind_id(self, value):
        original_value = self._kind_id
        if value != original_value:
            self._kind_id = value
            self._kind_id_changed(self, original_value, value)

    @property
    def kind_id_changed(self):
        return self._kind_id_changed

    @property
    def kind_properties(self):
        """
        Dict[str:str]: Data used by the `AttributeType's` Kind.
        """
        return self._kind_properties

    @kind_properties.setter
    def kind_properties(self, value):
        if not value:
            value = {}
        elif not isinstance(value, dict):
            msg = (
                'Failed to set kind properties: Value must be a dictionary - '
                'received "{0}"'
            )
            msg = msg.format(value)
            raise ValueError(msg)

        original_value = self._kind_properties
        if value != original_value:
            self._kind_properties = value
            self._kind_properties_changed(self, original_value, value)

    @property
    def kind_properties_changed(self):
        return self._kind_properties_changed

    @property
    def kind(self):
        """
        The kind represents the underlying type of the value data
        (string, float, etc).

        Returns:
            An `elemental-kinds` class.
        """
        if not self.kind_id:
            return None

        return process_elemental_class_value(self.kind_id)

    @ResourceReference
    def filter_types(self):
        """
        List of `FilterType`s that reference this `AttributeType`.
        """
        return self._id

    @ResourceReference
    def sorter_types(self):
        """
        List of `SorterType`s that reference this `AttributeType`.
        """
        return self._id

    def __init__(self, id=None, name=None, value_resolution_order=None,
                 default_value=NO_VALUE, false_value=NO_VALUE,
                 kind_id=None, kind_properties=None):
        super(FieldType, self).__init__(id=id, name=name)

        self._value_resolution_order = None
        self._value_resolution_order_changed = PropertyChangedHook()

        self._default_value = NO_VALUE
        self._default_value_changed = PropertyChangedHook()

        self._false_value = NO_VALUE
        self._false_value_changed = PropertyChangedHook()

        self._kind_id = None
        self._kind_id_changed = PropertyChangedHook()

        self._kind_properties = None
        self._kind_properties_changed = PropertyChangedHook()

        self.value_resolution_order = value_resolution_order or tuple()
        self.default_value = default_value
        self.false_value = false_value
        self.kind_id = kind_id
        self.kind_properties = kind_properties or dict()
