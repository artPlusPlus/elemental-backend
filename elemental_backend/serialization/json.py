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
        'id': str(attribute_type.id),
        'name': str(attribute_type.name),
        'default_value': str(attribute_type.default_value),
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
        'id': str(content_instance.id),
        'type_id': str(content_instance.type_id),
        'attribute_instance_ids': [str(aid) for aid in
                                   content_instance.attribute_instance_ids]
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
    attribute_instance_ids = data['attribute_instance_ids']

    content_instance.id = id
    content_instance.type_id = type_id
    content_instance.attribute_instance_ids = attribute_instance_ids


def serialize_attribute_instance(attribute_instance):
    """
    Extracts data from `attribute_instance` into a JSON string.

    Args:
        attribute_instance (ContentInstance): The ``AttributeInstance``
            instance to be serialized.

    Returns:
        str: Raw JSON string containing `attribute_instance` data.

    """
    data = {
        'id': str(attribute_instance.id),
        'type_id': str(attribute_instance.type_id),
        'value': attribute_instance.value
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

    attribute_instance.id = id
    attribute_instance.type_id = type_id
    attribute_instance.value = value


def bind_json_serializers_to_controller(controller):
    controller.serializer()