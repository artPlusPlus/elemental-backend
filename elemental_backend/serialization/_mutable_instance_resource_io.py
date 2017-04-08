from marshmallow import fields

from ._mutable_resource_io import MutableResourceSchema


class MutableInstanceResourceSchema(MutableResourceSchema):
    resource_type_id = fields.UUID()
