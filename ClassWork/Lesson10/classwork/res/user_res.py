from flask_restful import Resource
from flask import request, jsonify

from ClassWork.Lesson10.classwork.models.user import Post
from ClassWork.Lesson10.classwork.models.user import User
from ClassWork.Lesson10.classwork.schemes.user_scheme import PostScheme
from ClassWork.Lesson10.classwork.schemes.user_scheme import UserScheme


class UserRes(Resource):

    def get(self, nickname=None):

        if nickname:
            user = User.objects(nickname=nickname).get()
            Post.objects(author=user).update(inc__views=1)
            return PostScheme().dump(Post.objects(author=user), many=True)

        objects = User.objects
        return UserScheme().dump(objects, many=True)



class PostRes(Resource):

    def get(self, teg=None):

        if not teg:

            objects = Post.objects
            return PostScheme().dump(objects, many=True)

        return PostScheme().dump(Post.objects(teg__teg_title=teg), many=True)
