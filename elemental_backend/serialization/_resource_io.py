from marshmallow import Schema, fields


class ResourceSchema(Schema):
    id = fields.UUID()
