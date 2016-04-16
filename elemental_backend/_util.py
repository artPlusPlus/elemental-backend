from elemental_core.util import (
    process_elemental_class_value,
    process_data_format_value
)


def process_serializer_key(resource_type, data_format):
    """
    Computes a hashable value based on a `Resource` type and data format.

    Args:
        resource_type (str or Resource): A `Resource` subclass.
        data_format (str): A valid data format label.

    Returns:
        Tuple(`Resource`, str) if successful, None otherwise.
    """
    resource_type = process_elemental_class_value(resource_type)
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
    resource_type = process_elemental_class_value(resource_type)
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
    resource_type = process_elemental_class_value(resource_type)

    if event:
        return event, action, resource_type

    return None
