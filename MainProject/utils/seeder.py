from MainProject.models.models import (Category,
                                       Product,
                                       News)
import lorem
from random import choice, randint


def category_seeder():

    genres = ['Action', 'Adventure', 'Horror']
    categories = ['VIDEO GAMES', 'MOVIE', 'MUSIC']

    for category in categories:

        category_dict = {
            'title': category,
            'description': lorem.sentence()
        }

        Category(**category_dict).save()
    #
    # sub_categories = {'VIDEO GAMES': ['PC', 'XBOX', 'PlayStation']}
    #
    # for category in sub_categories:
    #
    #     for sub_category in category:
    #
    #         sub_category_dict = {
    #             'title': sub_category,
    #             'description': lorem.sentence()
    #
    #         }
    #
    #         sub_category = Category(**sub_category_dict).save()
    #
    #         Category.objects(title=category).get().add_subcategory(sub_category)
    #
    # categories = [{'VIDEO GAMES': [{'PC': genres},
    #                                {'XBOX': genres},
    #                                {'PlayStation': genres}
    #                                ]},
    #               {'MOVIES': genres},
    #               'MUSIC'
    #               ]
    # for category in categories:
    #     while type(category) == dict:
    #         for sub_category in category:
    #
    #             if type(sub_category) == dict:
    #                 while
    #
    #             sub_category_dict = {
    #                 'title': sub_category,
    #                 'description': lorem.sentence()
    #                 ''
    #             }
    #
    #         category_dict = {
    #             'title': category,
    #             'description': lorem.sentence(),
    #             'subcategory': sub_category
    #         }
    # root_status = categories
    #
    # while True:
    #
    #     for category in root_status:
    #
    #         category_dict = {
    #             'title': category,
    #             'description': lorem.sentence()
    #         }
    #
    #         if category == dict:
    #
    #
    #         if


def product_seeder(amount):

    games_names = ['DOOM', 'DIABLO', 'DOTA']

    movies_names = ['Hunters of the Forest', 'Girl in pink', 'Wolf and Bear forest friends']

    music = ['AppleMusic subscribe']

    p_dict = {
        'VIDEO GAMES': games_names,
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
            'category': category

        }

        Product(**product_dict).save()


def news_seeder(amount):

    for _ in range(amount):

        news_dict = {
            'title': lorem.sentence()[:15],
            'content': lorem.paragraph()[:255]
        }

        News(**news_dict).save()
