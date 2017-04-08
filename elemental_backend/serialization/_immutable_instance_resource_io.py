from marshmallow import fields

from ._immutable_resource_io import ImmutableResourceSchema


class ImmutableInstanceResourceSchema(ImmutableResourceSchema):
    type_id = fields.UUID()
