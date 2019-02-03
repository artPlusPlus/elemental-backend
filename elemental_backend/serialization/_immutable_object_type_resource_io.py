from marshmallow import fields

from ._immutable_type_resource_io import ImmutableTypeResourceSchema


class ImmutableObjectTypeResourceSchema(ImmutableTypeResourceSchema):
    extends_type_ids = fields.List(fields.UUID())
    field_type_ids = fields.List(fields.UUID())
