from ClassWork.Lesson10.classwork.models.user import Post, User, Teg
from random import choice
from names import (get_first_name, get_last_name)
import lorem



def db_spammer(amount, teg_list=None):

    if teg_list is None:
        teg_list = ['Science', 'Math', 'Style',
                    'Drugs', 'Tech', 'Linux']

    nickname = ['FightForDobro', 'iLikeIceCream', 'Yoda',
                'Albert Hoffman', 'Alexander Theodore Shulgin',
                'Timothy Francis Leary']

    if len(User.objects().to_json()) == 2:

        for i in nickname:

                user_dict = {

                    'nickname': i,
                    'name': get_first_name(),
                    'surname': get_last_name()

                }

                User(**user_dict).save()

    for _ in range(amount):

        teg_obj = Teg(teg_title=choice(teg_list))

        post_dict = {

                        'post_title': lorem.sentence(),
                        'content': lorem.paragraph(),
                        'teg': teg_obj,
                    }

        user = User.objects(nickname=choice(nickname)).get()

        user.create_post(**post_dict)

