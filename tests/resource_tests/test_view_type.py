import uuid

import pytest

import elemental_backend as backend


_view_type_id = uuid.uuid4()
_content_type_id = uuid.uuid4()
_filter_type_id = uuid.uuid4()


class _InstantiationParams(object):
    id = [
        (None, None),
        (_view_type_id, _view_type_id),
        (str(_view_type_id), _view_type_id)
    ]

    name = [
        (None, None),
        ('foo', 'foo')
    ]

    content_type_ids = [
        (None, []),
        (_content_type_id, [_content_type_id]),
        ([_content_type_id], [_content_type_id]),
        ([_content_type_id, _content_type_id], [_content_type_id])
    ]

    filter_type_ids = [
        (None, []),
        (_filter_type_id, [_filter_type_id]),
        ([_filter_type_id], [_filter_type_id]),
        ([_filter_type_id, _filter_type_id], [_filter_type_id])
    ]


@pytest.mark.parametrize('id', _InstantiationParams.id)
@pytest.mark.parametrize('name', _InstantiationParams.name)
@pytest.mark.parametrize('content_type_ids', _InstantiationParams.content_type_ids)
@pytest.mark.parametrize('filter_type_ids', _InstantiationParams.filter_type_ids)
def test_view_type_instantiation(id, name, content_type_ids, filter_type_ids):
    id_value, id_expected = id
    name_value, name_expected = name
    content_type_ids_value, content_type_ids_expected = content_type_ids
    filter_type_ids_value, filter_type_ids_expected = filter_type_ids

    at = backend.resources.ViewType(id=id_value, name=name_value,
                                    content_type_ids=content_type_ids_value,
                                    filter_type_ids=filter_type_ids_value)

    assert at.id == id_expected
    assert at.name == name_expected
    assert at.content_type_ids == content_type_ids_expected
    assert at.filter_type_ids == filter_type_ids_expected
