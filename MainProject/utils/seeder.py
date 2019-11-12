from models.models import (Category,
                            Product,
                            News)
import lorem
from random import choice, randint


def category_seeder():

    # genres = ['Action', 'Adventure', 'Horror']
    #
    # for genre in genres:
    #
    #     genre_dict = {
    #         'title': genre,
    #         'description': lorem.sentence(),
    #         'is_root': False
    #     }

    categories = ['VIDEO GAMES', 'MOVIE', 'MUSIC']

    for category in categories:

        category_dict = {
            'title': category,
            'description': lorem.sentence(),
            'is_root': True
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


def product_seeder(amount):

    games_names = ['DOOM', 'DIABLO', 'DOTA']

    movies_names = ['Hunters of the Forest', 'Girl in pink', 'Wolf and Bear forest friends']

    music = ['AppleMusic subscribe']

    p_dict = {
        'PC': games_names,
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

        default_img = open('/home/ffd/Downloads/PythonAdv/MainProject/img/default.png', 'rb')

        product = Product(**product_dict)
        product.img.put(default_img, content_type='image/png/')
        product.save()

        default_img.close()



def news_seeder(amount):

    for _ in range(amount):

        news_dict = {
            'title': lorem.sentence()[:15],
            'content': lorem.paragraph()[:255]
        }

        News(**news_dict).save()


# category_seeder()
# product_seeder(7)
# news_seeder(8)

# subsub_cut_example = {
#     'title': 'Subcut of subcut',
#     'description': 'i am the lowest in the current hierarchy'
# }
#
# subsub_cut = Category(**subsub_cut_example).save()
#
#
# subcut_example = {
#     'title': 'Subcut of Root',
#     'description': 'i am subcut of Root',
#     'subcategory': [subsub_cut]
# }
#
# subcut = Category(**subcut_example).save()
#
# cat_example = {
#     'title': 'The root',
#     'description': 'Root directory',
#     'is_root': True,
#     'subcategory': [subcut]
# }
#
# Category(**cat_example).save()


# category_seeder()
# product_seeder(7)
# news_seeder(8)
