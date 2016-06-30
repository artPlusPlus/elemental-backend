import uuid
import json as default_json


_json = default_json


def serialize_content_type(content_type):
    """
    Extracts data from `content_type` into a JSON string.

    Args:
        content_type (ContentType): The ``ContentType`` instance to be
            serialized.

    Returns:
        str: Raw JSON string containing `content_type` data.
    """
    data = {
        'type': type(content_type).__name__,
        'id': str(content_type.id),
        'name': str(content_type.name),
        'base_ids': [str(bid) for bid in content_type.base_ids],
        'attribute_type_ids': [str(atid) for atid in
                               content_type.attribute_type_ids]
    }

    data = _json.dumps(data)

    return data


def deserialize_content_type(data, content_type):
    """
    Populates `content_type` with values extracted from `data`.

    Args:
        data (str): Raw JSON string containing ``ContentType`` data.
        content_type (ContentType): A ``ContentType`` instance to be populated
            with `data`.

    Returns:
        None
    """
    data = _json.loads(data)

    id = uuid.UUID(data['id'])
    name = data['name']
    base_ids = data['base_ids']
    attribute_type_ids = data['attribute_type_ids']

    content_type.id = id
    content_type.name = name
    content_type.base_ids = base_ids
    content_type.attribute_type_ids = attribute_type_ids


def serialize_attribute_type(attribute_type):
    """
    Extracts data from `attribute_type` into a JSON string.

    Args:
        attribute_type (AttributeType): The ``AttributeType`` instance to be
            serialized.

    Returns:
        str: Raw JSON string containing `attribute_type` data.
    """
    data = {
        'type': type(attribute_type).__name__,
        'id': str(attribute_type.id),
        'name': str(attribute_type.name),
        'default_value': attribute_type.default_value,
        'kind_id': str(attribute_type.kind_id),
        'kind_properties': attribute_type.kind_properties
    }

    data = _json.dumps(data)

    return data


def deserialize_attribute_type(data, attribute_type):
    """
    Populates `attribute_type` with values extracted from `data`.

    Args:
        data (str): Raw JSON string containing ``AttributeType`` data.
        attribute_type (AttributeType): An ``AttributeType`` instance to be
            populated with `data`.

    Returns:
        None
    """
    data = _json.loads(data)

    id = data['id']
    name = data['name']
    default_value = data['default_value']
    kind_id = data['kind_id']
    kind_properties = data['kind_properties']

    attribute_type.id = id
    attribute_type.name = name
    attribute_type.default_value = default_value
    attribute_type.kind_id = kind_id
    attribute_type.kind_properties = kind_properties


def serialize_filter_type(filter_type):
    """
    Extracts data from `filter_type` into a JSON string.

    Args:
        filter_type (FilterType): The ``FilterType`` instance to be serialized.

    Returns:
        str: Raw JSON string containing `filter_type` data.
    """
    data = {
        'type': type(filter_type).__name__,
        'id': str(filter_type.id),
        'name': filter_type.name,
        'attribute_type_ids': [str(at_id) for at_id in
                               filter_type.attribute_type_ids]
    }

    data = _json.dumps(data)

    return data


def deserialize_filter_type(data, filter_type):
    """
    Populates `filter_type` with values extracted from `data`.

    Args:
        data (str): Raw JSON string containing ``FilterType`` data.
        filter_type (FilterType): A ``FilterType`` instance to be populated
            with `data`.

    Returns:
        None
    """
    data = _json.loads(data)

    id = data['id']
    name = data['name']
    attribute_type_ids = data['attribute_type_ids']

    filter_type.id = id
    filter_type.name = name
    filter_type.attribute_type_ids = attribute_type_ids


def serialize_view_type(view_type):
    """
    Extracts data from `view_type` into a JSON string.

    Args:
        view_type (ViewType): The ``ViewType`` instance to be serialized.

    Returns:
        str: Raw JSON string containing `view_type` data.
    """
    data = {
        'type': type(view_type).__name__,
        'id': str(view_type.id),
        'name': view_type.name,
        'content_type_ids': [str(ct_id) for ct_id in
                             view_type.content_type_ids],
        'filter_type_ids': [str(ft_id) for ft_id in view_type.filter_type_ids]
    }

    data = _json.dumps(data)

    return data


def deserialize_view_type(data, view_type):
    """
    Populates `view_type` with values extracted from `data`.

    Args:
        data (str): Raw JSON string containing ``ViewType`` data.
        view_type (ViewType): A ``ViewType`` instance to be populated with
            `data`.

    Returns:
        None
    """
    data = _json.loads(data)

    id = data['id']
    name = data['name']
    content_type_ids = data['content_type_ids']
    filter_type_ids = data['filter_type_ids']

    view_type.id = id
    view_type.name = name
    view_type.content_type_ids = content_type_ids
    view_type.filter_type_ids = filter_type_ids


def serialize_content_instance(content_instance):
    """
    Extracts data from `content_instance` into a JSON string.

    Args:
        content_instance (ContentInstance): The ``ContentInstance`` instance
            to be serialized.

    Returns:
        str: Raw JSON string containing `content_instance` data.
    """
    data = {
        'type': type(content_instance).__name__,
        'id': str(content_instance.id),
        'type_id': str(content_instance.type_id),
        'attribute_ids': [str(aid) for aid in
                          content_instance.attribute_ids]
    }

    data = _json.dumps(data)

    return data


