from marshmallow import Schema, fields, validate

class ProductInSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    description = fields.String(load_default="")

class ProductSchema(ProductInSchema):
    id = fields.Integer(dump_only=True)
