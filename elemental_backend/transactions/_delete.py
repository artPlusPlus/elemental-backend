from ._transaction import Transaction
from ._actions import Actions


class Delete(Transaction):
    def __init__(self, resource_id):
        super(Delete, self).__init__(Actions.DELETE,
                                     resource_id=resource_id)
