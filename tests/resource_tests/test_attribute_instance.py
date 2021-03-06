import uuid

import pytest

import elemental_backend as backend
import elemental_core as core


_attribute_instance_id = uuid.uuid4()
_attribute_type_id = uuid.uuid4()


class _InstantiationParams(object):
    id = [
        (None, None),
        (_attribute_instance_id, _attribute_instance_id),
        (str(_attribute_instance_id), _attribute_instance_id)
    ]

    type_id = [
        (None, None),
        (_attribute_type_id, _attribute_type_id),
        (str(_attribute_type_id), _attribute_type_id)
    ]

    value = [
        (core.NO_VALUE, core.NO_VALUE),
        (None, None),
        ('string_value', 'string_value'),
        (4, 4),
        (1.3, 1.3)
    ]


@pytest.mark.parametrize('id', _InstantiationParams.id)
@pytest.mark.parametrize('type_id', _InstantiationParams.type_id)
@pytest.mark.parametrize('value', _InstantiationParams.value)
def test_attribute_instance_instantiation(id, type_id, value):
    id_value, id_expected = id
    type_id_value, type_id_expected = type_id
    value_value, value_expected = value

    ai = backend.resources.AttributeInstance(id=id_value,
                                             type_id=type_id_value,
                                             value=value_value)

    assert isinstance(ai, backend.resources.AttributeInstance)
    assert ai.id == id_expected
    assert ai.type_id == type_id_expected
    assert ai.value == value_expected
