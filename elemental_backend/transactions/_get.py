from ._transaction import Transaction
from ._actions import Actions


class Get(Transaction):
    """
    Convenience interface for a Get operation.

    A Get Transaction retrieves the current state of a `Resource` from the backend.
    """
    def __init__(self, resource_id, outbound_format=None):
        """
        Constructor for a Get Transaction instance.

        Args:
            resource_id (str or UUID): The Id of the `Resource` to retrieve.
            outbound_format Optional(str): The format in which to serialize
                the retrieved `Resource` data. If `None`, no serialization
                will occur. Default is `None`.
        """
        super(Get, self).__init__(
            Actions.GET, resource_id=resource_id,
            outbound_format=outbound_format)
