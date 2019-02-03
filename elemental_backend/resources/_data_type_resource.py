from ._resource import Resource


class DataTypeResource(Resource):
    """
    Used by `ImmutableFieldTypes` to enable use of `ResourceReference` Fields.

    The `ResourceReference` Kind requires a compatible_resource_type_id.
    """
    pass
