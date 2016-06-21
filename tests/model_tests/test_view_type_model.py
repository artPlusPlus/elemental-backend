import uuid

import pytest

import elemental_backend as backend

from tests import utils
from tests.fixtures import model


_view_type_id_raw = uuid.uuid4()
_view_type_id_str = uuid.uuid4()
_content_type_id_raw = uuid.uuid4()
_content_type_id_str = uuid.uuid4()
_filter_type_id_raw = uuid.uuid4()
_filter_type_id_str = uuid.uuid4()


class _RegistrationParams(object):
    id = [
        (None, None, backend.errors.ResourceNotRegisteredError),
        (_view_type_id_raw, _view_type_id_raw, None),
        (str(_view_type_id_str), _view_type_id_str, None),
        (_view_type_id_raw, None, backend.errors.ResourceCollisionError)
    ]

    content_type_ids = [
        (None, [], None),
        (_content_type_id_raw, [_content_type_id_raw], None),
        (str(_content_type_id_str), [_content_type_id_str], None),
        ([_content_type_id_raw], [_content_type_id_raw], None),
        ([str(_content_type_id_str)], [_content_type_id_str], None)
    ]

    filter_type_ids = [
        (None, [], None),
        (_view_type_id_raw, [_view_type_id_raw], None),
        (str(_view_type_id_str), [_view_type_id_str], None),
        ([_view_type_id_raw], [_view_type_id_raw], None),
        ([str(_view_type_id_str)], [_view_type_id_str], None)
    ]


@pytest.mark.parametrize('id', _RegistrationParams.id)
@pytest.mark.parametrize('content_type_ids', _RegistrationParams.content_type_ids)
@pytest.mark.parametrize('filter_type_ids', _RegistrationParams.filter_type_ids)
def test_model_register_view_type(model, id, content_type_ids, filter_type_ids):
    id_value, id_expected, id_error = id
    content_type_ids_value, content_type_ids_expected, content_type_ids_error = content_type_ids
    filter_type_ids_value, filter_type_ids_expected, filter_type_ids_error = filter_type_ids

    resource = backend.resources.ViewType(id=id_value,
                                          content_type_ids=content_type_ids_value,
                                          filter_type_ids=filter_type_ids_value)
    resource = utils.register_resource(model, resource, id_error)
    if not resource:
        return

    all_resources = model._resources
    cls_resources = model._map__resource_cls__resources[backend.resources.ViewType]
    assert resource.id in all_resources
    assert all_resources[resource.id] is resource
    assert resource.id in cls_resources


class _RetrievalParams(object):
    id = [
        (None, None, ValueError),
        ('foo', None, ValueError),
        (uuid.uuid4(), None, backend.errors.ResourceNotFoundError),
        (_view_type_id_raw, _view_type_id_raw, None),
        (str(_view_type_id_str), _view_type_id_str, None)
    ]


@pytest.mark.parametrize('id', _RetrievalParams.id)
def test_model_retrieve_view_type(model, id):
    id_value, id_expected, id_error = id

    resource = utils.retrieve_resource(model, id_value, id_error)
    if not resource:
        return

    assert isinstance(resource, backend.resources.ViewType)
    assert resource.id == id_expected


class _ReleaseParams(object):
    id = [
        (None, None, ValueError),
        ('foo', None, ValueError),
        (uuid.uuid4(), None, backend.errors.ResourceNotFoundError),
        (_view_type_id_raw, _view_type_id_raw, None),
        (str(_view_type_id_str), _view_type_id_str, None)
    ]


@pytest.mark.parametrize('id', _ReleaseParams.id)
def test_model_release_view_type(model, id):
    id_value, id_expected, id_error = id

    resource = utils.release_resource(model, id_value, id_error)
    if not resource:
        return

    all_resources = model._resources
    cls_resources = model._map__resource_cls__resources[backend.resources.ViewType]
    assert resource.id not in all_resources
    assert resource.id not in cls_resources
