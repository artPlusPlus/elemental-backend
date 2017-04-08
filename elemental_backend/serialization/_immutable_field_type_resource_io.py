from marshmallow import fields

from ._immutable_type_resource_io import ImmutableTypeResourceSchema


class ImmutableFieldTypeResourceSchema(ImmutableTypeResourceSchema):
    kind_id = fields.String()
    kind_params = fields.Dict()
