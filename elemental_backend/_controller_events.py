from enum import Enum


class ControllerEvents(Enum):
    initialized = 1

    transaction_opened = 2
    transaction_succeeded = 3
    transaction_failed = 4
    transaction_closing = 5

    resource_resolved = 6
    resource_not_resolved = 7
    resource_created = 8
    resource_not_created = 9
    resource_registered = 10
    resource_not_registered = 11
    resource_updated = 12
    resource_not_updated = 13
    resource_deregistered = 14
    resource_deleted = 15
    resource_not_deleted = 16
