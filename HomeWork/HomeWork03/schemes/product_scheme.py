from marshmallow import (fields, Schema,
                         validate, ValidationError)


class CategoryScheme(Schema):

    title = fields.String()
    description = fields.String()


class ProductScheme(Schema):

    title = fields.String()
    price = fields.Integer()
    accessibility = fields.Boolean()
    amount = fields.Integer()
    views = fields.Integer()
    category = fields.Nested(CategoryScheme)


