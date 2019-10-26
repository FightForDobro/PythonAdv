from mongoengine import *
from datetime import datetime


connect('test_db')


class User(Document):

    first_name = StringField(max_length=128)
    surname = StringField(max_length=128)
    email = EmailField()
    birth_of_year = IntField()

    @property
    def posts(self):
        return Post.objects(user=self)  # ЭТО ОБДЕЖКТ ИД ТИПО КЛЮЧ

    @classmethod
    def create(cls, **kwargs):
        if kwargs.get('birth_of_year') < 2005:
            return ValidationError()

        cls(**kwargs).save()

    def create_post(self, **kwargs):
        kwargs.update(user=self)
        Post(**kwargs).save()

class Post(Document):

    title = StringField(max_length=512)
    body = StringField(max_length=4096)
    added_at = DateTimeField(default=datetime.now())
    user = ReferenceField(User)


# dict_user = {
#     'first_name': 'Jonh',
#     'surname': 'Jonhovich',
#     'email': 'SomeEmail@gmail.com',
#     'birth_of_year': 2000,
# }
#
# user = User(**dict_user).save()
#
# dict_post = {
#     'title': 'new_post1',
#     'body': 'text',
#     'user': user
#  }

# post = Post(**dict_post).save()

# users = User.objects(
#     first_name__in=['Jonh', 'Denys']).update(
#     email='NewMail@icloud.com'
# )  # GET возвращает обьект а objects quarry set

# for u in users:
#     print(u)
#     u.birth_of_year += 1000
#     print(u.birth_of_year)
#     u.save()

user = User.objects.first()

user.create_post(**{'title': 'new', 'body': 'Hello'})
user.create_post(**{'title': 'VeryNew', 'body': 'Hello Privet'})