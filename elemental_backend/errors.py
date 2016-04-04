import logging
import weakref

_LOG = logging.getLogger(__name__)


class ElementalError(Exception):
    @property
    def message(self):
        return self._message

    def __init__(self, message, inner_error=None):
        self._message = message
        self._inner_error = inner_error

    def __str__(self):
        return self._message


class TransactionError(ElementalError):
    @property
    def transaction(self):
        if self._transaction:
            return self._transaction()
        return self._transaction

    def __init__(self, message, inner_error=None, transaction=None):
        super(TransactionError, self).__init__(
            message, inner_error=inner_error)

        try:
            self._transaction = weakref.ref(transaction)
        except TypeError:
            self._transaction = transaction


class InvalidTransactionAction(TransactionError):
    @property
    def invalid_action(self):
        return self._invalid_action

    def __init__(self, message, inner_error=None, transaction=None,
                 invalid_action=None):
        super(InvalidTransactionAction, self).__init__(
            message, inner_error=inner_error, transaction=transaction)

        self._invalid_action = invalid_action


class DeserializerError(ElementalError):
    @property
    def resource_type(self):
        return self._resource_type

    @property
    def data_format(self):
        return self._data_format

    def __init__(self, message, inner_error=None, resource_type=None,
                 data_format=None):
        super(DeserializerError, self).__init__(
            message, inner_error=inner_error)

        self._resource_type = resource_type
        self._data_format = data_format


class DeserializerNotFoundError(DeserializerError):
    pass


class InvalidDeserializerKeyError(DeserializerError):
    pass


class SerializerError(ElementalError):
    @property
    def resource_type(self):
        return self._resource_type

    @property
    def data_format(self):
        return self._data_format

    def __init__(self, message, inner_error=None, resource_type=None,
                 data_format=None):
        super(SerializerError, self).__init__(
            message, inner_error=inner_error)

        self._resource_type = resource_type
        self._data_format = data_format


class SerializerNotFoundError(SerializerError):
    pass


class InvalidSerializerKeyError(SerializerError):
    pass


class HandlerError(SerializerError):
    pass


class InvalidHandlerKeyError(HandlerError):
    pass


class ResourceTypeError(ElementalError):
    @property
    def resource_type(self):
        return self._resource_type

    def __init__(self, message, inner_error=None, resource_type=None):
        super(ResourceTypeError, self).__init__(
            message, inner_error=inner_error)

        self._resource_type = resource_type


class ResourceTypeNotFoundError(ResourceTypeError):
    pass


class ResourceError(ElementalError):
    @property
    def resource_type(self):
        return self._resource_type

    @property
    def resource_id(self):
        return self._resource_id

    def __init__(self, message, inner_error=None,
                 resource_type=None, resource_id=None):
        super(ResourceError, self).__init__(
            message, inner_error=inner_error)

        self._resource_type = resource_type
        self._resource_id = resource_id


class ResourceNotFoundError(ResourceError):
    pass


class ResourceNotCreatedError(ResourceError):
    pass


class ResourceNotRegisteredError(ResourceError):
    pass


class ResourceCollisionError(ResourceError):
    pass


class ResourceNotDeletedError(ResourceError):
    pass


class ResourceNotReleasedError(ResourceError):
    pass


class ResourceNotUpdatedError(ResourceError):
    pass


class ContentTypeImportError(ElementalError):
    pass


class ContentImportError(ElementalError):
    pass


class AttributeTypeCollisionError(ElementalError):
    pass


class AttributeCollisionError(ElementalError):
    pass


class UnknownAttributeTypeError(ElementalError):
    pass


class ElementalResourceNotFoundError(ElementalError):
    pass


class ContentTypeNotFoundError(ElementalResourceNotFoundError):
    pass


class ContentNotFoundError(ElementalResourceNotFoundError):
    pass
