from HomeWork.HomeWork03.models.product import (Product,
                                                 Category)
from random import randint, choice
import lorem


def shop_spamer(amount):

    data = {

            'food': ['Apple', 'Meat', 'IceCream'],
            'drinks': ['Cola', 'Fanta', 'Sprite'],
            'clothes': ['Backpack', 'Jacket', 'Shoes'],

            }
    for _ in range(amount):

        title = choice(list(data.keys()))
        amount = randint(0, 100)

        category_obj = Category(title=title,
                                description=lorem.sentence())

        product_dict = {
            'title': choice(data[title]),
            'price': randint(1, 100),
            'accessibility': bool(amount),
            'amount': amount,
            'category': category_obj
        }

        Product(**product_dict).save()


shop_spamer(34)
