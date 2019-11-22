from flask_restful import Resource
from flask import request

from models.models import (Category,
                           Product,
                           News)
from schemes.schemes import (CategoryScheme,
                             ProductScheme,
                             NewsScheme)


class CategoryRes(Resource):

    def get(self, c_id=None):

        if c_id:
            return CategoryScheme().dump(Category.objects(id=c_id).get())

        return CategoryScheme().dump(Category.objects, many=True)

    def post(self, c_id=None):

        if c_id:
            category = Category.objects(id=c_id).get()
            sub_category = Category(**request.json).save()

            category.add_subcategory(sub_category)

            return CategoryScheme().dump(sub_category)

        obj = Category(**request.json)
        obj.save()

        return CategoryScheme().dump(obj)

    def put(self, c_id):

        obj = Category.objects(id=c_id).get()
        obj.update(**request.json)

        return CategoryScheme().dump(obj.reload())

    def delete(self, c_id):  # FIXME Починить сделать так чтобы удалсяьс котигори парент и тд

        obj = Category.objects(id=c_id).get()

        if obj.parent:
            return {'ERROR': 'First delete child'}

        obj.delete()

        return {c_id: 'DELETED'}


class ProductRes(Resource):

    def get(self, p_id=None):

        if p_id:
            return ProductScheme().dump(Product.objects(id=p_id).get())

        return ProductScheme().dump(Product.objects, many=True)

    def post(self):

        category = request.json.pop('category')
        request.json['category'] = Category.objects(id=(category['id'])).get()
        obj = Product(**request.json)
        obj.save()

        return ProductScheme().dump(obj)

    def put(self, p_id):

        if request.json.get('category'):
            category = request.json.pop('category')
            request.json['category'] = Category.objects(id=(category['id'])).get()

        obj = Product.objects(id=p_id).get()
        obj.update(**request.json)

        return ProductScheme().dump(obj.reload())

    def delete(self, p_id):
        obj = Product.objects(id=p_id).get()
        obj.delete()

        return {p_id: 'DELETED'}



class NewsRes(Resource):

    def get(self, n_id=None):

        if n_id:
            return NewsScheme().dump(News.objects(id=n_id).get())

        return NewsScheme().dump(News.objects, many=True)

    def post(self):

        obj = News(**request.json).save()
        return NewsScheme().dump(obj)

    def put(self, n_id):

        obj = News.objects(id=n_id).get()
        obj.update(**request.json)

        return NewsScheme().dump(obj.reload())

    def delete(self, n_id):

        obj = News.objects(id=n_id).get()
        obj.delete()

        return {n_id: 'DELETED'}
