from ._transaction import Transaction
from ._actions import Actions


class Put(Transaction):
    def __init__(self, resource_id, inbound_format, inbound_payload):
        super(Put, self).__init__(
            Actions.PUT, resource_id=resource_id,
            inbound_format=inbound_format, inbound_payload=inbound_payload)
