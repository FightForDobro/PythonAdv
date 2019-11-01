from marshmallow import (fields, Schema,
                         validate, ValidationError)


class TegScheme(Schema):

    teg_title = fields.String()


class UserScheme(Schema):

    nickname = fields.String()
    name = fields.String()
    surname = fields.String()
    post_count = fields.Integer()


class PostScheme(Schema):

    post_title = fields.String()
    content = fields.String()
    publish_date = fields.DateTime()
    views = fields.Integer()
    teg = fields.Nested(TegScheme)
    author = fields.Nested(UserScheme)

