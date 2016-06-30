from elemental_core.util import process_uuids_value

from ._resource_type import ResourceType
from ._property_changed_hook import PropertyChangedHook
from ._resource_reference import ResourceReference


class ContentType(ResourceType):
    """
    Represents a collection of `AttributeTypes`.

    A `ContentType` can inherit from other `ContentTypes`.
    """
    @property
    def base_ids(self):
        """
        List[uuid]: A sequence of Ids resolving to other `ContentType` instances.

        `ContentInstances` created from this `ContentType` will have references
        to `AttributeInstances` that were in turn created from all
        `AttributeTypes` found on this `ContentType` and all `ContentTypes`
        identified in `base_ids`.
        """
        return self._base_ids

    @base_ids.setter
    def base_ids(self, value):
        try:
            value = process_uuids_value(value)
        except (ValueError, TypeError):
            msg = (
                'Failed to set base ids: '
                'Value contains invalid UUID values - {0}'
            )
            msg = msg.format(value)
            raise ValueError(msg)

        self._base_ids = value

        original_value = self._base_ids
        if value != original_value:
            self._base_ids = value
            self._base_ids_changed(self, original_value, value)

    @property
    def base_ids_changed(self):
        return self._base_ids_changed

    @base_ids_changed.setter
    def base_ids_changed(self, value):
        if value is not self._base_ids_changed:
            raise TypeError('base_ids_changed cannot be set')

    @property
    def attribute_type_ids(self):
        """
        List[uuid]: A sequence of Ids resolving to `AttributeType` instances.
        """
        return self._attribute_type_ids

    @attribute_type_ids.setter
    def attribute_type_ids(self, value):
        try:
            value = process_uuids_value(value)
        except (TypeError, ValueError):
            msg = (
                'Failed to set attribute type ids: '
                'Value contains invalid UUID values - {0}'
            )
            msg = msg.format(value)
            raise ValueError(msg)

        original_value = self._attribute_type_ids
        if value != original_value:
            self._attribute_type_ids = value
            self._attribute_type_ids_changed(self, original_value, value)

    @property
    def attribute_type_ids_changed(self):
        return self._attribute_type_ids_changed

    @ResourceReference
    def attribute_types(self):
        return self._attribute_type_ids

    @ResourceReference
    def view_types(self):
        return self._id

    def __init__(self, id=None, name=None, base_ids=None,
                 attribute_type_ids=None):
        """
        Initializes a new `ContentType` instance.

        Args:
            id (str or uuid): The unique id of this `ContentType` instance.
            name (str): A human-friendly label identifying the purpose of the
                data represented by referring `AttributeInstances`.
            base_ids (str or List[str]): Ids resolving to valid `ContentType`
                instances.
            attribute_type_ids (str or List[str]): Ids resolving to valid
                `AttributeType` instances.
        """
        super(ContentType, self).__init__(id=id, name=name)

        self._base_ids = None
        self._attribute_type_ids = None

        self._base_ids_changed = PropertyChangedHook()
        self._attribute_type_ids_changed = PropertyChangedHook()

        self.base_ids = base_ids
        self.attribute_type_ids = attribute_type_ids
