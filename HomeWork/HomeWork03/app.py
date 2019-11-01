from flask import (Flask,
                   request,
                   jsonify,
                   Response)

from models.product import Product
from schemes.product_scheme import ProductScheme
from flask_restful import Api
from res.poduct_res import ProductRes, PriceRes

app = Flask(__name__)
api = Api(app)

api.add_resource(ProductRes, '/category/',
                 '/category/<string:category>/<string:product>')

api.add_resource(PriceRes, '/prices/')

if __name__ == '__main__':
    app.run(debug=True)