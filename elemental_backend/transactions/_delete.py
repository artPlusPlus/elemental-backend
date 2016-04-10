from ._transaction import Transaction
from ._actions import Actions


class Delete(Transaction):
    """
    Convenience interface for a Delete operation.

    A Delete Transaction removes a `Resource` and all references from the backend.
    """
    def __init__(self, resource_id):
        """
        Constructor for a Delete Transaction instance.

        Args:
            resource_id (str or UUID): The Id of the `Resource` to delete.
        """
        super(Delete, self).__init__(Actions.DELETE,
                                     resource_id=resource_id)
