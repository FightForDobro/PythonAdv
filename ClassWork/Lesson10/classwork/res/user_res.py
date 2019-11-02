from flask_restful import Resource
from flask import request, jsonify

from ClassWork.Lesson10.classwork.models.user import Post, User, Teg
from ClassWork.Lesson10.classwork.schemes.user_scheme import PostScheme, UserScheme, TegScheme


class UserRes(Resource):

    def get(self, nickname=None):

        if nickname:
            user = User.objects(nickname=nickname).get()
            return PostScheme().dump(Post.objects(author=user), many=True)

        objects = User.objects
        return UserScheme().dump(objects, many=True)

    def post(self):

        obj = User(**request.json)
        obj.save()
        return UserScheme().dump(obj.reload())

    def put(self, nickname):

        obj = User.objects(nickname=nickname).get()
        obj.update(**request.json)

        return UserScheme().dump(obj.reload())

    def delete(self, nickname):

        obj = User.objects(nickname=nickname).get()
        obj.delete()

        return {nickname: 'DELETED'}

class PostRes(Resource):

    def get(self, p_id=None):

        if p_id:
            Post.objects(id=p_id).update(inc__views=1)
            return PostScheme().dump(Post.objects(id=p_id).get())

        return PostScheme().dump(Post.objects, many=True)

    def post(self):

        user_data = request.json[0].pop('author')
        user = User.objects(id=user_data['id']).get()
        user.create_post(**request.json[0])

        return {'Post create successful': request.json[0]}

    def put(self, p_id):

        obj = Post.objects(id=p_id).get()
        obj.update(**request.json)

        return PostScheme().dump(obj.reload())

    def delete(self, p_id):

        user_data = request.json[0].pop('author')
        user = User.objects(id=user_data['id']).get()
        user.delete_post(p_id)

        return {'Post deleted successful': request.json[0]}


class TegRes(Resource):

    def get(self, teg=None):

        if not teg:

            objects = Post.objects
            return PostScheme().dump(objects, many=True)

        return PostScheme().dump(Post.objects(teg__teg_title=teg), many=True)
