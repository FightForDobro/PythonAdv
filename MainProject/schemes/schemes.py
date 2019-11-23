from marshmallow import (fields, Schema,
                         validate, ValidationError)


class PropertiesScheme(Schema):
    pass


class LazyCatScheme(Schema):

    id = fields.String()
    title = fields.String()
    description = fields.String()
    parent = fields.Nested('self')


class CategoryScheme(LazyCatScheme):
    subcategory = fields.List(fields.Nested(LazyCatScheme))


class ProductScheme(Schema):

    id = fields.String()
    title = fields.String()
    description = fields.String()
    price = fields.Integer()
    new_price = fields.Integer()
    is_discount = fields.Boolean()
    properties = fields.Nested(PropertiesScheme)
    category = fields.Nested(CategoryScheme)
    img = fields.String()  # FIXME Как ставить file field


class NewsScheme(Schema):
    
    id = fields.String()
    title = fields.String()
    content = fields.String()
    date = fields.DateTime()



