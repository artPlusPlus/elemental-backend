import uuid


DATA_ATTR_TYPE_NAME = {
    'id': str(uuid.uuid4()),
    'name': 'name',
    'default_value': None,
    'kind_id': 'string',
    'kind_properties': {}
}


DATA_CONTENT_TYPE_BASE = {
    'id': str(uuid.uuid4()),
    'name': 'BaseContentType',
    'base_ids': [],
    'attribute_type_ids': [
        str(DATA_ATTR_TYPE_NAME['id'])
    ]
}


DATA_ATTR_TYPE_PATH = {
    'id': str(uuid.uuid4()),
    'name': 'depot_path',
    'default_value': None,
    'kind_id': 'string',
    'kind_properties': {}
}


DATA_CONTENT_TYPE_SUB = {
    'id': str(uuid.uuid4()),
    'name': 'SubContentType',
    'base_ids': [
        DATA_CONTENT_TYPE_BASE['id']
    ],
    'attribute_type_ids': [
        str(DATA_ATTR_TYPE_PATH['id'])
    ]
}


DATA_ATTR_INST_NAME = {
    'type_id': DATA_ATTR_TYPE_NAME['id'],
    'source_id': None,
    'id': str(uuid.uuid4()),
    'value': 'MyAsset'
}


DATA_ATTR_INST_PATH = {
    'type_id': DATA_ATTR_TYPE_PATH['id'],
    'source_id': None,
    'id': str(uuid.uuid4()),
    'value': '//depot/foo.txt'
}


DATA_CONTENT_INST = {
    'type_id': DATA_CONTENT_TYPE_SUB['id'],
    'id': str(uuid.uuid4()),
    'attribute_ids': [
        str(DATA_ATTR_INST_NAME['id']),
        str(DATA_ATTR_INST_PATH['id'])
    ]
}
