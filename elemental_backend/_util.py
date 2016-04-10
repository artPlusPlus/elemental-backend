import uuid

import elemental_backend


NO_VALUE = object()


def process_uuid_value(value):
    """
    Processes a value into a UUID.

    Args:
        value (str or uuid): Data to process into a uuid.

    Returns:
        UUID if `value`, else None.

    Raises:
        ValueError: If `value` is not a UUID instance and cannot be converted
            into a UUID instance.
    """
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
    """
    Processes a sequence of values into a sequence of UUIDs.

    Args:
        value (List[str or uuid]): Sequence of values to process.

    Returns:
        List[uuid]: Sequence of unique UUID instances.

    Raises:
        TypeError: If any item in `value` is not a UUID instance and cannot
            be converted into a UUID instance.
    """
    result = value or list()

    if isinstance(value, str):
        result = [result]
    else:
        try:
            result = list(result)
        except TypeError:
            result = [result]

    valid_values = []
    invalid_values = []
    for id in result:
        try:
            id = process_uuid_value(id)
        except ValueError:
            invalid_values.append(id)
        else:
            valid_values.append(id)

    if invalid_values:
        invalid_values = ['"{0}"'.format(id) for id in invalid_values]
        invalid_values = ', '.join(invalid_values)
        msg = 'Invalid uuid values: {0}'
        msg = msg.format(invalid_values)
        raise ValueError(msg)

    seen = set()
    result = [
        id for id in valid_values
        if id and not (id in seen or seen.add(id))
    ]

    return result


def process_resource_type_value(value):
    """
    Processes a name into a `Resource` class.

    Args:
        value (str or `Resource`): Name of a `Resource` class.

    Returns:
        A `Resource` class if successful, None otherwise.
    """
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
    """
    Computes a standardized label for a data format.

    Args:
        value (str): Name of a data format

    Returns:
        Formatted string if successful, None otherwise.
    """
    if value:
        return str(value).lower().strip().replace(' ', '_')
    return None


def process_serializer_key(resource_type, data_format):
    """
    Computes a hashable value based on a `Resource` type and data format.

    Args:
        resource_type (str or Resource): A `Resource` subclass.
        data_format (str): A valid data format label.

    Returns:
        Tuple(`Resource`, str) if successful, None otherwise.
    """
    resource_type = process_resource_type_value(resource_type)
    data_format = process_data_format_value(data_format)

    if resource_type and data_format:
        return resource_type, data_format
    return None


def process_deserializer_key(resource_type, data_format):
    """
    Computes a hashable value based on a `Resource` type and data format.

    Args:
        resource_type (str or Resource): A `Resource` subclass.
        data_format (str): A valid data format label.

    Returns:
        Tuple(`Resource`, str) if successful, None otherwise.
    """
    resource_type = process_resource_type_value(resource_type)
    data_format = process_data_format_value(data_format)

    if resource_type and data_format:
        return resource_type, data_format

    return None


def process_handler_key(event, action, resource_type):
    """
    Computes a hashable value based on a `ControllerEvent`, `Action`,
        and `Resource` type.

    Args:
        event (ControllerEvents): A `ControllerEvents` value.
        action (Actions): A `Actions` value.
        resource_type (str or Resource): A `Resource` subclass.

    Returns:
        Tuple(ControllerEvent, Action, Resource) if successful, None otherwise.
    """
    resource_type = process_resource_type_value(resource_type)

    if event:
        return event, action, resource_type

    return None
