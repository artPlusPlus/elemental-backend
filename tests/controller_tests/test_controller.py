import uuid
import json

from elemental_core.util import process_elemental_class_value

import elemental_backend as backend
from elemental_backend.serialization import json as json_serialization

from tests import resource_data
from tests.fixtures import *


class _SerializerRegistrationParams(object):
    serializer_data = [
        ('ContentType', 'json', json_serialization.serialize_content_type),
        ('AttributeType', 'json', json_serialization.serialize_attribute_type),
        ('FilterType', 'json', json_serialization.serialize_filter_type),
        ('ViewType', 'json', json_serialization.serialize_view_type),
        ('ContentInstance', 'json', json_serialization.serialize_content_instance),
        ('AttributeInstance', 'json', json_serialization.serialize_attribute_instance),
        ('FilterInstance', 'json', json_serialization.serialize_filter_instance),
        ('ViewInstance', 'json', json_serialization.serialize_view_instance)
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
        ('FilterType', 'json', json_serialization.deserialize_filter_type),
        ('ViewType', 'json', json_serialization.deserialize_view_type),
        ('ContentInstance', 'json', json_serialization.deserialize_content_instance),
        ('AttributeInstance', 'json', json_serialization.deserialize_attribute_instance),
        ('FilterInstance', 'json', json_serialization.deserialize_filter_instance),
        ('ViewInstance', 'json', json_serialization.deserialize_view_instance)
    ]


@pytest.mark.parametrize('deserializer_data', _DeserializerRegistrationParams.deserializer_data)
def test_controller_deserializer_registration(controller, deserializer_data):
    resource_type, data_format, func = deserializer_data

    controller.deserializer(resource_type, data_format)(func)

    key = backend._util.process_deserializer_key(resource_type, data_format)

    assert controller._deserializers[key] is func


def test_controller_handler_registration(controller):
    event = backend.ControllerEvents.resource_created
    action = None
    resource_type = None

    @controller.handler(event, action=action, resource_type=resource_type)
    def _handler(_):
        pass

    key = backend._util.process_handler_key(event, action, resource_type)

    assert controller._handlers[key][0]() is _handler

    del _handler


class _ImportParams(object):
    resource_data = [
        (resource_data.DATA_CONTENT_TYPE_BASE, 'json'),
        (resource_data.DATA_CONTENT_TYPE_SUB, 'json'),
        (resource_data.DATA_ATTR_TYPE_NAME, 'json'),
        (resource_data.DATA_ATTR_TYPE_PATH, 'json'),
        (resource_data.DATA_FILTER_TYPE, 'json'),
        (resource_data.DATA_VIEW_TYPE, 'json'),
        # (resource_data.DATA_CONTENT_INST, 'json'),  # Will be POSTed later
        (resource_data.DATA_ATTR_INST_NAME, 'json'),
        (resource_data.DATA_ATTR_INST_PATH, 'json'),
        (resource_data.DATA_FILTER_INSTANCE, 'json'),
        (resource_data.DATA_VIEW_INSTANCE, 'json')
    ]


@pytest.mark.parametrize('resource_data', _ImportParams.resource_data)
def test_controller_resource_import(controller, resource_data):
    resource_data, data_format = resource_data

    resource = controller.import_resource(
        resource_data['type'], json.dumps(resource_data), data_format)

    resource_type = process_elemental_class_value(resource_data['type'])

    assert isinstance(resource, resource_type)
    assert resource.id == uuid.UUID(resource_data['id'])


class _ExportParams(object):
    resource_data = [
        resource_data.DATA_CONTENT_TYPE_BASE,
        resource_data.DATA_CONTENT_TYPE_SUB,
        resource_data.DATA_ATTR_TYPE_NAME,
        resource_data.DATA_ATTR_TYPE_PATH,
        # (resource_data.DATA_CONTENT_INST,  # Will be POSTed later
        resource_data.DATA_ATTR_INST_NAME,
        resource_data.DATA_ATTR_INST_PATH,
        resource_data.DATA_FILTER_TYPE,
        resource_data.DATA_FILTER_INSTANCE,
        resource_data.DATA_VIEW_TYPE,
        resource_data.DATA_VIEW_INSTANCE
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
        (resource_data.DATA_CONTENT_INST, 'json')
    ]


@pytest.mark.parametrize('resource_data', _PostParams.resource_data)
def test_controller_transaction_post(controller, resource_data):
    resource_data, data_format = resource_data
    inbound_payload = json.dumps(resource_data)

    transaction = backend.transactions.Post(resource_data['type'], data_format,
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
        (resource_data.DATA_CONTENT_TYPE_BASE, backend.resources.ContentType),
        (resource_data.DATA_CONTENT_TYPE_SUB, backend.resources.ContentType),
        (resource_data.DATA_ATTR_TYPE_NAME, backend.resources.AttributeType),
        (resource_data.DATA_ATTR_TYPE_PATH, backend.resources.AttributeType),
        (resource_data.DATA_FILTER_TYPE, backend.resources.FilterType),
        (resource_data.DATA_VIEW_TYPE, backend.resources.ViewType),
        (resource_data.DATA_CONTENT_INST, backend.resources.ContentInstance),
        (resource_data.DATA_ATTR_INST_NAME, backend.resources.AttributeInstance),
        (resource_data.DATA_ATTR_INST_PATH, backend.resources.AttributeInstance),
        (resource_data.DATA_FILTER_INSTANCE, backend.resources.FilterInstance),
        (resource_data.DATA_VIEW_INSTANCE, backend.resources.ViewInstance)
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
        (resource_data.DATA_FILTER_TYPE, 'name'),
        (resource_data.DATA_VIEW_TYPE, 'name'),
        # (resource_data.DATA_CONTENT_INST, 'name'),  # 05/04/2016, excluded - nothing to change
        (resource_data.DATA_ATTR_INST_NAME, 'value'),
        (resource_data.DATA_ATTR_INST_PATH, 'value'),
        # (resource_data.DATA_FILTER_INSTANCE, ''),  # 5/30/2016, excluded - nothing to change
        # (resource_data.DATA_VIEW_INSTANCE, '')  # 5/30/2016, excluded - nothing to change
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
        resource_data.DATA_FILTER_TYPE['id'],
        resource_data.DATA_VIEW_TYPE['id'],
        resource_data.DATA_CONTENT_INST['id'],
        resource_data.DATA_ATTR_INST_NAME['id'],
        resource_data.DATA_ATTR_INST_PATH['id'],
        resource_data.DATA_FILTER_INSTANCE['id'],
        resource_data.DATA_VIEW_INSTANCE['id']
    ]


@pytest.mark.parametrize('resource_id', _DeleteParams.resource_ids)
def test_controller_transaction_delete(controller, resource_id):
    transaction = backend.transactions.Delete(resource_id)
    controller.process_transaction(transaction)

    resource_id = uuid.UUID(resource_id)

    assert len(transaction.errors) == 0
    assert resource_id not in controller._model._resources
