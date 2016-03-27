import uuid

import pytest

import elemental_backend as backend


_content_instance_id = uuid.uuid4()
_content_type_id = uuid.uuid4()
_attribute_id = uuid.uuid4()
_attribute_ids = [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]


class _InstantiationParams(object):
    id = [
        (None, None),
        (_content_instance_id, _content_instance_id),
        (str(_content_instance_id), _content_instance_id)
    ]

    type_id = [
        (None, None),
        (_content_type_id, _content_type_id),
        (str(_content_type_id), _content_type_id)
    ]

    attribute_ids = [
        (None, []),
        (_attribute_id, [_attribute_id]),
        (str(_attribute_id), [_attribute_id]),
        (_attribute_ids, _attribute_ids),
        ([str(aid) for aid in _attribute_ids], _attribute_ids)
    ]


@pytest.mark.parametrize('id', _InstantiationParams.id)
@pytest.mark.parametrize('type_id', _InstantiationParams.type_id)
@pytest.mark.parametrize('attribute_ids', _InstantiationParams.attribute_ids)
def test_content_instance_instantiation(id, type_id, attribute_ids):
    id_value, id_expected = id
    type_id_value, type_id_expected = type_id
    attribute_ids_value, attribute_ids_expected = attribute_ids

    ci = backend.ContentInstance(id=id_value, type_id=type_id_value,
                                 attribute_ids=attribute_ids_value)

    assert isinstance(ci, backend.ContentInstance)
    assert ci.id == id_expected
    assert ci.type_id == type_id_expected
    assert ci.attribute_ids == attribute_ids_expected
