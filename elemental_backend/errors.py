import logging
import weakref
import traceback
import sys

_LOG = logging.getLogger(__name__)


class ElementalError(Exception):
    """
    Base class for Elemental exceptions.
    """

    @property
    def message(self):
        """
        str: Human readable string describing the exception.
        """
        return self._message

    @property
    def inner_error(self):
        """
        Exception: Exception instance that caused this exception.
        """
        return self._inner_error

    @property
    def traceback(self):
        """
        str: Frame where inner_error was raised.
        """
        if self._inner_error:
            return self._traceback
        return None

    def __init__(self, message, inner_error=None):
        """
        Initializes a new `ElementalError` instance.

        Args:
            message (str): Human readable string describing the exception.
            inner_error (Optional[Exception]): Exception instance that caused
                this exception.
        """
        self._message = message
        self._inner_error = inner_error
        self._traceback = traceback.format_tb(sys.exc_info()[-1])

    def __str__(self):
        if self._inner_error:
            return '{0}\n{1}'.format(self._message, self.traceback)
        return self._message


class TransactionError(ElementalError):
    """
    Base class for Errors that occur during the processing of a `Transaction`.
    """

    @property
    def transaction(self):
        """
        Transaction: The `Transaction` instance being processed when the
            Exception was raised.

        Internally, the `Transaction` is weakly referenced.
        """
        if isinstance(self._transaction, weakref.ref):
            return self._transaction()
        return self._transaction

    def __init__(self, message, inner_error=None, transaction=None):
        """
        Initializes a new `TransactionError` instance.

        Args:
            message (str): Human readable string describing the exception.
            inner_error (Optional[Exception]): Exception instance that caused
                this exception.
            transaction (Optional[Transaction]): The `Transaction` instance
                being processed when the Exception was raised.
        """
        super(TransactionError, self).__init__(
            message, inner_error=inner_error)

        try:
            self._transaction = weakref.ref(transaction)
        except TypeError:
            self._transaction = transaction


class InvalidTransactionAction(TransactionError):
    """
    Raised when processing is attempted on a `Transaction` without a valid
        `Action` value.
    """

    @property
    def invalid_action(self):
        """
        `Transactions` must contain a valid `Action`.
        """
        return self._invalid_action

    def __init__(self, message, inner_error=None, transaction=None,
                 invalid_action=None):
        """
        Initializes a new `InvalidTransactionAction` instance.

        Args:
            message (str): Human readable string describing the exception.
            inner_error (Optional[Exception]): Exception instance that caused
                this exception.
            transaction (Optional[Transaction]): The `Transaction` instance
                being processed when the Exception was raised.
            invalid_action (Optional[Action]): The value as it was retrieved
                from the `Transaction`.
        """
        super(InvalidTransactionAction, self).__init__(
            message, inner_error=inner_error, transaction=transaction)

        self._invalid_action = invalid_action


class DeserializerError(ElementalError):
    """
    Base class for Errors that relate to deserialization.
    """

    @property
    def resource_type(self):
        """
        The type of resource being deserialized.
        """
        return self._resource_type

    @property
    def data_format(self):
        """
        The format to deserialize from.
        """
        return self._data_format

    def __init__(self, message, inner_error=None, resource_type=None,
                 data_format=None):
        """
        Initializes a new DeserializerError instance.

        Args:
            message (str): Human readable string describing the exception.
            inner_error (Optional[Exception]): Exception instance that caused
                this exception.
            resource_type (Resource): The type of Resource being deserialized.
            data_format (str): The format to deserialize from.
        """
        super(DeserializerError, self).__init__(
            message, inner_error=inner_error)

        self._resource_type = resource_type
        self._data_format = data_format


class DeserializerNotFoundError(DeserializerError):
    """
    Raised when a deserializer matching the `resource_type` and `data_format`
        cannot be found.
    """
    pass


class InvalidDeserializerKeyError(DeserializerError):
    """
    Raised when values representing a `Resource` and data format cannot be
        processed into a valid key for resolving a deserializer.
    """
    pass


class SerializerError(ElementalError):
    """
    Base class for Errors that relate to serialization.
    """
    @property
    def resource_type(self):
        """
        The type of resource being serialized.
        """
        return self._resource_type

    @property
    def data_format(self):
        """
        The format to serialize to.
        """
        return self._data_format

    def __init__(self, message, inner_error=None, resource_type=None,
                 data_format=None):
        """
        Initializes a new SerializerError instance.

        Args:
            message (str): Human readable string describing the exception.
            inner_error (Optional[Exception]): Exception instance that caused
                this exception.
            resource_type (Resource): The type of Resource being serialized.
            data_format (str): The format to serialize to.
        """
        super(SerializerError, self).__init__(
            message, inner_error=inner_error)

        self._resource_type = resource_type
        self._data_format = data_format


class SerializerNotFoundError(SerializerError):
    """
    Raised when a serializer matching the `resource_type` and `data_format`
        cannot be found.
    """
    pass


class InvalidSerializerKeyError(SerializerError):
    """
    Raised when values representing a `Resource` and data format cannot be
        processed into a valid key for resolving a serializer.
    """
    pass


class HandlerError(SerializerError):
    """
    Base class for Errors relating to Handler registration and invocation.
    """
    pass


class InvalidHandlerKeyError(HandlerError):
    """
    Raised when values representing a `ControllerEvent`, `Action`, and
        `Resource` type cannot be processed into a valid key for resolving a
        handler.
    """
    pass


class ResourceError(ElementalError):
    """
    Base class for Errors relating to Resources.
    """

    @property
    def resource_type(self):
        """
        Resource: The type of the problematic `Resource` instance.
        """
        return self._resource_type

    @property
    def resource_id(self):
        """
        uuid: The id of the problematic `Resource` instance.
        """
        return self._resource_id

    def __init__(self, message, inner_error=None,
                 resource_type=None, resource_id=None):
        """
        Initializes a new `ResourceError` instance.

        Args:
            message (str): Human readable string describing the exception.
            inner_error (Optional[Exception]): Exception instance that caused
                this exception.
            resource_type (Resource): The type of the problem `Resource`.
            resource_id (uuid): The id of the problem `Resource`.
        """
        super(ResourceError, self).__init__(
            message, inner_error=inner_error)

        self._resource_type = resource_type
        self._resource_id = resource_id


class ResourceNotFoundError(ResourceError):
    """
    Raised when a `Resource` is requested, but none exist matching the
        requested id.
    """
    pass


class ResourceNotCreatedError(ResourceError):
    """
    Raised when `Resource` creation fails.
    """
    pass


class ResourceNotRegisteredError(ResourceError):
    """
    Raised when the registration of a `Resource` fails.
    """
    pass


class ResourceCollisionError(ResourceNotRegisteredError):
    """
    Raised when the registration of a `Resource` fails due to the id of the
        registrant collides with an existing `Resource`.
    """
    pass


class ResourceNotDeletedError(ResourceError):
    """
    Raised when a `Resource` cannot be deleted.
    """
    pass


class ResourceNotReleasedError(ResourceError):
    """
    Raised when a `Resource` cannot be released by a `Model`.
    """
    pass


class ResourceNotUpdatedError(ResourceError):
    """
    Raised when an update to a `Resource` fails.
    """
    pass
