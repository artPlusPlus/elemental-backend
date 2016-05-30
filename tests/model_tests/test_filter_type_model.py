import uuid

import pytest

import elemental_backend as backend

from tests import utils
from tests.fixtures import model


_filter_type_id_raw = uuid.uuid4()
_filter_type_id_str = uuid.uuid4()
_attribute_type_id_raw = uuid.uuid4()
_attribute_type_id_str = uuid.uuid4()


class _RegistrationParams(object):
    id = [
        (None, None, backend.errors.ResourceNotRegisteredError),
        (_filter_type_id_raw, _filter_type_id_raw, None),
        (str(_filter_type_id_str), _filter_type_id_str, None),
        (_filter_type_id_raw, None, backend.errors.ResourceCollisionError)
    ]

    attribute_type_ids = [
        (None, None, None),
        (_attribute_type_id_raw, [_attribute_type_id_raw], None),
        ([_attribute_type_id_raw], [_attribute_type_id_raw], None),
        (str(_attribute_type_id_str), [_attribute_type_id_str], None),
        ([str(_attribute_type_id_str)], [_attribute_type_id_str], None),
    ]


@pytest.mark.parametrize('id', _RegistrationParams.id)
@pytest.mark.parametrize('attribute_type_ids', _RegistrationParams.attribute_type_ids)
def test_model_register_filter_type(model, id, attribute_type_ids):
    id_value, id_expected, id_error = id
    attr_type_ids_value, attr_type_ids_expected, attr_type_ids_error = attribute_type_ids

    resource = backend.resources.FilterType(
        id=id_value, attribute_type_ids=attr_type_ids_value)
    resource = utils.register_resource(model, resource, id_error, attr_type_ids_error)
    if not resource:
        return

    all_resources = model._resources
    assert resource.id in all_resources
    assert all_resources[resource.id] is resource

    type_resources = model._map__resource_class__resources[backend.resources.FilterType]
    assert resource.id in type_resources
    assert type_resources[resource.id] is resource


class _RetrievalParams(object):
    id = [
        (None, None, ValueError),
        ('foo', None, ValueError),
        (uuid.uuid4(), None, backend.errors.ResourceNotFoundError),
        (_filter_type_id_raw, _filter_type_id_raw, None),
        (str(_filter_type_id_str), _filter_type_id_str, None)
    ]


@pytest.mark.parametrize('id', _RetrievalParams.id)
def test_model_retrieve_filter_type(model, id):
    id_value, id_expected, id_error = id

    resource = utils.retrieve_resource(model, id_value, id_error)
    if not resource:
        return

    assert isinstance(resource, backend.resources.FilterType)
    assert resource.id == id_expected


class _ReleaseParams(object):
    id = [
        (None, None, ValueError),
        ('foo', None, ValueError),
        (uuid.uuid4(), None, backend.errors.ResourceNotFoundError),
        (_filter_type_id_raw, _filter_type_id_raw, None),
        (str(_filter_type_id_str), _filter_type_id_str, None)
    ]


@pytest.mark.parametrize('id', _ReleaseParams.id)
def test_model_release_filter_type(model, id):
    id_value, id_expected, id_error = id

    resource = utils.release_resource(model, id_value, id_error)
    if not resource:
        return

    all_resources = model._resources
    assert resource.id not in all_resources

    type_resources = model._map__resource_class__resources[backend.resources.FilterType]
    assert resource.id not in type_resources
