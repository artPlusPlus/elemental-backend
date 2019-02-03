from marshmallow import fields

from ._mutable_instance_resource_io import MutableInstanceResourceSchema


class MutableFieldInstanceResourceSchema(MutableInstanceResourceSchema):
    value_id = fields.UUID()
