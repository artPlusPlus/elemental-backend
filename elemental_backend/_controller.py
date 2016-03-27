from ._transaction_actions import TransactionActions
from ._controller_events import ControllerEvents
from ._errors import SerializerNotFoundError, DeserializerNotFoundError


class Controller(object):
    """
    A Controller manages the processing of transactions.
    """

    def __init__(self, model):
        self._model = model
        self._serializers = {}
        self._deserializers = {}
        self._handlers = {}

        self._action_handlers = {
            TransactionActions.GET: self._get,
            TransactionActions.POST: self._post,
            TransactionActions.PUT: self._put,
            TransactionActions.DELETE: self._delete,
        }

    def serializer(self, resource_type, format):
        """
        `importer` decorates functions that populate a resource from serialized data.

        Functions decorated as `importers` take two arguments:
            resource - the resource to update
            resource_data - the serialized representation of the data

        Functions decorated as `importers` should not return anything.

        :param resource_type:
        :param format:
        :return:
        """
        def wrap(func):
            self._serializers[(resource_type, format)] = func
            return func
        return wrap

    def deserializer(self, resource_type, format):
        """
        `exporter` decorates functions that convert a resource to serialized data.

        Functions decorated as `exporters` take one argument:
            resource - the resource to serialize

        Functions decorated as `exporters` must return a string representation
            of the resource.

        :param resource_type:
        :param format:
        :return:
        """
        def wrap(func):
            self._deserializers[(resource_type, format)] = func
            return func
        return wrap

    def handler(self, event, action=None, resource_type=None):
        """
        `handler` decorates functions that respond to events that occur during
            the processing of a transaction.

        Functions decorated as `handlers` take one argument:
            transaction - the transaction currently under going processing.

        Functions decorated as `handlers` should not return anything.

        :param event:
        :param action:
        :param resource_type:
        :return:
        """
        def wrap(func):
            key = (event, action, resource_type)
            self._handlers[key] = func
            return func
        return wrap

    def import_resource(self, resource_type, resource_data, format):
        deserializer_key = (resource_type, format)
        try:
            deserializer = self._deserializers[deserializer_key]
        except KeyError:
            e = DeserializerNotFoundError()
            e.key = deserializer_key
            raise e

        resource = resource_type()
        deserializer(resource, resource_data)
        self._model.register_resource(resource)

    def process_transaction(self, transaction):
        self._invoke_handlers(ControllerEvents.transaction_opened,
                              transaction)

        deserializer_key = (transaction.resource_type, transaction.inbound_format)
        try:
            importer = self._deserializers[deserializer_key]
        except KeyError:
            e = DeserializerNotFoundError()
            e.key = deserializer_key
            transaction.errors.append(e)
            self._invoke_handlers(ControllerEvents.transaction_failed,
                                  transaction)
            return transaction
        transaction.inbound_importer = importer

        if transaction.outbound_format:
            serializer_key = (transaction.resource_type,
                              transaction.outbound_format)
            try:
                exporter = self._serializers[serializer_key]
            except KeyError:
                e = SerializerNotFoundError()
                e.key = serializer_key
                transaction.errors.append(e)
                self._invoke_handlers(ControllerEvents.transaction_failed,
                                      transaction)
                return transaction
            transaction.outbound_exporter = exporter

        try:
            action_handler = self._action_handlers[transaction.action]
        except Exception as e:
            # TODO: Action not supported error
            self._invoke_handlers(ControllerEvents.transaction_failed,
                                  transaction)
            return transaction

        try:
            action_handler(transaction)
        except Exception as e:
            # TODO: Set transaction result to error
            self._invoke_handlers(ControllerEvents.transaction_failed,
                                  transaction)
            return transaction
        else:
            self._invoke_handlers(ControllerEvents.transaction_succeeded,
                                  transaction)

        self._invoke_handlers(ControllerEvents.transaction_closing,
                              transaction)

        return transaction

    def _get(self, transaction):
        self._resolve_resource(transaction)

    def _post(self, transaction):
        self._create_resource(transaction)
        self._update_resource(transaction)
        self._register_resource(transaction)

    def _put(self, transaction):
        self._resolve_resource(transaction)
        self._update_resource(transaction)

    def _delete(self, transaction):
        self._resolve_resource(transaction)
        self._delete_resource(transaction)

    def _invoke_handlers(self, event, transaction):
        keys = (
            (event, transaction.action, transaction.resource_type),
            (event, transaction.action, None),
            (event, None, transaction.resource_type),
            (event, None, None)
        )

        for key in keys:
            try:
                handler = self._handlers[key]
            except KeyError:
                pass
            else:
                handler(transaction)

    def _resolve_resource(self, transaction):
        try:
            resource = self._model.retrieve_resource(transaction.resource_type,
                                                transaction.target_resource_id)
        except Exception as e:
            transaction.target_resource = None
            self._invoke_handlers(ControllerEvents.resource_not_resolved,
                                  transaction)
        else:
            transaction.target_resource = resource
            self._invoke_handlers(ControllerEvents.resource_resolved,
                                  transaction)

    def _create_resource(self, transaction):
        try:
            resource = transaction.resource_type()
        except Exception as e:
            transaction.target_resource = None
            self._invoke_handlers(ControllerEvents.resource_not_created,
                                  transaction)
        else:
            transaction.target_resource = resource
            self._invoke_handlers(ControllerEvents.resource_created,
                                  transaction)

    def _register_resource(self, transaction):
        try:
            self._model.register_resource(transaction.target_resource)
        except Exception as e:
            self._invoke_handlers(ControllerEvents.resource_not_registered,
                                  transaction)
        else:
            self._invoke_handlers(ControllerEvents.resource_registered,
                                  transaction)

    def _update_resource(self, transaction):
        deserializer_key = (transaction.resource_type, transaction.format)
        try:
            importer = self._deserializers[deserializer_key]
        except KeyError:
            self._invoke_handlers(ControllerEvents.resource_not_updated,
                                  transaction)
        else:
            try:
                importer(transaction.inbound_payload,
                         transaction.target_resource)
            except Exception as e:
                self._invoke_handlers(ControllerEvents.resource_not_updated,
                                      transaction)
            else:
                self._invoke_handlers(ControllerEvents.resource_updated,
                                      transaction)

    def _delete_resource(self, transaction):
        try:
            self._model.release_resource(transaction.target_resource)
        except Exception as e:
            self._invoke_handlers(ControllerEvents.resource_not_deleted,
                                  transaction)
        else:
            self._invoke_handlers(ControllerEvents.resource_deleted,
                                  transaction)
