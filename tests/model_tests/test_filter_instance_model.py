import uuid

import pytest

import elemental_backend as backend

from tests import utils
from tests.fixtures import model


_filter_type_id_raw = uuid.uuid4()
_filter_type_id_str = uuid.uuid4()
_filter_inst_id_raw = uuid.uuid4()
_filter_inst_id_str = uuid.uuid4()


class _RegistrationParams(object):
    id = [
        (None, None, backend.errors.ResourceNotRegisteredError),
        (_filter_inst_id_raw, _filter_inst_id_raw, None),
        (str(_filter_inst_id_str), _filter_inst_id_str, None),
        (_filter_inst_id_raw, None, backend.errors.ResourceCollisionError)
    ]

    type_id = [
        (None, None, backend.errors.ResourceNotRegisteredError),
        (_filter_type_id_raw, _filter_type_id_raw, None),
        (str(_filter_type_id_str), _filter_type_id_str, None)
    ]


@pytest.mark.parametrize('id', _RegistrationParams.id)
@pytest.mark.parametrize('type_id', _RegistrationParams.type_id)
def test_model_register_filter_instance(model, id, type_id):
    id_value, id_expected, id_error = id
    type_id_value, typ_id_expected, type_id_error = type_id

    resource = backend.resources.FilterInstance(id=id_value, type_id=type_id_value)
    resource = utils.register_resource(model, resource, id_error, type_id_error)
    if not resource:
        return

    all_resources = model._resources
    assert resource.id in all_resources
    assert all_resources[resource.id] is resource

    type_resources = model._map__resource_class__resources[backend.resources.FilterInstance]
    assert resource.id in type_resources
    assert type_resources[resource.id] is resource

    # Entries in _map__filter_instance__view_instance should be created
    # when a ViewInstance is registered.
    map_fi_vi = model._map__filter_instance__view_instance
    assert resource.id not in map_fi_vi


class _RetrievalParams(object):
    id = [
        (None, None, ValueError),
        ('foo', None, ValueError),
        (uuid.uuid4(), None, backend.errors.ResourceNotFoundError),
        (_filter_inst_id_raw, _filter_inst_id_raw, None),
        (str(_filter_inst_id_str), _filter_inst_id_str, None)
    ]


@pytest.mark.parametrize('id', _RetrievalParams.id)
def test_model_retrieve_filter_instance(model, id):
    id_value, id_expected, id_error = id

    resource = utils.retrieve_resource(model, id_value, id_error)
    if not resource:
        return

    assert isinstance(resource, backend.resources.FilterInstance)
    assert resource.id == id_expected


class _ReleaseParams(object):
    id = [
        (None, None, ValueError),
        ('foo', None, ValueError),
        (uuid.uuid4(), None, backend.errors.ResourceNotFoundError),
        (_filter_inst_id_raw, _filter_inst_id_raw, None),
        (str(_filter_inst_id_str), _filter_inst_id_str, None)
    ]


@pytest.mark.parametrize('id', _ReleaseParams.id)
def test_model_release_filter_instance(model, id):
    id_value, id_expected, id_error = id

    resource = utils.release_resource(model, id_value, id_error)
    if not resource:
        return

    all_resources = model._resources
    assert resource.id not in all_resources

    type_resources = model._map__resource_class__resources[backend.resources.FilterInstance]
    assert resource.id not in type_resources

    map_fi_vi = model._map__filter_instance__view_instance
    assert resource.id not in map_fi_vi
