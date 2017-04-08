from marshmallow import fields

from ._mutable_type_resource_io import MutableTypeResourceSchema


class MutableObjectTypeResourceSchema(MutableTypeResourceSchema):
    extends_type_ids_value_id = fields.UUID()
    field_type_ids_value_id = fields.UUID()
