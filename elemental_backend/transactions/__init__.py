"""
Transactions are the primary means of interfacing with a backend.

A Transaction `represents` an atomic operation on a single `Resource`.
The `elemental-backend` provides a RESTful interface, which is reflected in
the available `Transactions`.
"""

from ._actions import Actions
from ._transaction import Transaction
from ._get import Get
from ._put import Put
from ._post import Post
from ._delete import Delete
