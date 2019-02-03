from marshmallow import fields

from ._resource_io import ResourceSchema


class ImmutableTypeResourceSchema(ResourceSchema):
    label = fields.String()
    doc = fields.String()
