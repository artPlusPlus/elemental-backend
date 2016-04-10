import uuid

import pytest

import elemental_backend as backend

from tests import utils
from tests.fixtures import model


_content_type_id_raw = uuid.uuid4()
_content_type_id_str = uuid.uuid4()


class _RegistrationParams(object):
    id = [
        (None, None, backend.errors.ResourceNotRegisteredError),
        (_content_type_id_raw, _content_type_id_raw, None),
        (str(_content_type_id_str), _content_type_id_str, None),
        (_content_type_id_raw, None, backend.errors.ResourceCollisionError)
    ]


@pytest.mark.parametrize('id', _RegistrationParams.id)
def test_model_register_content_type(model, id):
    id_value, id_expected, id_error = id

    resource = backend.resources.ContentType(id=id_value)
    resource = utils.register_resource(model, resource, id_error)
    if not resource:
        return

    all_resources = model._resources
    type_resources = model._map__resource_type__resources[backend.resources.ContentType]
    assert resource.id in all_resources
    assert all_resources[resource.id] is resource
    assert resource.id in type_resources
    assert type_resources[resource.id] is resource


class _RetrievalParams(object):
    id = [
        (None, None, ValueError),
        ('foo', None, ValueError),
        (uuid.uuid4(), None, backend.errors.ResourceNotFoundError),
        (_content_type_id_raw, _content_type_id_raw, None),
        (str(_content_type_id_str), _content_type_id_str, None)
    ]


@pytest.mark.parametrize('id', _RetrievalParams.id)
def test_model_retrieve_content_type(model, id):
    id_value, id_expected, id_error = id

    resource = utils.retrieve_resource(model, id_value, id_error)
    if not resource:
        return

    assert isinstance(resource, backend.resources.ContentType)
    assert resource.id == id_expected


class _ReleaseParams(object):
    id = [
        (None, None, ValueError),
        ('foo', None, ValueError),
        (uuid.uuid4(), None, backend.errors.ResourceNotFoundError),
        (_content_type_id_raw, _content_type_id_raw, None),
        (str(_content_type_id_str), _content_type_id_str, None)
    ]


@pytest.mark.parametrize('id', _ReleaseParams.id)
def test_model_release_content_type(model, id):
    id_value, id_expected, id_error = id

    resource = utils.release_resource(model, id_value, id_error)
    if not resource:
        return

    all_resources = model._resources
    type_resources = model._map__resource_type__resources[backend.resources.ContentType]
    assert resource.id not in all_resources
    assert resource.id not in type_resources