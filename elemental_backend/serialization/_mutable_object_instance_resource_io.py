from marshmallow import fields

from ._mutable_instance_resource_io import MutableInstanceResourceSchema


class MutableObjectInstanceResourceSchema(MutableInstanceResourceSchema):
    field_instance_ids_value_id = fields.UUID()
