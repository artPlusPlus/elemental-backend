import logging
import weakref
from collections import deque

from elemental_core import ElementalError
from elemental_core.util import (
    process_elemental_class_value
)

from .transactions import Actions
from ._controller_events import ControllerEvents
from .errors import (
    InvalidSerializerKeyError,
    SerializerNotFoundError,
    InvalidDeserializerKeyError,
    DeserializerNotFoundError,
    InvalidHandlerKeyError,
    TransactionError,
    InvalidTransactionAction,
    ResourceNotFoundError,
    ResourceNotCreatedError,
    ResourceNotRegisteredError,
    ResourceNotUpdatedError,
    ResourceNotDeletedError
)
from ._util import (
    process_serializer_key,
    process_deserializer_key,
    process_handler_key
)

_LOG = logging.getLogger(__name__)


class Controller(object):
    """
    A `Controller` manages `Model` access through `Transaction` processing.
    """

    def __init__(self, model):
        self._model = model
        self._serializers = weakref.WeakValueDictionary()
        self._deserializers = weakref.WeakValueDictionary()
        self._handlers = {}

    def serializer(self, resource_type, data_format):
        """
        Decorator for registering functions capable of serializing `Resources`.

        `serializer` functions must accept one argument:
            resource - the resource to serialize

        `serializer` functions must return a string.

        Args:
            resource_type (Resource): The type of `Resource` handled by the
                decorated function.
            data_format (str): The serialization format implemented by the
                function. (Ex. `json`, `xml`)

        Returns:
            None

        Notes:
            The decorated function is not modified or wrapped. This decorator
            only acts to identify and track the function for future use by
            the `Controller` instance.
        """
        def wrap(func):
            key = process_serializer_key(resource_type, data_format)
            if not key:
                msg = (
                    'Failed to register "{0}.{1}" as a serializer: '
                    'Invalid resource type or data format.'
                )
                msg = msg.format(func.__module__, func.__name__)

                _LOG.error(msg)
                raise InvalidSerializerKeyError(msg,
                                                resource_type=resource_type,
                                                data_format=data_format)

            self._serializers[key] = func

            msg = 'Registered "{0}.{1}" as the "{2}" serializer to "{3}"'
            msg = msg.format(func.__module__, func.__name__,
                             key[0].__name__, data_format)
            _LOG.info(msg)

            return func
        return wrap

    def deserializer(self, resource_type, data_format):
        """
        Decorator for registering functions capable of deserializing `Resources`.

        `deserializer` functions must accept two arguments:
            resource (Resource): A `Resource` instance to populate
            resource_data (str): Serialized data representing a `Resource`.

        `deserializer` functions should not return any data; it will be discarded.

        Args:
            resource_type (Resource): The type of `Resource` handled by the
                decorated function.
            data_format (str): The serialization format expected by the
                function. (Ex. 'json', 'xml')

        Returns:
            None

        Notes:
            The decorated function is not modified or wrapped. This decorator
            only acts to identify and track the function for future use by
            the `Controller` instance.
        """
        def wrap(func):
            key = process_deserializer_key(resource_type, data_format)
            if not key:
                msg = (
                    'Failed to register "{0}.{1}" as a serializer: '
                    'Invalid resource type or data format.'
                )
                msg = msg.format(func.__module__, func.__name__)

                _LOG.error(msg)
                raise InvalidDeserializerKeyError(msg,
                                                  resource_type=resource_type,
                                                  data_format=data_format)

            self._deserializers[key] = func

            msg = 'Registered "{0}.{1}" as the "{2}" deserializer from "{3}"'
            msg = msg.format(func.__module__, func.__name__,
                             key[0].__name__, data_format)
            _LOG.info(msg)

            return func
        return wrap

    def handler(self, event, action=None, resource_type=None):
        """
        Decorator for registering callback functions for `ControllerEvents`.

        Functions decorated as `handlers` take one argument:
            transaction - the transaction currently under going processing.

        Functions decorated as `handlers` should not return anything.

        Args:
            event (ControllerEvents): The event after which the function should
                be invoked.
            action (Optional[TransactionActions]): Defaults to None.
                If specified, the function will be invoked only if the current
                `Transaction's` action matches `action`. If None, the function
                will be invoked for all `Transactions`.
            resource_type (Optional[Resource]): Defaults to None. If specified,
                the function will be invoked only if the type of the current
                `Transaction's` `target_resource` value matches `resource_type`.
                If None, the function will be invoked for all `Transactions`.

        Returns:
            None

        Notes:
            The decorated function is not modified or wrapped. This decorator
            only acts to identify and track the function for future use by
            the `Controller` instance.
        """
        def wrap(func):
            key = process_handler_key(event, action, resource_type)
            if not key:
                msg = (
                    'Failed to register "{0}.{1}" as a handler: '
                    'Invalid event, action, or resource_type.'
                )
                msg = msg.format(func.__module__, func.__name__)

                _LOG.error(msg)
                raise InvalidHandlerKeyError(msg)

            try:
                handlers = self._handlers[key]
            except KeyError:
                handlers = []
                self._handlers[key] = handlers
            handlers.append(weakref.ref(func))

            msg = 'Registered "{0}.{1}" as an event handler for "{2}"'
            msg = msg.format(func.__module__, func.__name__, event)
            _LOG.info(msg)

            return func
        return wrap

    def import_resource(self, resource_type, resource_data, data_format):
        """
        Create and register a `Resource` outside the `Transaction` system.

        `import_resource` is meant to streamline the population of the model.
        No events are triggered, nor is model state restored if an error occurs
        during resource registration.

        Args:
            resource_type (str): Name of or reference to a `Resource` type.
            resource_data (str): Serialized `Resource` data.
            data_format (str): Format of serialized data.

        Returns:
            None
        """
        deserializer_key = process_deserializer_key(resource_type, data_format)
        if not deserializer_key:
            msg = (
                'Failed to import resource: '
                'Invalid resource type ("{0}") or data format ("{1}").'
            )
            msg = msg.format(resource_type, data_format)

            _LOG.error(msg)
            raise InvalidDeserializerKeyError(msg,
                                              resource_type=resource_type,
                                              data_format=data_format)

        try:
            deserializer = self._deserializers[deserializer_key]
        except KeyError:
            msg = (
                'Failed to import resource: No deserializer found for '
                'resource type "{0}" and data format "{1}".'
            )
            msg = msg.format(repr(resource_type), data_format)

            _LOG.error(msg)
            raise DeserializerNotFoundError(msg, resource_type=resource_type,
                                            data_format=data_format)

        resource_type = process_elemental_class_value(resource_type)
        resource = resource_type()
        deserializer(resource_data, resource)
        self._model.register_resource(resource)

        msg = 'Imported resource "{0}" from "{1}".'
        msg = msg.format(resource.id, data_format)
        _LOG.info(msg)

        return resource

    def export_resource(self, resource_id, data_format):
        """
        Retrieve and serialize a `Resource` outside the `Transaction` system.

        `export_resource` is meant to streamline the persistence of the model.
        No events are triggered.

        Args:
            resource_id (str or UUID): Id of target `Resource`
            data_format (str): Format to serialize target `Resource` to
        """
        try:
            resource = self._model.retrieve_resource(resource_id)
        except (ValueError, ResourceNotFoundError) as e:
            msg = 'Failed to export resource: {0}'.format(e)

            _LOG.error(msg)
            raise e

        serializer_key = process_serializer_key(type(resource), data_format)
        if not serializer_key:
            msg = (
                'Failed to export resource: '
                'Invalid resource type ("{0}") or data format ("{1}").'
            )
            msg = msg.format(type(resource), data_format)

            _LOG.error(msg)
            raise InvalidSerializerKeyError(msg,
                                            resource_type=type(resource),
                                            data_format=data_format)

        try:
            serializer = self._serializers[serializer_key]
        except KeyError:
            msg = (
                'Failed to resolve serializer for '
                'resource type "{0}" and data format "{1}".'
            )
            msg = msg.format(repr(type(resource)), data_format)

            _LOG.error(msg)
            raise SerializerNotFoundError(msg, resource_type=type(resource),
                                          data_format=data_format)

        resource_data = serializer(resource)

        msg = 'Exported resource "{0}" to "{1}".'
        msg = msg.format(resource_id, data_format)
        _LOG.info(msg)

        return resource_data

    def process_transaction(self, transaction):
        """
        Entry point for interaction with the `Model` managed by this `Controller`.

        `process_transaction` provides a way for third-parties to interact with
        a `Model`. As a transaction proceeds, registered handlers for
        `ControllerEvents` are invoked. In cases where the `Model` is mutated,
        the `Controller` will attempt to rollback any changes if the mutation
        fails.

        Args:
            transaction (Transaction): A transaction instance specifying how
                the `Model` should be interrogated or mutated. The
                `Transaction` instance will be modified as it proceeds through
                the system.

        Returns:
            The `Transaction` instance passed in.
        """
        msg = 'Opened Transaction: {0} {1}'
        msg = msg.format(transaction.action, transaction.id)
        _LOG.info(msg)

        processes = {
            Actions.POST: deque((
                self._resolve_transaction_inbound_deserializer,
                self._resolve_transaction_outbound_serializer,
                self._create_resource,
                self._update_resource,
                self._register_resource
            )),
            Actions.GET: deque((
                self._resolve_resource,
                self._resolve_transaction_outbound_serializer
            )),
            Actions.PUT: deque((
                self._resolve_resource,
                self._resolve_transaction_inbound_deserializer,
                self._resolve_transaction_outbound_serializer,
                self._update_resource
            )),
            Actions.DELETE: deque((
                self._resolve_resource,
                self._resolve_transaction_outbound_serializer,
                self._delete_resource
            ))
        }

        try:
            processes = processes[transaction.action]
        except KeyError:
            msg = (
                'Failed to process Transaction "{0}": '
                'Invalid action - "{1}"'
            )
            msg = msg.format(transaction.id, transaction.action)
            e = InvalidTransactionAction(
                msg,
                invalid_action=transaction.action,
                transaction=transaction)
            transaction.errors.append(e)
        else:
            try:
                self._process_transaction(transaction, processes)
            except Exception as e:
                msg = (
                    'Failed to process Transaction "{0}": '
                    'Unexpected error - {1}'
                )
                msg = msg.format(transaction.id, e)
                e = TransactionError(msg, inner_error=e,
                                     transaction=transaction)
                transaction.errors.append(e)

        for error in transaction.errors:
            _LOG.error(error.message)

        if all([not transaction.errors,
                transaction.target_resource,
                transaction.outbound_format]):
            serializer = transaction.outbound_serializer
            resource = transaction.target_resource
            payload = serializer(resource)
            transaction.outbound_payload = payload

        msg = 'Closed Transaction: {0} {1}'
        msg = msg.format(transaction.action, transaction.id)
        _LOG.info(msg)

        return transaction

    def _process_transaction(self, transaction, processes):
        self._invoke_handlers(ControllerEvents.transaction_opened,
                              transaction)

        while processes and not transaction.errors:
            process = processes.popleft()
            try:
                process(transaction)
            except ElementalError as e:
                transaction.errors.append(e)
            except Exception as e:
                msg = 'Failed to process Transaction "{0}": {1}'
                msg = msg.format(transaction.id, e)
                e = TransactionError(msg, inner_error=e,
                                     transaction=transaction)
                transaction.errors.append(e)

        if transaction.errors:
            self._invoke_handlers(ControllerEvents.transaction_failed,
                                  transaction)
        else:
            self._invoke_handlers(ControllerEvents.transaction_succeeded,
                                  transaction)

        self._invoke_handlers(ControllerEvents.transaction_closing,
                              transaction)

    def _resolve_transaction_inbound_deserializer(self, transaction):
        transaction.inbound_deserializer = None

        if not transaction.resource_type:
            msg = (
                'Transaction "{0}" inbound deserializer not resolved: '
                'Transaction has no resource type'
            )
            msg = msg.format(transaction.id)
            _LOG.debug(msg)

        if not transaction.inbound_format:
            msg = (
                'Transaction "{0}" inbound serializer not resolved: '
                'Transaction has no inbound format'
            )
            msg = msg.format(transaction.inbound_format)
            _LOG.debug(msg)

        if not all([transaction.resource_type, transaction.inbound_format]):
            return

        deserializer_key = process_deserializer_key(transaction.resource_type,
                                                    transaction.inbound_format)
        if not deserializer_key:
            msg = (
                'Failed to process Transaction "{0}": '
                'Invalid resource type ("{1}") or data format ("{2}").'
            )
            msg = msg.format(transaction.id, transaction.resource_type,
                             transaction.inbound_format)

            raise InvalidDeserializerKeyError(
                msg,
                resource_type=transaction.resource_type,
                data_format=transaction.inbound_format)

        try:
            deserializer = self._deserializers[deserializer_key]
        except KeyError:
            msg = (
                'Failed to process Transaction "{0}": '
                'No deserializer for resource type "{1}" and data format "{2}".'
            )
            msg = msg.format(transaction.id, transaction.resource_type,
                             transaction.inbound_format)

            raise DeserializerNotFoundError(
                msg,
                resource_type=transaction.resource_type,
                data_format=transaction.inbound_format)
        else:
            transaction.inbound_deserializer = deserializer

    def _resolve_transaction_outbound_serializer(self, transaction):
        transaction.outbound_serializer = None

        if not transaction.resource_type:
            msg = (
                'Transaction "{0}" outbound serializer not resolved: '
                'Transaction has no resource type'
            )
            msg = msg.format(transaction.id)
            _LOG.debug(msg)

        if not transaction.outbound_format:
            msg = (
                'Transaction "{0}" outbound serializer not resolved: '
                'Transaction has no outbound format'
            )
            msg = msg.format(transaction.outbound_format)
            _LOG.debug(msg)

        if not all([transaction.resource_type, transaction.outbound_format]):
            return

        serializer_key = process_serializer_key(transaction.resource_type,
                                                transaction.outbound_format)
        if not serializer_key:
            msg = (
                'Failed to process Transaction "{0}": '
                'Invalid resource type ("{1}") or data format ("{2}").'
            )
            msg = msg.format(transaction.id, transaction.resource_type,
                             transaction.inbound_format)
            raise InvalidSerializerKeyError(
                msg,
                resource_type=transaction.resource_type,
                data_format=transaction.inbound_format)

        try:
            serializer = self._serializers[serializer_key]
        except KeyError:
            msg = (
                'Failed to process Transaction "{0}": '
                'No serializer for resource type "{1}" and data format "{2}".'
            )
            msg = msg.format(transaction.id, transaction.resource_type,
                             transaction.inbound_format)
            raise SerializerNotFoundError(
                msg,
                resource_type=transaction.resource_type,
                data_format=transaction.inbound_format)
        else:
            transaction.outbound_serializer = serializer

    def _resolve_resource(self, transaction):
        resource_id = transaction.resource_id

        if not resource_id:
            msg = (
                'Resource not resolved: '
                'Transaction has no resource id'
            )
            e = ResourceNotFoundError(msg)
            transaction.errors.append(e)
        else:
            try:
                resource = self._model.retrieve_resource(resource_id)
            except Exception as e:
                transaction.target_resource = None

                msg = 'Resource not resolved: {0} - {1}'
                msg = msg.format(type(e).__name__, e)
                e = ResourceNotFoundError(msg, inner_error=e,
                                          resource_id=resource_id)
                transaction.errors.append(e)
            else:
                transaction.target_resource = resource

                msg = 'Resource Resolved: "{0}"'.format(resource_id)
                _LOG.debug(msg)

        if transaction.errors:
            self._invoke_handlers(ControllerEvents.resource_not_resolved,
                                  transaction)
        else:
            self._invoke_handlers(ControllerEvents.resource_resolved,
                                  transaction)

    def _create_resource(self, transaction):
        resource_type = transaction.resource_type

        if not resource_type:
            msg = (
                'Resource not created: '
                'Transaction has no resource type'
            )
            e = ResourceNotCreatedError(msg)
            transaction.errors.append(e)
        else:
            try:
                resource = resource_type()
            except Exception as e:
                transaction.target_resource = None

                msg = 'Resource not created: {0} - {1}'
                msg = msg.format(type(e).__name__, e)
                e = ResourceNotCreatedError(msg, inner_error=e,
                                            resource_type=resource_type)
                transaction.errors.append(e)
            else:
                transaction.target_resource = resource

                msg = 'Resource Created: "{0}"'.format(resource.id)
                _LOG.debug(msg)

        if transaction.errors:
            self._invoke_handlers(ControllerEvents.resource_not_created,
                                  transaction)
        else:
            self._invoke_handlers(ControllerEvents.resource_created,
                                  transaction)

    def _register_resource(self, transaction):
        resource = transaction.target_resource

        if not resource:
            msg = (
                'Resource not updated: '
                'Transaction has no resource'
            )
            e = ResourceNotRegisteredError(msg)
            transaction.errors.append(e)
        else:
            try:
                self._model.register_resource(resource)
            except Exception as e:
                msg = 'Resource not registered: {0} - {1}'
                msg = msg.format(type(e).__name__, e)
                e = ResourceNotRegisteredError(msg, inner_error=e,
                                               resource_type=repr(type(resource)),
                                               resource_id=resource.id)
                transaction.errors.append(e)
            else:
                msg = 'Resource Registered: "{0}"'.format(resource.id)
                _LOG.debug(msg)

        if transaction.errors:
            self._invoke_handlers(ControllerEvents.resource_not_registered,
                                  transaction)
        else:
            self._invoke_handlers(ControllerEvents.resource_registered,
                                  transaction)

    def _update_resource(self, transaction):
        deserializer = transaction.inbound_deserializer
        resource_data = transaction.inbound_payload
        resource = transaction.target_resource

        if not deserializer:
            msg = (
                'Resource not updated: '
                'Transaction has no inbound deserializer'
            )
            e = ResourceNotUpdatedError(msg,
                                        resource_type=repr(type(resource)),
                                        resource_id=resource.id)
            transaction.errors.append(e)
        elif not resource_data:
            msg = (
                'Resource not updated: '
                'Transaction has no resource data'
            )
            e = ResourceNotUpdatedError(msg,
                                        resource_type=repr(type(resource)),
                                        resource_id=resource.id)
            transaction.errors.append(e)
        elif not resource:
            msg = (
                'Resource not updated: '
                'Transaction has no resource'
            )
            e = ResourceNotUpdatedError(msg,
                                        resource_type=repr(type(resource)),
                                        resource_id=resource.id)
            transaction.errors.append(e)
        else:
            try:
                deserializer(resource_data, resource)
            except Exception as e:
                msg = 'Resource not updated: {0} - {1}'
                msg = msg.format(type(e).__name__, e)
                e = ResourceNotUpdatedError(msg, inner_error=e,
                                            resource_type=repr(type(resource)),
                                            resource_id=resource.id)
                transaction.errors.append(e)
            else:
                msg = 'Resource updated: "{0}"'.format(resource.id)
                _LOG.debug(msg)

        if transaction.errors:
            self._invoke_handlers(ControllerEvents.resource_not_updated,
                                  transaction)
        else:
            self._invoke_handlers(ControllerEvents.resource_updated,
                                  transaction)

    def _delete_resource(self, transaction):
        resource = transaction.target_resource

        if not resource:
            msg = (
                'Resource not deleted: '
                'Transaction has no resource'
            )
            e = ResourceNotDeletedError(msg)
            transaction.errors.append(e)
        else:
            try:
                self._model.release_resource(transaction.resource_id)
            except Exception as e:
                msg = 'Resource not deleted: {0} - {1}'
                msg = msg.format(type(e).__name__, e)
                e = ResourceNotDeletedError(msg, inner_error=e,
                                            resource_type=repr(type(resource)),
                                            resource_id=resource.id)
                transaction.errors.append(e)
            else:
                msg = 'Resource deleted: "{0}"'.format(resource.id)
                _LOG.debug(msg)

        if transaction.errors:
            self._invoke_handlers(ControllerEvents.resource_not_deleted,
                                  transaction)
        else:
            self._invoke_handlers(ControllerEvents.resource_deleted,
                                  transaction)

    def _invoke_handlers(self, event, transaction):
        keys = [
            (event, None, None),
            (event, transaction.action, None),
        ]
        if transaction.resource_type:
            keys.extend([
                (event, None, transaction.resource_type),
                (event, transaction.action, transaction.resource_type)
            ])

        for key in keys:
            key = process_handler_key(*key)
            try:
                handlers = self._handlers[key]
            except KeyError:
                continue

            handlers = [h() if isinstance(h, weakref.ref) else h for h in handlers]
            handlers = [h for h in handlers if h]
            self._handlers[key] = [weakref.ref(h) for h in handlers]

            for handler in handlers:
                try:
                    handler(event, transaction)
                except ElementalError as e:
                    transaction.errors.append(e)
                except Exception as e:
                    msg = 'Error occurred in handler "{0}.{1}" - {2}'
                    msg = msg.format(handler.__module__, handler.__name__, e)
                    e = ElementalError(msg, inner_error=e)
                    transaction.errors.append(e)
