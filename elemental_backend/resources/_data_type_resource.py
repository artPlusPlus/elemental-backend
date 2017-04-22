from ._immutable_type_resource import ImmutableTypeResource


class DataTypeResource(ImmutableTypeResource):
    """
    Used by `ImmutableFieldTypes` to enable use of `ResourceReference` Fields.

    The `ResourceReference` Kind requires a compatible_resource_type_id.
    """
    pass
