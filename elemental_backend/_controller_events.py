from enum import Enum


class ControllerEvents(Enum):
    transaction_opened = 1
    transaction_succeeded = 2
    transaction_failed = 3
    transaction_closing = 4

    resource_resolved = 5
    resource_not_resolved = 6
    resource_created = 7
    resource_not_created = 8
    resource_registered = 9
    resource_not_registered = 10
    resource_updated = 11
    resource_not_updated = 12
    resource_deleted = 13
    resource_not_deleted = 14
