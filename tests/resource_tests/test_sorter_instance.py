import uuid

import pytest

import elemental_backend as backend


_sorter_instance_id = uuid.uuid4()
_sorter_type_id = uuid.uuid4()


class _InstantiationParams(object):
    id = [
        (None, None),
        (_sorter_instance_id, _sorter_instance_id),
        (str(_sorter_instance_id), _sorter_instance_id)
    ]

    type_id = [
        (None, None),
        (_sorter_type_id, _sorter_type_id),
        (str(_sorter_type_id), _sorter_type_id)
    ]

    kind_params = [
        (None, {}),
        ({'foo': 'bar'}, {'foo': 'bar'})
    ]


@pytest.mark.parametrize('id', _InstantiationParams.id)
@pytest.mark.parametrize('type_id', _InstantiationParams.type_id)
@pytest.mark.parametrize('kind_params', _InstantiationParams.kind_params)
def test_sorter_instance_instantiation(id, type_id, kind_params):
    id_value, id_expected = id
    type_id_value, type_id_expected = type_id
    kind_params_value, kind_params_expected = kind_params

    ai = backend.resources.SorterInstance(id=id_value,
                                          type_id=type_id_value,
                                          kind_params=kind_params_value)

    assert isinstance(ai, backend.resources.SorterInstance)
    assert ai.id == id_expected
    assert ai.type_id == type_id_expected
    assert ai.kind_params == kind_params_expected
