#TODO Спросить как переводать значения в обджект и как витаскивать все диктом

from mongoengine import *

connect('workers')


class Location(EmbeddedDocument):

    CITY_CHOICES = (
        ('Kyiv', 'Kyiv'),
        ('Kharkiv', 'Kharkiv'),
        ('Lviv', 'Lviv')
    )

    city = StringField(choices=CITY_CHOICES)
    street = StringField(max_length=256)


class Person(Document):

    name = StringField(max_length=64)
    surname = StringField(max_length=64)
    age = IntField()
    experience = IntField()
    location = EmbeddedDocumentField(Location)