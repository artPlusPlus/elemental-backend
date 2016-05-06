import uuid

from elemental_core import ElementalBase
from elemental_core.util import (
    process_uuid_value,
    process_elemental_class_value,
    process_data_format_value
)


class Transaction(ElementalBase):
    """
    A Transaction represents an atomic operation on a single `Resource`.

    A `Transaction` manages the state of an operation as the backend executes
    it. It handles how and to what the backend will operate on.
    """
    @property
    def id(self):
        """
        Unique identifier for the Transaction.
        """
        return self._id

    @property
    def super_id(self):
        """
        Unique identifier of a higher-order Transaction.

        A batch `Transaction` could be made up of multiple smaller
        `Transactions`. If any of the smaller `Transactions` fails, the
        entire batch `Transaction` would be rolled back.
        """
        return self._super_id

    @property
    def action(self):
        """
        What the Transaction wishes to accomplish.
        """
        return self._action

    @property
    def resource_type(self):
        """
        The class of the `Resource` the `Transaction` is targeting.
        """
        if self.target_resource:
            return type(self.target_resource)
        return self._resource_type

    @property
    def resource_id(self):
        """
        The unique ID of the `Resource` the `Transaction` is targeting.
        """
        if self.target_resource:
            return self.target_resource.id
        return self._resource_id

    @property
    def inbound_format(self):
        """
        The format of any data destined for the backend.
        """
        return self._inbound_format

    @inbound_format.setter
    def inbound_format(self, value):
        value = process_data_format_value(value)
        if value == self._inbound_format:
            return

        self._inbound_format = value
        # TODO: Inbound Format changed event?

    @property
    def inbound_payload(self):
        """
        Any data destined for the backend.
        """
        return self._inbound_payload

    @property
    def outbound_format(self):
        """
        The format to which the target `Resource` should be formatted.
        """
        return self._outbound_format

    @outbound_format.setter
    def outbound_format(self, value):
        value = process_data_format_value(value)
        if value == self._outbound_format:
            return

        self._outbound_format = value
        # TODO: Outbound Format changed event?

    @property
    def data(self):
        """
        Dictionary containing site specific data.
        """
        return self._data

    @property
    def errors(self):
        """
        Contains any errors encountered during processing by the backend.
        """
        return self._errors

    def __init__(self, action, resource_type=None, resource_id=None,
                 super_id=None, inbound_format=None, inbound_payload=None,
                 outbound_format=None):
        """
        Constructor for a Transaction instance.

        Args:
            action (Actions): What the Transaction will do.
            resource_type Optional(Resource): The type of the target `Resource`.
            resource_id Optional(str or uuid): The ID of the target `Resource`.
            super_id Optional(str or uuid): The ID of a batch `Transaction`.
            inbound_format Optional(str): The format of the data contained in
                `inbound_payload`.
            inbound_payload Optional(str): Data intended to be processed and
                persisted by the backend.
            outbound_format Optional(str): The format to which the target
                `Resource` will be formatted should the `Transaction` succeed.
        """
        self._id = uuid.uuid4()
        self._action = action
        self._resource_type = process_elemental_class_value(resource_type)
        self._resource_id = process_uuid_value(resource_id)
        self._super_id = process_uuid_value(super_id)
        self._inbound_format = None
        self._inbound_payload = inbound_payload
        self.inbound_deserializer = None
        self._outbound_format = None
        self.outbound_payload = None
        self.outbound_serializer = None

        self.target_resource = None
        self._data = {}
        self._errors = []

        self.outbound_format = outbound_format
        self.inbound_format = inbound_format

    def _drop_handler(self, ref):
        self._handler = None
