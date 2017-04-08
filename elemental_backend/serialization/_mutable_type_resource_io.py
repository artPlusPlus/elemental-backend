from marshmallow import fields

from ._mutable_resource_io import MutableResourceSchema


class MutableTypeResourceSchema(MutableResourceSchema):
    label_value_id = fields.UUID()
    doc_value_id = fields.UUID()
