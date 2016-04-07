from ._transaction import Transaction
from ._actions import Actions


class Put(Transaction):
    """
    Convenience interface for a Put operation.

    A Put Transaction modifies an existing `Resource` managed by the backend.
    Put Transactions are idempotent; the same data will result in the state
    of the `Resource` changing 0 (if the data matches the current state) or 1
    times.
    """
    def __init__(self, resource_id, inbound_format, inbound_payload):
        """
        Constructor for a Put Transaction instance.

        Args:
            resource_id (str or UUID): The Id of `Resource` to modify.
            inbound_format (str): The format of the serialized `Resource` data.
            inbound_payload (str): Data representing the new `Resource` state.
        """
        super(Put, self).__init__(
            Actions.PUT, resource_id=resource_id,
            inbound_format=inbound_format, inbound_payload=inbound_payload)
