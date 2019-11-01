from flask_restful import Resource
from flask import request, jsonify

from HomeWork.HomeWork03.models.product import Product, Category
from HomeWork.HomeWork03.schemes.product_scheme import ProductScheme, CategoryScheme


class ProductRes(Resource):

    def get(self, category=None, product=None):

        if category:

            if product:
                Product.objects(category__title=category,
                                title=product).update(inc__views=1)
                return ProductScheme().dump(Product.objects(
                    category__title=category, title=product
                ), many=True)

            return ProductScheme().dump(Product.objects(
                category__title=category), many=True)

        return ProductScheme().dump(Product.objects, many=True)


class PriceRes(Resource):

    def get(self):

        all_price = []

        for product in Product.objects:

            all_price.append(product.price)

        return sum(all_price)

