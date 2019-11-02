from mongoengine import *

a = connect('shop')


class Category(Document):

    title = StringField(max_length=32, required=True)
    description = StringField(max_length=128)


class Product(Document):

    title = StringField(max_length=128, required=True)
    price = IntField(required=True)
    accessibility = BooleanField(default=True)
    amount = IntField(default=0)
    views = IntField(default=0)
    category = ReferenceField(Category)


# print(a.collection.aggregate({
#   "$group": {
#     "_id": None,
#     "avg_bvc": {"$avg": "$price"}
#   }
# }))

# prods = Product.objects
#
# all_price = []
#
# for product in prods:
#
#     all_price.append(product.price)
#
# print(sum(all_price))
