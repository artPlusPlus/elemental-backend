import uuid

import pytest

import elemental_backend as backend


_view_instance_id = uuid.uuid4()
_view_type_id = uuid.uuid4()
_filter_instance_id = uuid.uuid4()


class _InstantiationParams(object):
    id = [
        (None, None),
        (_view_instance_id, _view_instance_id),
        (str(_view_instance_id), _view_instance_id)
    ]

    type_id = [
        (None, None),
        (_view_type_id, _view_type_id),
        (str(_view_type_id), _view_type_id)
    ]

    filter_ids = [
        (None, []),
        (_filter_instance_id, [_filter_instance_id]),
        ([_filter_instance_id], [_filter_instance_id]),
        ([_filter_instance_id, _filter_instance_id], [_filter_instance_id])
    ]


@pytest.mark.parametrize('id', _InstantiationParams.id)
@pytest.mark.parametrize('type_id', _InstantiationParams.type_id)
@pytest.mark.parametrize('filter_ids', _InstantiationParams.filter_ids)
def test_view_instance_instantiation(id, type_id, filter_ids):
    id_value, id_expected = id
    type_id_value, type_id_expected = type_id
    filter_ids_value, filter_ids_expected = filter_ids

    ai = backend.resources.ViewInstance(id=id_value,
                                        type_id=type_id_value,
                                        filter_ids=filter_ids_value)

    assert isinstance(ai, backend.resources.ViewInstance)
    assert ai.id == id_expected
    assert ai.type_id == type_id_expected
    assert ai.filter_ids == filter_ids_expected
