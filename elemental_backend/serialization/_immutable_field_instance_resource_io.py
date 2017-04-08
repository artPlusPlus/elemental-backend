from marshmallow import fields

from ._immutable_instance_resource_io import ImmutableInstanceResourceSchema


class ImmutableFieldInstanceResourceSchema(ImmutableInstanceResourceSchema):
    data_id = fields.UUID()

