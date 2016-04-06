import uuid

import pytest

import elemental_backend as backend


_content_type_id = uuid.uuid4()
_base_id = uuid.uuid4()
_base_ids = [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
_attribute_type_id = uuid.uuid4()
_attribute_type_ids = [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]


class _InstantiationParams(object):
    id = [
        (None, None),
        (_content_type_id, _content_type_id),
        (str(_content_type_id), _content_type_id)
    ]

    name = [
        (None, None),
        ('foo', 'foo')
    ]

    base_ids = [
        (None, []),
        (_base_id, [_base_id]),
        (str(_base_id), [_base_id]),
        (_base_ids, _base_ids),
        ([str(bid) for bid in _base_ids], _base_ids)
    ]

    attribute_type_ids = [
        (None, []),
        (_attribute_type_id, [_attribute_type_id]),
        (str(_attribute_type_id), [_attribute_type_id]),
        (_attribute_type_ids, _attribute_type_ids),
        ([str(atid) for atid in _attribute_type_ids], _attribute_type_ids)
    ]


@pytest.mark.parametrize('id', _InstantiationParams.id)
@pytest.mark.parametrize('name', _InstantiationParams.name)
@pytest.mark.parametrize('base_ids', _InstantiationParams.base_ids)
@pytest.mark.parametrize('attribute_type_ids', _InstantiationParams.attribute_type_ids)
def test_content_instance_instantiation(id, name, base_ids, attribute_type_ids):
    id_value, id_expected = id
    name_value, name_expected = name
    base_ids_value, base_ids_expected = base_ids
    attribute_type_ids_value, attribute_type_ids_expected = attribute_type_ids

    ct = backend.resources.ContentType(
        id=id_value, name=name_value, base_ids=base_ids_value,
        attribute_type_ids=attribute_type_ids_value)

    assert isinstance(ct, backend.resources.ContentType)
    assert ct.id == id_expected
    assert ct.name == name_expected
    assert ct.base_ids == base_ids_expected
    assert ct.attribute_type_ids == attribute_type_ids_expected
