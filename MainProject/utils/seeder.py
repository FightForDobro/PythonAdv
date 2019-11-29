import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.models import (Category,
                           Product,
                           News,
                           Texts)
import lorem
from random import choice, randint
from scripts import default_photo


def category_seeder():

    categories = ['VIDEO GAMES', 'MOVIE', 'MUSIC']

    for category in categories:

        category_dict = {
            'title': category,
            'description': lorem.sentence()
        }

        Category(**category_dict).save()

    sub_categories = [{'VIDEO GAMES': 'PC'}, {'VIDEO GAMES': 'XBox'}, {'VIDEO GAMES': 'PlayStation'}]

    for i in sub_categories:
        for k, v in i.items():

            subcategory_dict = {
                'title': v,
                'description': lorem.sentence()
            }

            subcategory = Category(**subcategory_dict).save()

            Category.objects(title=k).get().add_subcategory(subcategory)

    sub_category = {
        'title': 'Action',
        'description': lorem.sentence()
    }
    subsub_c = Category(**sub_category).save()
    Category.objects(title='PC').get().add_subcategory(subsub_c)


def product_seeder(amount):

    games_names = ['DOOM', 'DIABLO', 'DOTA', 'GTA', 'Rust', 'Grad', 'Need For Speed', 'The legend of Zelda',
                   'Half-Life', 'BioShock', 'The Witcher', 'Portal', 'Tetris', 'Mario', 'Halo']

    movies_names = ['Hunters of the Forest', 'Girl in pink', 'Wolf and Bear forest friends', 'Some movie', 'King'
                    'Queen of the mexico', 'Green Land', 'Rome The Empire', 'Yakudza', 'Ice Cold', 'The Beast']

    music = ['AppleMusic subscribe']

    p_dict = {
        'Action': games_names,
        'MOVIE': movies_names,
        'MUSIC': music
    }

    for _ in range(amount):

        price = randint(0, 100)

        category = choice(list(p_dict.keys()))

        product_dict = {
            'title': choice(p_dict[category]),
            'description': lorem.sentence(),
            'price': price,
            'new_price': price // 2,
            'is_discount': choice([True, False]),
            'category': Category.objects(title=category).get(),

        }

        product = Product(**product_dict)
        product.save()


def news_seeder(amount):

    for _ in range(amount):

        news_dict = {
            'title': lorem.sentence()[:15],
            'content': lorem.paragraph()[:255]
        }

        News(**news_dict).save()


def definitions_help():

    definition_help = {
        'Название': 'Нажмите на названия чтобы вывести карту продукта',
        'Цена': 'Нажмите на цену чтобы вывести старую цену продукта',
        'Удалить': 'Нажмите на красный знакчок чтобы удалить товар с корзины',
        'cart': 'Это общая цена всех товаров в корзине',  # TODO Попробовать добавить общую цену без скидок
        'product': 'Здесь указано ваще текущее положение нажимайте кнопки < или > для перемещения',
        'empty': 'Здесь нет товара',
        'login': 'Здесь ваш логин',
        'fullname': 'Здесь ваше имя в телеграмм',
        'phone': 'Здесь ваш телефон'
    }

    for t, b in definition_help.items():

        Texts(**{'title': t,
                 'body': b}).save()

category_seeder()
product_seeder(100)
news_seeder(8)




