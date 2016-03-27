import uuid

import pytest

import elemental_backend as backend


@pytest.fixture(scope='module')
def model():
    return backend.Model()


@pytest.fixture(scope='module')
def attribute_type_name(model):
    resource = backend.AttributeType(
        id=uuid.uuid4(),
        name='Name',
        default_value=backend.NO_VALUE,
        kind_id='str',
        kind_properties=None
    )
    model.register_resource(resource)
    return resource


@pytest.fixture(scope='module')
def attribute_type_path(model):
    resource = backend.AttributeType(
        id=uuid.uuid4(),
        name='Path',
        default_value=backend.NO_VALUE,
        kind_id='str',
        kind_properties=None
    )
    model.register_resource(resource)
    return resource


@pytest.fixture(scope='module')
def attribute_inst_name(model, attribute_type_name):
    resource = backend.AttributeInstance(
        id=uuid.uuid4(),
        type_id=attribute_type_name.id,
        value='FIXTURE_ATTR_INST_NAME'
    )
    model.register_resource(resource)
    return resource


@pytest.fixture(scope='module')
def attribute_inst_path(model, attribute_type_path):
    resource = backend.AttributeInstance(
        id=uuid.uuid4(),
        type_id=attribute_type_path.id,
        value='FIXTURE_ATTR_INST_PATH'
    )
    model.register_resource(resource)
    return resource


@pytest.fixture(scope='module')
def content_type_base(model, attribute_type_name):
    resource = backend.ContentType(
        id=uuid.uuid4(),
        name='FIXTURE_BASE',
        base_ids=None,
        attribute_type_ids=[attribute_type_name.id]
    )
    model.register_resource(resource)
    return resource


@pytest.fixture(scope='module')
def content_type_sub(model, content_type_base, attribute_type_path):
    resource = backend.ContentType(
        id=uuid.uuid4(),
        name='FIXTURE_SUB',
        base_ids=[content_type_base.id],
        attribute_type_ids=[attribute_type_path.id]
    )
    model.register_resource(resource)
    return resource


