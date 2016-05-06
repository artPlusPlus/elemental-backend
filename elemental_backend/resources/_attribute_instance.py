import logging
import weakref
from functools import partial

from elemental_core import NO_VALUE
from elemental_core.util import process_uuid_value

from ._resource import Resource


_LOG = logging.getLogger(__name__)


class AttributeInstance(Resource):
    """
    Represents an instance of an `AttributeType`.

    An AttributeInstance holds value data for an AttributeType relative to
    a ContentInstance.
    """
    @property
    def type_id(self):
        """
        uuid: An Id resolving to an `AttributeType` Resource.
        """
        return self._type_id

    @type_id.setter
    def type_id(self, value):
        try:
            value = process_uuid_value(value)
        except ValueError:
            msg = 'Failed to set type id: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        if value == self._type_id:
            return

        self._type_id = value
        # TODO: AttributeInstance.type_id changed event

    @property
    def value(self):
        """
        Data managed by the `AttributeInstance` instance.

        When `value` is set, an attempt is made to retrieve an `AttributeType`
        resource matching the value of `type_id`. If successful, an attempt
        is made to resolve an `AttributeKind` class matching the value of the
        `AttributeType`'s `kind_id` attribute. If this is also successful,
        the `AttributeKind` will be invoked to process and validate the
        incoming value.

        If any of these fail, the value will still be set. This is to allow
        for the construction of a `Model` instance from persisted data. During
        this process, it is conceivable that the `AttributeType` instance
        may not be loaded yet. In this case, it is desirable that the value
        still load.

        Notes:
            - Perhaps some sort of flag could be implemented to enable/disable
            setting of data when the `AttributeKind` cannot be resolved.
        """
        return self._value

    @value.setter
    def value(self, value):
        attr_type = self.attribute_type

        if attr_type:
            kind = attr_type.kind
            if kind:
                value = kind.process_value(value, **attr_type.kind_properties)
                kind.validate_value(value)
            else:
                msg = (
                    'AttributeInstance "{0}" value set without AttributeKind '
                    'processing or validation: AttributeKind "{1}" from '
                    'AttributeType "{2}" not resolved.'
                )
                msg = msg.format(self.id, attr_type.kind_id, attr_type.id)
                _LOG.warn(msg)
        else:
            msg = (
                'AttributeInstance "{0}" value set without AttributeKind '
                'processing or validation: AttributeType "{1}" not resolved.'
            )
            msg = msg.format(self.id, self.type_id)
            _LOG.debug(msg)

        if value == self._value:
            return

        self._value = value
        # TODO: AttributeInstance.value changed event

    @property
    def source_id(self):
        """
        uuid: An Id resolving to an `AttributeInstance` Resource.

        If `source_id` is valid, the value of this `AttributeInstance` will be
        that of the `AttributeInstance` with the `source_id`.
        """
        return self._source_id

    @source_id.setter
    def source_id(self, value):
        try:
            value = process_uuid_value(value)
        except ValueError:
            msg = 'Failed to set source id: "{0}" is not a valid UUID.'
            msg = msg.format(value)
            raise ValueError(msg)

        if value == self._source_id:
            return

        self._source_id = value
        # TODO: AttributeInstance.source_id changed event

    @property
    def attribute_type(self):
        """
        `AttributeType` instance from which this `AttributeInstance` is "derived".

        Warnings:
            Care should be taken when setting this value. `Model` instances
            use it to provide a callback which will resolve a registered
            `AttributeType` instance when this property is hit. Changes to this
            value are not persisted back to any `Model` instances.

        See Also:
            `AttributeInstance.value`
        """
        result = self._attribute_type or None
        if result and isinstance(result, weakref.ref):
            result = result()
        if result and not isinstance(result, Resource) and callable(result):
            result = result()
        return result

    @attribute_type.setter
    def attribute_type(self, value):
        if not isinstance(value, partial):
            try:
                value = weakref.ref(value)
            except TypeError:
                value = value

        if value != self._attribute_type:
            self._attribute_type = value

    def __init__(self, id=None, type_id=None, value=NO_VALUE, source_id=None):
        """
        Initializes a new `AttributeInstance` instance.

        Args:
            id (str or uuid): The unique id of this `AttributeInstance` instance.
            type_id (str or uuid): A valid id for an `AttributeType` instance.
            value: Data to associate with this `AttributeInstance` instance.
            source_id (str or uuid): A valid id for an `AttributeInstance`
                instance from which this instance's value should be pulled.
        """
        super(AttributeInstance, self).__init__(id=id)

        self._type_id = None
        self._value = None
        self._source_id = None
        self._attribute_type = None

        self.type_id = type_id
        self.value = value
        self.source_id = source_id
