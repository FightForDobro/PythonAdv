from marshmallow import (fields, Schema,
                         validate, ValidationError)


class BytesField(fields.Field):

    def _validate(self, value):
        
        if not isinstance(value, bytes):
            raise ValidationError('Invalid type'
                                  f'Current type is: {type(value)}'
                                  f'Must be bytes')
        if value == b'':
            raise ValidationError('Invalid value')

    # def serialize(
    #     self,
    #     attr: str,
    #     obj: typing.Any,
    #     accessor: typing.Callable[[typing.Any, str, typing.Any], typing.Any] = None,
    #     **kwargs
    # ):
    #     value = self.get_value(obj, attr, accessor=accessor)
    #     print(value)
    #     return {'img': str(value)}


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
    img = BytesField(load_only=True)


class NewsScheme(Schema):
    
    id = fields.String()
    title = fields.String()
    content = fields.String()
    date = fields.DateTime()


class TextsScheme(Schema):
    
    id = fields.String()
    title = fields.String()
    body = fields.String()
