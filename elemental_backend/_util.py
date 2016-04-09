import uuid

import elemental_backend


NO_VALUE = object()


def process_uuid_value(value):
    if not value:
        result = None
    elif not isinstance(value, uuid.UUID):
        try:
            result = uuid.UUID(value)
        except (TypeError, ValueError):
            msg = 'Invalid uuid value: "{0}"'
            msg = msg.format(value)
            raise ValueError(msg)
    else:
        result = value

    return result


def process_uuids_value(value):
    result = value or list()

    if isinstance(value, str):
        result = [result]
    else:
        try:
            result = list(result)
        except TypeError:
            result = [result]

    result = [process_uuid_value(id) for id in result]

    seen = set()
    result = [
        id for id in result
        if id and not (id in seen or seen.add(id))
    ]

    return result


def process_resource_type_value(value):
    try:
        if issubclass(value, elemental_backend.resources.Resource):
            return value
    except TypeError:
        pass

    value = str(value).lower().strip().replace(' ', '')
    resource_types = {
        elemental_backend.resources.ContentType.__name__.lower(): elemental_backend.resources.ContentType,
        elemental_backend.resources.AttributeType.__name__.lower(): elemental_backend.resources.AttributeType,
        elemental_backend.resources.ContentInstance.__name__.lower(): elemental_backend.resources.ContentInstance,
        elemental_backend.resources.AttributeInstance.__name__.lower(): elemental_backend.resources.AttributeInstance,
    }
    try:
        return resource_types[value]
    except KeyError:
        return None


def process_data_format_value(value):
    if value:
        return str(value).lower().strip().replace(' ', '_')
    return None


def process_serializer_key(resource_type, data_format):
    resource_type = process_resource_type_value(resource_type)
    data_format = process_data_format_value(data_format)

    if resource_type and data_format:
        return resource_type, data_format
    return None


def process_deserializer_key(resource_type, data_format):
    resource_type = process_resource_type_value(resource_type)
    data_format = process_data_format_value(data_format)

    if resource_type and data_format:
        return resource_type, data_format

    return None


def process_handler_key(event, action, resource_type):
    resource_type = process_resource_type_value(resource_type)

    if event:
        return event, action, resource_type

    return None
