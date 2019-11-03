from marshmallow import (fields, Schema,
                         validate, ValidationError)


class CategoryScheme(Schema):

    id = fields.String()
    title = fields.String()
    description = fields.String()


class ProductScheme(Schema):

    id = fields.String()
    title = fields.String()
    price = fields.Integer()
    accessibility = fields.Boolean()
    amount = fields.Integer()
    views = fields.Integer()
    category = fields.Nested(CategoryScheme)


