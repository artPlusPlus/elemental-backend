import logging


_LOG = logging.getLogger(__name__)


class PeriodicError(Exception):
    pass


class ContentTypeImportError(PeriodicError):
    pass


class ContentImportError(PeriodicError):
    pass


class AttributeTypeCollisionError(PeriodicError):
    pass


class AttributeCollisionError(PeriodicError):
    pass


class UnknownAttributeTypeError(PeriodicError):
    pass


class PeriodicResourceNotFoundError(PeriodicError):
    pass


class ContentTypeNotFoundError(PeriodicResourceNotFoundError):
    pass


class ContentNotFoundError(PeriodicResourceNotFoundError):
    pass
