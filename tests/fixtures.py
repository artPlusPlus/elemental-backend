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
def filter_type():
    resource = backend.resources.FilterType(
        id=resource_data.DATA_FILTER_TYPE['id'],
        name=resource_data.DATA_FILTER_TYPE['name'],
        attribute_type_ids=resource_data.DATA_FILTER_TYPE['attribute_type_ids']
    )
    return resource


@pytest.fixture(scope='module')
def filter_instance():
    resource = backend.resources.FilterInstance(
        id=resource_data.DATA_FILTER_INSTANCE['id'],
        type_id=resource_data.DATA_FILTER_INSTANCE['type_id'],
        kind_params=resource_data.DATA_FILTER_INSTANCE['kind_params']
    )
    return resource


@pytest.fixture(scope='module')
def sorter_type():
    resource = backend.resources.SorterType(
        id=resource_data.DATA_SORTER_TYPE['id'],
        name=resource_data.DATA_SORTER_TYPE['name'],
        attribute_type_ids=resource_data.DATA_SORTER_TYPE['attribute_type_ids']
    )
    return resource


@pytest.fixture(scope='module')
def sorter_instance():
    resource = backend.resources.SorterInstance(
        id=resource_data.DATA_SORTER_INSTANCE['id'],
        type_id=resource_data.DATA_SORTER_INSTANCE['type_id'],
        kind_params=resource_data.DATA_SORTER_INSTANCE['kind_params']
    )
    return resource


@pytest.fixture(scope='module')
def view_type():
    resource = backend.resources.ViewType(
        id=resource_data.DATA_VIEW_TYPE['id'],
        name=resource_data.DATA_VIEW_TYPE['name'],
        content_type_ids=resource_data.DATA_VIEW_TYPE['content_type_ids'],
        filter_type_ids=resource_data.DATA_VIEW_TYPE['filter_type_ids'],
        sorter_type_ids=resource_data.DATA_VIEW_TYPE['sorter_type_ids']
    )
    return resource


@pytest.fixture(scope='module')
def view_instance():
    resource = backend.resources.ViewInstance(
        id=resource_data.DATA_VIEW_INSTANCE['id'],
        type_id=resource_data.DATA_VIEW_INSTANCE['type_id'],
        filter_ids=resource_data.DATA_VIEW_INSTANCE['filter_ids'],
        sorter_ids=resource_data.DATA_VIEW_INSTANCE['sorter_ids'],
        result_id=resource_data.DATA_VIEW_INSTANCE['result_id']
    )
    return resource


@pytest.fixture(scope='module')
def view_result():
    resource = backend.resources.ViewResult(
        id=resource_data.DATA_VIEW_RESULT['id']
    )
    return resource
