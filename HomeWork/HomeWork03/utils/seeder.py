from HomeWork.HomeWork03.models.product import (Product,
                                                 Category)
from random import randint, choice
import lorem


def seeder(amount):

    data = {

            'food': ['Apple', 'Meat', 'IceCream'],
            'drinks': ['Cola', 'Fanta', 'Sprite'],
            'clothes': ['Backpack', 'Jacket', 'Shoes'],

            }

    if len(Category.objects.to_json()) == 2:

        for i in data.keys():

            category_dict = {
                'title': i,
                'description': lorem.sentence()
            }

            Category(**category_dict).save()

    for _ in range(amount):

        title = choice(list(data.keys()))
        amount = randint(0, 100)

        product_dict = {
            'title': choice(data[title]),
            'price': randint(1, 100),
            'accessibility': bool(amount),
            'amount': amount,
            'category': Category.objects(title=title).get()
        }

        Product(**product_dict).save()


seeder(34)