def deserialize_content_instance(data, content_instance):
    """
    Populates `content_instance` with values extracted from `data`.

    Args:
        data (str): Raw JSON string containing ``ContentInstance`` data.
        content_instance (ContentInstance): A ``ContentInstance`` instance to
            be populated with `data`.

    Returns:
        None
    """
    data = _json.loads(data)

    id = data['id']
    type_id = data['type_id']
    attribute_ids = data['attribute_ids']

    content_instance.id = id
    content_instance.type_id = type_id
    content_instance.attribute_ids = attribute_ids


def serialize_attribute_instance(attribute_instance):
    """
    Extracts data from `attribute_instance` into a JSON string.

    Args:
        attribute_instance (ContentInstance): The ``AttributeInstance``
            instance to be serialized.

    Returns:
        str: Raw JSON string containing `attribute_instance` data.
    """
    if attribute_instance.source_id:
        source_id = str(attribute_instance.source_id)
    else:
        source_id = attribute_instance.source_id

    data = {
        'type': type(attribute_instance).__name__,
        'id': str(attribute_instance.id),
        'type_id': str(attribute_instance.type_id),
        'value': attribute_instance.value,
        'source_id': source_id
    }

    data = _json.dumps(data)

    return data


def deserialize_attribute_instance(data, attribute_instance):
    """
    Populates `attribute_instance` with values extracted from `data`.

    Args:
        data (str): Raw JSON string containing ``AttributeInstance`` data.
        attribute_instance (AttributeInstance): An ``AttributeInstance``
            instance to be populated with `data`.

    Returns:
        None
    """
    data = _json.loads(data)

    id = data['id']
    type_id = data['type_id']
    value = data['value']
    source_id = data['source_id']

    attribute_instance.id = id
    attribute_instance.type_id = type_id
    attribute_instance.value = value
    attribute_instance.source_id = source_id


def serialize_filter_instance(filter_instance):
    """
    Extracts data from `filter_instance` into a JSON string.

    Args:
        filter_instance (FilterInstance): The ``FilterInstance``
            instance to be serialized.

    Returns:
        str: Raw JSON string containing `filter_instance` data.
    """
    data = {
        'type': type(filter_instance).__name__,
        'id': str(filter_instance.id),
        'type_id': str(filter_instance.type_id),
        'kind_params': filter_instance.kind_params
    }

    data = _json.dumps(data)

    return data


def deserialize_filter_instance(data, filter_instance):
    """
    Populates `filter_instance` with values extracted from `data`.

    Args:
        data (str): Raw JSON string containing ``FilterInstance`` data.
        filter_instance (FilterInstance): An ``FilterInstance`` instance to be
            populated with `data`.

    Returns:
        None
    """
    data = _json.loads(data)

    id = data['id']
    type_id = data['type_id']
    kind_params = data['kind_params']

    filter_instance.id = id
    filter_instance.type_id = type_id
    filter_instance.kind_params = kind_params


def serialize_view_instance(view_instance):
    """
    Extracts data from `view_instance` into a JSON string.

    Args:
        view_instance (ViewInstance): The ``ViewInstance``
            instance to be serialized.

    Returns:
        str: Raw JSON string containing `ViewInstance` data.
    """
    data = {
        'type': type(view_instance).__name__,
        'id': str(view_instance.id),
        'type_id': str(view_instance.type_id),
        'filter_ids': [str(f_id) for f_id in view_instance.filter_ids],
        'result_id': str(view_instance.result_id)
    }

    data = _json.dumps(data)

    return data


def deserialize_view_instance(data, view_instance):
    """
    Populates `view_instance` with values extracted from `data`.

    Args:
        data (str): Raw JSON string containing ``ViewInstance`` data.
        view_instance (ViewInstance): An ``ViewInstance`` instance to be
            populated with `data`.

    Returns:
        None
    """
    data = _json.loads(data)

    id = data['id']
    type_id = data['type_id']
    filter_ids = data['filter_ids']
    result_id = data['result_id']

    view_instance.id = id
    view_instance.type_id = type_id
    view_instance.filter_ids = filter_ids
    view_instance.result_id = result_id


def bind_to_controller(controller):
    controller.serializer('ContentType', 'json')(serialize_content_type)
    controller.serializer('AttributeType', 'json')(serialize_attribute_type)
    controller.serializer('FilterType', 'json')(serialize_filter_type)
    controller.serializer('ViewType', 'json')(serialize_view_type)
    controller.serializer('ContentInstance', 'json')(serialize_content_instance)
    controller.serializer('AttributeInstance', 'json')(serialize_attribute_instance)
    controller.serializer('FilterInstance', 'json')(serialize_filter_instance)
    controller.serializer('ViewInstance', 'json')(serialize_view_instance)

    controller.deserializer('ContentType', 'json')(deserialize_content_type)
    controller.deserializer('AttributeType', 'json')(deserialize_attribute_type)
    controller.deserializer('FilterType', 'json')(deserialize_filter_type)
    controller.deserializer('ViewType', 'json')(deserialize_view_type)
    controller.deserializer('ContentInstance', 'json')(deserialize_content_instance)
    controller.deserializer('AttributeInstance', 'json')(deserialize_attribute_instance)
    controller.deserializer('FilterInstance', 'json')(deserialize_filter_instance)
    controller.deserializer('ViewInstance', 'json')(deserialize_view_instance)