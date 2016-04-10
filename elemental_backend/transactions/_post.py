from ._transaction import Transaction
from ._actions import Actions


class Post(Transaction):
    """
    Convenience interface for a Post operation.

    A Post Transaction creates a new `Resource` managed by the backend.
    Post Transactions are not idempotent; the same data will always create a
    new `Resource`.
    """
    def __init__(self, resource_type, inbound_format, inbound_payload):
        """
        Constructor for a Post Transaction instance.

        Args:
            resource_type (Resource): The type of `Resource` to create.
            inbound_format (str): The format of the serialized `Resource` data.
            inbound_payload (str): Data representing the new `Resource`.
        """
        super(Post, self).__init__(
            Actions.POST, resource_type=resource_type,
            inbound_format=inbound_format, inbound_payload=inbound_payload)
