import uuid

import pytest

import elemental_backend as backend


_attribute_type_id = uuid.uuid4()


class _InstantiationParams(object):
    id = [
        (None, None),
        (_attribute_type_id, _attribute_type_id),
        (str(_attribute_type_id), _attribute_type_id)
    ]

    name = [
        (None, None),
        ('foo', 'foo')
    ]

    default_value = [
        (None, None),
        ('string_value', 'string_value'),
        (4, 4),
        (1.3, 1.3)
    ]

    kind_id = [
        (None, None),
        ('str', 'str')
    ]


@pytest.mark.parametrize('id', _InstantiationParams.id)
@pytest.mark.parametrize('name', _InstantiationParams.name)
@pytest.mark.parametrize('default_value', _InstantiationParams.default_value)
@pytest.mark.parametrize('kind_id', _InstantiationParams.kind_id)
def test_attribute_type_instantiation(id, name, default_value, kind_id):
    id_value, id_expected = id
    name_value, name_expected = name
    default_value_value, default_value_expected = default_value
    kind_id_value, kind_id_expected = kind_id

    at = backend.AttributeType(id=id_value, name=name_value,
                               default_value=default_value_value,
                               kind_id=kind_id_value)

    assert at.id == id_expected
    assert at.name == name_expected
    assert at.default_value == default_value_expected
    assert at.kind_id == kind_id_expected
    assert at.kind_properties == {}
