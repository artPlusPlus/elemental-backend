import uuid
import json

import elemental_backend as backend
from elemental_backend.serialization import json as json_serialization

from tests import resource_data
from tests.fixtures import *


class _SerializerRegistrationParams(object):
    serializer_data = [
        ('ContentType', 'json', json_serialization.serialize_content_type),
        ('AttributeType', 'json', json_serialization.serialize_attribute_type),
        ('ContentInstance', 'json', json_serialization.serialize_content_instance),
        ('AttributeInstance', 'json', json_serialization.serialize_attribute_instance),
    ]


@pytest.mark.parametrize('serializer_data', _SerializerRegistrationParams.serializer_data)
def test_controller_serializer_registration(controller, serializer_data):
    resource_type, data_format, func = serializer_data

    controller.serializer(resource_type, data_format)(func)

    key = backend._util.process_serializer_key(resource_type, data_format)

    assert controller._serializers[key] is func


class _DeserializerRegistrationParams(object):
    deserializer_data = [
        ('ContentType', 'json', json_serialization.deserialize_content_type),
        ('AttributeType', 'json', json_serialization.deserialize_attribute_type),
        ('ContentInstance', 'json', json_serialization.deserialize_content_instance),
        ('AttributeInstance', 'json', json_serialization.deserialize_attribute_instance),
    ]


@pytest.mark.parametrize('deserializer_data', _DeserializerRegistrationParams.deserializer_data)
def test_controller_deserializer_registration(controller, deserializer_data):
    resource_type, data_format, func = deserializer_data

    controller.deserializer(resource_type, data_format)(func)

    key = backend._util.process_deserializer_key(resource_type, data_format)

    assert controller._deserializers[key] is func


def test_controller_handler_registration(controller):
    event = backend.ControllerEvents.initialized
    action = None
    resource_type = None

    @controller.handler(event, action=action, resource_type=resource_type)
    def _handler(transaction):
        pass

    key = backend._util.process_handler_key(event, action, resource_type)

    assert controller._handlers[key][0]() is _handler


class _ImportParams(object):
    resource_data = [
        ('ContentType', 'json', resource_data.DATA_CONTENT_TYPE_BASE),
        ('ContentType', 'json', resource_data.DATA_CONTENT_TYPE_SUB),
        ('AttributeType', 'json', resource_data.DATA_ATTR_TYPE_NAME),
        ('AttributeType', 'json', resource_data.DATA_ATTR_TYPE_PATH),
        ('AttributeInstance', 'json', resource_data.DATA_ATTR_INST_NAME),
        ('AttributeInstance', 'json', resource_data.DATA_ATTR_INST_PATH)
    ]


@pytest.mark.parametrize('resource_data', _ImportParams.resource_data)
def test_controller_resource_import(controller, resource_data):
    resource_type, data_format, resource_data = resource_data

    resource = controller.import_resource(
        resource_type, json.dumps(resource_data), data_format)

    resource_type = backend._util.process_resource_type_value(resource_type)

    assert isinstance(resource, resource_type)
    assert resource.id == uuid.UUID(resource_data['id'])


class _ExportParams(object):
    resource_data = [
        resource_data.DATA_CONTENT_TYPE_BASE,
        resource_data.DATA_CONTENT_TYPE_SUB,
        resource_data.DATA_ATTR_TYPE_NAME,
        resource_data.DATA_ATTR_TYPE_PATH,
        resource_data.DATA_ATTR_INST_NAME,
        resource_data.DATA_ATTR_INST_PATH
    ]


@pytest.mark.parametrize('resource_data', _ExportParams.resource_data)
def test_controller_resource_export(controller, resource_data):
    resource_id = resource_data['id']
    data_format = 'json'

    export_data = controller.export_resource(resource_id, data_format)

    resource_data = json.dumps(resource_data)

    assert sorted(export_data) == sorted(resource_data)


class _PostParams(object):
    resource_data = [
        (resource_data.DATA_CONTENT_INST, 'ContentInstance', 'json')
    ]


