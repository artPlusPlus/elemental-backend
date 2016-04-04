from ._transaction import Transaction
from ._actions import Actions


class Post(Transaction):
    def __init__(self, resource_type, inbound_format, inbound_payload):
        super(Post, self).__init__(
            Actions.POST, resource_type=resource_type,
            inbound_format=inbound_format, inbound_payload=inbound_payload)
