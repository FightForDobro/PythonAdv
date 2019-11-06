from mongoengine import *
from datetime import datetime


connect('web_shop_bot')


class Texts(Document):

    title = StringField(unique=True)
    body = StringField(max_length=4096)


class Properties(DynamicEmbeddedDocument):

    weight = FloatField(min_value=0)


class Category(Document):

    title = StringField(max_length=255, required=True)
    description = StringField(max_length=512)
    subcategory = ReferenceField('self')

    @property
    def is_parent(self):
        return bool(self.subcategory)

    @property
    def get_products(self, **kwargs):
        return Product.objects(category=self, **kwargs)

    def add_subcategory(self, obj):
        self.subcategory.append(obj)


class Product(Document):

    title = StringField(max_length=255)
    description = StringField(max_length=1024)
    price = IntField(min_value=0)
    new_price = IntField(min_value=0)
    is_discount = BooleanField(default=False)
    properties = EmbeddedDocumentField(Properties)
    category = ReferenceField(Category)

    @property
    def get_price(self):
        if self.is_discount:
            return str(self.new_price / 100)  # Добавить перечеркнутую надпись
        return str(self.price / 100)

    @classmethod
    def get_discount_product(cls, **kwargs):
        cls.objects(is_discount=True, **kwargs)


class News(Document):

    title = StringField(max_length=32)
    content = StringField(max_length=256)
    date = DateTimeField(default=datetime.now())


# news = {
#     'title': 'Мы открились!',
#     'content': 'Всем привет мы открили наш новй телегам шоп\n'
# }
#
# News(**news).save()
