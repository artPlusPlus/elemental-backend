import uuid


_BASE_ATTR_TYPE_DATA = {
    'id': str(uuid.uuid4()),
    'name': 'name',
    'default_value': None,
    'kind_id': 'string',
    'kind_properties': {}
}


_BASE_CONTENT_TYPE_DATA = {
    'id': str(uuid.uuid4()),
    'name': 'BaseContentType',
    'base_ids': [],
    'attribute_type_ids': [
        str(_BASE_ATTR_TYPE_DATA['id'])
    ]
}


_SUB_ATTR_TYPE_DATA = {
    'id': str(uuid.uuid4()),
    'name': 'depot_path',
    'default_value': None,
    'kind_id': 'string',
    'kind_properties': {}
}


_SUB_CONTENT_TYPE_DATA = {
    'id': str(uuid.uuid4()),
    'name': 'SubContentType',
    'base_ids': [
        _BASE_CONTENT_TYPE_DATA['id']
    ],
    'attribute_type_ids': [
        str(_SUB_ATTR_TYPE_DATA)
    ]
}


_SUB_ATTR_NAME_DATA = {
    'type_id': _BASE_ATTR_TYPE_DATA['id'],
    'source_id': None,
    'id': str(uuid.uuid4()),
    'value': 'MyAsset'
}


_SUB_ATTR_DEPOT_PATH_DATA = {
    'type_id': _SUB_ATTR_TYPE_DATA['id'],
    'source_id': None,
    'id': str(uuid.uuid4()),
    'value': '//depot/foo.txt'
}


_SUB_CONTENT_INSTANCE_DATA = {
    'type_id': _SUB_CONTENT_TYPE_DATA['id'],
    'id': str(uuid.uuid4()),
    'attribute_ids': [
        str(_SUB_ATTR_NAME_DATA['id']),
        str(_SUB_ATTR_DEPOT_PATH_DATA['id'])
    ]
}
