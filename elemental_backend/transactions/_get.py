from ._transaction import Transaction
from ._actions import Actions


class Get(Transaction):
    def __init__(self, resource_id, outbound_format=None):
        super(Get, self).__init__(
            Actions.GET, resource_id=resource_id,
            outbound_format=outbound_format)
