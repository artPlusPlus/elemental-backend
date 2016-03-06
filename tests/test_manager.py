import uuid

import elemental_backend


_BASE_CONTENT_TYPE_DATA = {
    'id': str(uuid.uuid4()),
    'name': 'BaseContentType',
    'base_ids': [],
    'attributes': [
        {
            'id': str(uuid.uuid4()),
            'name': 'name',
            'kind_id': 'string',
            'default_value': None,
            'kind_properties': {}
        }
    ]
}


_SUB_CONTENT_TYPE_DATA = {
    'id': str(uuid.uuid4()),
    'name': 'SubContentType',
    'base_ids': [
        _BASE_CONTENT_TYPE_DATA['id']
    ],
    'attributes': [
        {
            'id': str(uuid.uuid4()),
            'name': 'depot_path',
            'kind_id': 'string',
            'default_value': None,
            'kind_properties': {}
        },
    ]
}


_SUB_CONTENT_INSTANCE_DATA = {
    'type_id': _SUB_CONTENT_TYPE_DATA['id'],
    'id': str(uuid.uuid4()),
    'attributes': [
        {
            'type_id': _BASE_CONTENT_TYPE_DATA['attributes'][0]['id'],
            'source_id': None,
            'id': str(uuid.uuid4()),
            'value': 'MyAsset'
        },
        {
            'type_id': _SUB_CONTENT_TYPE_DATA['attributes'][0]['id'],
            'source_id': None,
            'id': str(uuid.uuid4()),
            'value': '//depot/foo.txt'
        }
    ]
}


def test_manager_instantiation():
    mgr = elemental_backend.Manager()

    assert isinstance(mgr, elemental_backend.Manager)


def test_manager_import_base_content_type_json():
    mgr = elemental_backend.Manager()

    mgr.import_content_type_json(_BASE_CONTENT_TYPE_DATA)
    content_type = mgr.get_content_type(_BASE_CONTENT_TYPE_DATA['id'])

    assert content_type
    assert str(content_type.id) == _BASE_CONTENT_TYPE_DATA['id']
    assert content_type.name == _BASE_CONTENT_TYPE_DATA['name']


def test_manager_import_sub_content_type_json():
    mgr = elemental_backend.Manager()

    mgr.import_content_type_json(_BASE_CONTENT_TYPE_DATA)
    mgr.import_content_type_json(_SUB_CONTENT_TYPE_DATA)
    content_type = mgr.get_content_type(_SUB_CONTENT_TYPE_DATA['id'])

    assert content_type
    assert str(content_type.id) == _SUB_CONTENT_TYPE_DATA['id']
    assert content_type.name == _SUB_CONTENT_TYPE_DATA['name']


def test_manager_import_content_instance_json():
    mgr = elemental_backend.Manager()

    mgr.import_content_type_json(_BASE_CONTENT_TYPE_DATA)
    mgr.import_content_type_json(_SUB_CONTENT_TYPE_DATA)
    mgr.import_content_json(_SUB_CONTENT_INSTANCE_DATA)
    content_instance = mgr.get_content(_SUB_CONTENT_INSTANCE_DATA['id'])

    assert str(content_instance.id) == _SUB_CONTENT_INSTANCE_DATA['id']
    assert str(content_instance.type_id) == _SUB_CONTENT_TYPE_DATA['id']
