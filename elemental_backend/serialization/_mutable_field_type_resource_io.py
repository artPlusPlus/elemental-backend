from marshmallow import fields

from ._mutable_type_resource_io import MutableTypeResourceSchema


class MutableFieldTypeResourceSchema(MutableTypeResourceSchema):
    modifiers = fields.List(fields.String)
    kind_id = fields.String()

    kind_params_value_id = fields.UUID()
    default_value_id = fields.UUID()
