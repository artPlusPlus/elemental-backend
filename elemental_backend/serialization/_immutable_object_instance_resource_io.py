from marshmallow import fields

from ._immutable_instance_resource_io import ImmutableInstanceResourceSchema


class ImmutableObjectInstanceResourceSchema(ImmutableInstanceResourceSchema):
    field_instance_ids = fields.List(fields.UUID())
