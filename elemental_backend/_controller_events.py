class ControllerEvents(object):
    initialized = object()

    transaction_opened = object()
    transaction_succeeded = object()
    transaction_failed = object()
    transaction_closing = object()

    resource_resolved = object()
    resource_not_resolved = object()
    resource_created = object()
    resource_not_created = object()
    resource_registered = object()
    resource_not_registered = object()
    resource_updated = object()
    resource_not_updated = object()
    resource_deregistered = object()
    resource_deleted = object()
    resource_not_deleted = object()
