import logging


_LOG = logging.getLogger(__name__)


class ElementalError(Exception):
    @property
    def message(self):
        return self._message

    def __init__(self, message, inner_error=None):
        self._message = message
        self._inner_error = inner_error

    def __str__(self):
        return self._message


class DeserializerError(ElementalError):
    @property
    def deserializer_id(self):
        return self._deserializer_id

    def __init__(self, message, inner_error=None, deserializer_id=None):
        super(DeserializerError, self).__init__(
            message, inner_error=inner_error)

        self._deserializer_id = deserializer_id


class DeserializerNotFoundError(DeserializerError):
    pass


class SerializerError(ElementalError):
    @property
    def serializer_id(self):
        return self._serializer_id

    def __init__(self, message, inner_error=None, serializer_id=None):
        super(SerializerError, self).__init__(
            message, inner_error=inner_error)

        self._serializer_id = serializer_id


class SerializerNotFoundError(SerializerError):
    pass


class ResourceTypeError(ElementalError):
    @property
    def resource_type(self):
        return self._resource_type

    def __init__(self, message, inner_error=None, resource_type=None):
        super(ResourceTypeError, self).__init__(
            message, inner_error=inner_error)

        self._resource_type = resource_type


class ResourceTypeNotFoundError(ResourceTypeError):
    pass


class ResourceError(ElementalError):
    @property
    def resource_type(self):
        return self._resource_type

    @property
    def resource_id(self):
        return self._resource_id

    def __init__(self, message, inner_error=None,
                 resource_type=None, resource_id=None):
        super(ResourceError, self).__init__(
            message, inner_error=inner_error)

        self._resource_type = resource_type
        self._resource_id = resource_id


class ResourceNotFoundError(ResourceError):
    pass


class ResourceNotRegisteredError(ResourceError):
    pass


class ResourceCollisionError(ResourceError):
    pass


class ResourceNotDeletedError(ResourceError):
    pass


class ResourceNotReleasedError(ResourceError):
    pass


class ContentTypeImportError(ElementalError):
    pass


class ContentImportError(ElementalError):
    pass


class AttributeTypeCollisionError(ElementalError):
    pass


class AttributeCollisionError(ElementalError):
    pass


class UnknownAttributeTypeError(ElementalError):
    pass


class ElementalResourceNotFoundError(ElementalError):
    pass


class ContentTypeNotFoundError(ElementalResourceNotFoundError):
    pass


class ContentNotFoundError(ElementalResourceNotFoundError):
    pass
