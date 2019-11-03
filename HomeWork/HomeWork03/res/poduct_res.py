from flask_restful import Resource
from flask import request, jsonify

from HomeWork.HomeWork03.models.product import Product, Category
from HomeWork.HomeWork03.schemes.product_scheme import ProductScheme, CategoryScheme


class ProductRes(Resource):

    def get(self, p_id=None):
        if p_id:
            Product.objects(id=p_id).update(inc__views=1)
            return ProductScheme().dump(Product.objects(id=p_id).get())

        return ProductScheme().dump(Product.objects, many=True)

    def post(self):
        category = request.json.pop('category')
        request.json['category'] = Category.objects(id=(category['id'])).get()
        obj = Product(**request.json)
        obj.save()

        return ProductScheme().dump(obj)

    def put(self, p_id):
        obj = Product.objects(id=p_id).get()
        obj.update(**request.json)

        return ProductScheme().dump(obj.reload())

    def delete(self, p_id):
        obj = Product.objects(id=p_id).get()
        obj.delete()

        return {p_id: 'DELETED'}


class CategoryRes(Resource):

    def get(self, c_id=None):
        if c_id:
            category = Category.objects(id=c_id).get()
            obj = Product.objects(category=category)
            return ProductScheme().dump(obj, many=True)

        return CategoryScheme().dump(Category.objects, many=True)

    def post(self):
        obj = Category(**request.json)
        obj.save()
        return CategoryScheme().dump(obj)

    def put(self, c_id):
        obj = Category.objects(id=c_id).get()
        obj.update(**request.json)
        return CategoryScheme().dump(obj.reload())

    def delete(self, c_id):
        obj = Category.objects(id=c_id).get()
        obj.delete()

        return {c_id: 'DELETED'}


class PriceRes(Resource):

    def get(self):

        pipeline = [
            {'$group': {'_id': '$title',

                        'TotalSum': {'$sum':
                                         {'$multiply': ['$price', '$amount']}
                                     }
                        }
             }
        ]

        data = Product.objects().aggregate(*pipeline)

        all_sum = {'total_sum': 0}

        data_to_json = list(data)

        for i in data_to_json:
            for v in i.values():

                if type(v) == int:
                    all_sum['total_sum'] += v

        return jsonify(data_to_json + [all_sum])

