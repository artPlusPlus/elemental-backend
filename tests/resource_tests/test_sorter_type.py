import uuid

import pytest

import elemental_backend as backend


_sorter_type_id = uuid.uuid4()
_attribute_type_id = uuid.uuid4()


class _InstantiationParams(object):
    id = [
        (None, None),
        (_sorter_type_id, _sorter_type_id),
        (str(_sorter_type_id), _sorter_type_id)
    ]

    name = [
        (None, None),
        ('foo', 'foo')
    ]

    attribute_type_ids = [
        (None, []),
        (_attribute_type_id, [_attribute_type_id]),
        ([_attribute_type_id], [_attribute_type_id]),
        ([_attribute_type_id, _attribute_type_id], [_attribute_type_id])
    ]


@pytest.mark.parametrize('id', _InstantiationParams.id)
@pytest.mark.parametrize('name', _InstantiationParams.name)
@pytest.mark.parametrize('attribute_type_ids', _InstantiationParams.attribute_type_ids)
def test_sorter_type_instantiation(id, name, attribute_type_ids):
    id_value, id_expected = id
    name_value, name_expected = name
    attribute_type_ids_value, attribute_type_ids_expected = attribute_type_ids

    at = backend.resources.SorterType(id=id_value, name=name_value,
                                      attribute_type_ids=attribute_type_ids_value)

    assert at.id == id_expected
    assert at.name == name_expected
    assert at.attribute_type_ids == attribute_type_ids_expected
