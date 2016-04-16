from elemental_core.util import process_uuids_value

from ._resource import Resource


class ContentType(Resource):
    """
    Represents a collection of `AttributeTypes`.

    A `ContentType` can inherit from other `ContentTypes`.
    """
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

        if value == self._name:
            return

        self._name = value
        # TODO: ContentType.name changed event

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

        if value == self._base_ids:
            return

        self._base_ids = value
        # TODO: ContentType.base_ids changed event

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

        if value == self._attribute_type_ids:
            return

        self._attribute_type_ids = value
        # TODO: ContentType.attribute_type_ids changed event

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
        super(ContentType, self).__init__(id=id)

        self._name = None
        self._base_ids = None
        self._attribute_type_ids = None

        self.name = name
        self.base_ids = base_ids
        self.attribute_type_ids = attribute_type_ids
