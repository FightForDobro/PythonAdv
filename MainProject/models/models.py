from mongoengine import *
from datetime import datetime

connect('web_shop_bot')


class Texts(Document):

    title = StringField(unique=True)
    body = StringField(max_length=4096)
    category = StringField(max_length=32)


class Properties(DynamicEmbeddedDocument):
    pass


class Category(Document):

    title = StringField(max_length=255, required=True, unique=True)
    description = StringField(max_length=512)
    subcategory = ListField(ReferenceField('self', reverse_delete_rule=PULL))
    parent = ReferenceField('self', reverse_delete_rule=NULLIFY)

    @classmethod
    def get_root_categories(cls):
        return cls.objects(parent=None)

    @property
    def is_parent(self):
        return bool(self.subcategory)

    @property
    def is_root(self):
        return not bool(self.parent)

    @property
    def get_products(self, **kwargs):
        return Product.objects(category=self, **kwargs)

    def add_subcategory(self, obj):
        obj.parent = self
        obj.save()
        self.subcategory.append(obj)
        self.save()


class Product(Document):

    title = StringField(max_length=255)
    description = StringField(max_length=1024)
    price = IntField(min_value=0)
    new_price = IntField(min_value=0)
    is_discount = BooleanField(default=False)
    properties = EmbeddedDocumentField(Properties)
    category = ReferenceField(Category, reverse_delete_rule=NULLIFY)
    img = BinaryField()

    @property
    def get_price(self):
        if self.is_discount:
            return str(self.new_price / 100)  # Добавить перечеркнутую надпись
        return str(self.price / 100)

    @classmethod
    def get_discount_product(cls, **kwargs):
        return cls.objects(is_discount=True, **kwargs)

    def add_img(self, img):
        self.img = img
        self.save()


class News(Document):

    title = StringField(max_length=32)
    content = StringField(max_length=256)
    date = DateTimeField(default=datetime.now())


class User(Document):
    
    user_id = StringField()
    fullname = StringField()
    nickname = StringField()
    phone = StringField()
    active = BooleanField(default=True)

    @classmethod
    def create_user(cls, user_id, fullname, nickname, phone=None):

        user_dict = {
            'user_id': user_id,
            'fullname': fullname,
            'nickname': nickname,
            'phone': phone
        }

        cls(**user_dict).save().create_cart()

    @property
    def is_active(self):

        return self.active

    def create_cart(self):

        cart_obj = {
            'all_products': [],
            'owner': self
        }

        Cart(**cart_obj).save()

    def update_cart(self, obj):

        cart = Cart.objects(owner=self).get()

        cart.all_products.append(obj)

        cart.save()


class Cart(Document):

    all_products = ListField(ReferenceField(Product, reverse_delete_rule=PULL))
    owner = ReferenceField('User', reverse_delete_rule=CASCADE)


class UserMenuCounter(Document):

    owner = ReferenceField(User, reverse_delete_rule=CASCADE)
    counter = IntField(default=4)
    user_position = StringField(default='0')


class OrderHistory(Document):

    cart = ListField()
    full_price = IntField()
    owner = ReferenceField(User, reverse_delete_rule=CASCADE)
    datetime = DateField(default=datetime.now())
    status = StringField(default='В обработке')
