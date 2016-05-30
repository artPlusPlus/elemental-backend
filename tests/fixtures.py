import pytest

import elemental_backend as backend

from tests import resource_data


@pytest.fixture(scope='module')
def controller_json():
    model = backend.Model()
    controller = backend.Controller(model)
    backend.serialization.json.bind_to_controller(controller)
    return controller


@pytest.fixture(scope='module')
def controller():
    model = backend.Model()
    return backend.Controller(model)


@pytest.fixture(scope='module')
def model():
    return backend.Model()


@pytest.fixture(scope='module')
def attribute_type_name():
    resource = backend.resources.AttributeType(
        id=resource_data.DATA_ATTR_TYPE_NAME['id'],
        name=resource_data.DATA_ATTR_TYPE_NAME['name'],
        default_value=resource_data.DATA_ATTR_TYPE_NAME['default_value'],
        kind_id=resource_data.DATA_ATTR_TYPE_NAME['kind_id'],
        kind_properties=resource_data.DATA_ATTR_TYPE_NAME['kind_properties']
    )
    return resource


@pytest.fixture(scope='module')
def attribute_type_path():
    resource = backend.resources.AttributeType(
        id=resource_data.DATA_ATTR_TYPE_PATH['id'],
        name=resource_data.DATA_ATTR_TYPE_PATH['name'],
        default_value=resource_data.DATA_ATTR_TYPE_PATH['default_value'],
        kind_id=resource_data.DATA_ATTR_TYPE_PATH['kind_id'],
        kind_properties=resource_data.DATA_ATTR_TYPE_PATH['kind_properties']
    )
    return resource


@pytest.fixture(scope='module')
def attribute_inst_name():
    resource = backend.resources.AttributeInstance(
        id=resource_data.DATA_ATTR_INST_NAME['id'],
        type_id=resource_data.DATA_ATTR_INST_NAME['type_id'],
        value=resource_data.DATA_ATTR_INST_NAME['value']
    )
    return resource


@pytest.fixture(scope='module')
def attribute_inst_path():
    resource = backend.resources.AttributeInstance(
        id=resource_data.DATA_ATTR_INST_PATH['id'],
        type_id=resource_data.DATA_ATTR_INST_PATH['type_id'],
        value=resource_data.DATA_ATTR_INST_PATH['value']
    )
    return resource


@pytest.fixture(scope='module')
def content_type_base():
    resource = backend.resources.ContentType(
        id=resource_data.DATA_CONTENT_TYPE_BASE['id'],
        name=resource_data.DATA_CONTENT_TYPE_BASE['name'],
        base_ids=resource_data.DATA_CONTENT_TYPE_BASE['base_ids'],
        attribute_type_ids=resource_data.DATA_CONTENT_TYPE_BASE['attribute_type_ids']
    )
    return resource


@pytest.fixture(scope='module')
def content_type_sub():
    resource = backend.resources.ContentType(
        id=resource_data.DATA_CONTENT_TYPE_SUB['id'],
        name=resource_data.DATA_CONTENT_TYPE_SUB['name'],
        base_ids=resource_data.DATA_CONTENT_TYPE_SUB['base_ids'],
        attribute_type_ids=resource_data.DATA_CONTENT_TYPE_SUB['attribute_type_ids']
    )
    return resource


@pytest.fixture(scope='module')
def content_inst_sub():
    resource = backend.resources.ContentInstance(
        id=resource_data.DATA_CONTENT_INST['id'],
        type_id=resource_data.DATA_CONTENT_INST['type_id'],
        attribute_ids=resource_data.DATA_CONTENT_INST['attribute_ids']
    )
    return resource


@pytest.fixture(scope='module')
def view_type():
    resource = backend.resources.ViewType(
        id=resource_data.D
    )