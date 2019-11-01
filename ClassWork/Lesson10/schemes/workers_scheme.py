from marshmallow import (fields, Schema,
                         validates, ValidationError)


class LocationSchema(Schema):
    city = fields.String()
    street = fields.String()


class PersonSchema(Schema):
    id = fields.String()
    name = fields.String()
    surname = fields.String()
    age = fields.Integer()
    experience = fields.Integer()
    location = fields.Nested(LocationSchema)

    @validates('age')
    def validate_age(self, value):
        if value > 65:
            raise ValidationError('The age must be less them 65')