@pytest.mark.parametrize('resource_data', _PostParams.resource_data)
def test_controller_transaction_post(controller, resource_data):
    resource_data, resource_type, data_format = resource_data
    inbound_payload = json.dumps(resource_data)

    transaction = backend.transactions.Post(resource_type, data_format,
                                            inbound_payload)
    controller.process_transaction(transaction)

    resource_id = uuid.UUID(resource_data['id'])

    assert len(transaction.errors) == 0
    assert resource_id in controller._model._resources


class _GetParams(object):
    outbound_format = [
        None,
        'json'
    ]
    resource_data = [
        (resource_data.DATA_CONTENT_TYPE_BASE, backend.ContentType),
        (resource_data.DATA_CONTENT_TYPE_SUB, backend.ContentType),
        (resource_data.DATA_ATTR_TYPE_NAME, backend.AttributeType),
        (resource_data.DATA_ATTR_TYPE_PATH, backend.AttributeType),
        (resource_data.DATA_ATTR_INST_NAME, backend.AttributeInstance),
        (resource_data.DATA_ATTR_INST_PATH, backend.AttributeInstance),
        (resource_data.DATA_CONTENT_INST, backend.ContentInstance)
    ]


@pytest.mark.parametrize('outbound_format', _GetParams.outbound_format)
@pytest.mark.parametrize('resource_data', _GetParams.resource_data)
def test_controller_transaction_get(controller, outbound_format, resource_data):
    resource_data, resource_type = resource_data
    resource_id = resource_data['id']

    transaction = backend.transactions.Get(resource_id,
                                           outbound_format=outbound_format)
    controller.process_transaction(transaction)

    assert len(transaction.errors) == 0
    assert isinstance(transaction.target_resource, resource_type)

    if outbound_format:
        resource_data = json.dumps(resource_data)
        payload = transaction.outbound_payload

        assert sorted(payload) == sorted(resource_data)


class _PutParams(object):
    resource_data =[
        (resource_data.DATA_CONTENT_TYPE_BASE, 'name'),
        (resource_data.DATA_CONTENT_TYPE_SUB, 'name'),
        (resource_data.DATA_ATTR_TYPE_NAME, 'name'),
        (resource_data.DATA_ATTR_TYPE_PATH, 'name'),
        (resource_data.DATA_ATTR_INST_NAME, 'value'),
        (resource_data.DATA_ATTR_INST_PATH, 'value'),
        # (resource_data.DATA_CONTENT_INST, 'name')  # 05/04/2016, excluded - nothing to change
    ]


@pytest.mark.parametrize('resource_data', _PutParams.resource_data)
def test_controller_transaction_put(controller, resource_data):
    resource_data, target_attr = resource_data
    resource_data[target_attr] = '{0}_test'.format(resource_data[target_attr])
    payload = json.dumps(resource_data)

    transaction = backend.transactions.Put(resource_data['id'], 'json', payload)
    transaction.outbound_format = 'json'
    controller.process_transaction(transaction)

    resource_id = uuid.UUID(resource_data['id'])
    resource_data = json.dumps(resource_data)
    payload = transaction.outbound_payload

    assert len(transaction.errors) == 0
    assert resource_id in controller._model._resources
    assert sorted(payload) == sorted(resource_data)


class _DeleteParams(object):
    resource_ids = [
        resource_data.DATA_CONTENT_TYPE_BASE['id'],
        resource_data.DATA_CONTENT_TYPE_SUB['id'],
        resource_data.DATA_ATTR_TYPE_NAME['id'],
        resource_data.DATA_ATTR_TYPE_PATH['id'],
        resource_data.DATA_ATTR_INST_NAME['id'],
        resource_data.DATA_ATTR_INST_PATH['id'],
        resource_data.DATA_CONTENT_INST['id']
    ]


@pytest.mark.parametrize('resource_id', _DeleteParams.resource_ids)
def test_controller_transaction_delete(controller, resource_id):
    transaction = backend.transactions.Delete(resource_id)
    controller.process_transaction(transaction)

    resource_id = uuid.UUID(resource_id)

    assert len(transaction.errors) == 0
    assert resource_id not in controller._model._resources
