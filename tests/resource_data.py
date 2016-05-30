import uuid


DATA_ATTR_TYPE_NAME = {
    'type': 'AttributeType',
    'id': str(uuid.uuid4()),
    'name': 'name',
    'default_value': None,
    'kind_id': 'StringKind',
    'kind_properties': {}
}


DATA_CONTENT_TYPE_BASE = {
    'type': 'ContentType',
    'id': str(uuid.uuid4()),
    'name': 'BaseContentType',
    'base_ids': [],
    'attribute_type_ids': [
        str(DATA_ATTR_TYPE_NAME['id'])
    ]
}


DATA_ATTR_TYPE_PATH = {
    'type': 'AttributeType',
    'id': str(uuid.uuid4()),
    'name': 'depot_path',
    'default_value': None,
    'kind_id': 'StringKind',
    'kind_properties': {}
}


DATA_CONTENT_TYPE_SUB = {
    'type': 'ContentType',
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
    'type': 'AttributeInstance',
    'type_id': DATA_ATTR_TYPE_NAME['id'],
    'source_id': None,
    'id': str(uuid.uuid4()),
    'value': 'MyFoo'
}


DATA_ATTR_INST_PATH = {
    'type': 'AttributeInstance',
    'type_id': DATA_ATTR_TYPE_PATH['id'],
    'source_id': None,
    'id': str(uuid.uuid4()),
    'value': '//depot/foo.txt'
}


DATA_CONTENT_INST = {
    'type': 'ContentInstance',
    'type_id': DATA_CONTENT_TYPE_SUB['id'],
    'id': str(uuid.uuid4()),
    'attribute_ids': [
        DATA_ATTR_INST_NAME['id'],
        DATA_ATTR_INST_PATH['id']
    ]
}


DATA_FILTER_TYPE = {
    'type': 'FilterType',
    'id': str(uuid.uuid4()),
    'attribute_type_ids': [
        DATA_ATTR_TYPE_NAME['id']
    ]
}


DATA_FILTER_INSTANCE = {
    'type': 'FilterInstance',
    'type_id': DATA_FILTER_TYPE['id'],
    'id': str(uuid.uuid4()),
    'kind_params': {
        'match': '.*Foo'
    }
}


DATA_VIEW_TYPE = {
    'type': 'ViewType',
    'id': str(uuid.uuid4()),
    'content_type_ids': [
        DATA_CONTENT_TYPE_SUB['id']
    ],
    'filter_type_ids': [
        DATA_FILTER_TYPE['id']
    ],
}


DATA_VIEW_INSTANCE = {
    'type': 'ViewInstance',
    'type_id': DATA_VIEW_TYPE['id'],
    'id': str(uuid.uuid4()),
    'filter_ids': [
        DATA_FILTER_INSTANCE['id']
    ]
}
