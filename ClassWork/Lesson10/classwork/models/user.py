from mongoengine import *
from datetime import datetime
import json


connect('blog')


class Teg(EmbeddedDocument):

    teg_title = StringField(max_length=12, default='NoTag')


class User(Document):

    nickname = StringField(max_length=128, required=True, unique=True)
    name = StringField(max_length=128, required=True)
    surname = StringField(max_length=128, required=True)
    post_count = IntField(default=0)

    def create_post(self, **kwargs):

        kwargs.update(author=self)
        Post(**kwargs).save()
        self.update(post_count=Post.objects(author=self).count())


class Post(Document):

    post_title = StringField(max_length=128, required=True)
    content = StringField(max_length=1028, required=True)
    publish_date = DateTimeField(default=datetime.now())
    views = IntField(default=0)
    teg = EmbeddedDocumentField(Teg)
    author = ReferenceField(User)


# username = User.objects(nickname='VariousPersonality').get()
# user = Post.objects(author=username)
#
# json_data = user.to_json()
#
# print(len(json.loads(json_data)))
# print(user.count())
#
# users = User.objects().to_json()
# if not users:
#     print(1)
#
#
# print(list(users))
# print(len(users))

