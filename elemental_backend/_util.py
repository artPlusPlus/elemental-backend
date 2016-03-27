import uuid


NO_VALUE = object()


def process_uuid_value(value):
    if not value:
        result = None
    elif not isinstance(value, uuid.UUID):
        try:
            result = uuid.UUID(value)
        except TypeError:
            raise ValueError(value)
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
