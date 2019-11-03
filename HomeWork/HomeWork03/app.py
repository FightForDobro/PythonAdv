from flask import (Flask,
                   request,
                   jsonify,
                   Response)

from models.product import Product
from schemes.product_scheme import ProductScheme
from flask_restful import Api
from res.poduct_res import ProductRes, PriceRes, CategoryRes

app = Flask(__name__)
api = Api(app)

api.add_resource(ProductRes, '/shop/', '/shop/<string:p_id>/')
api.add_resource(CategoryRes, '/category/', '/category/<string:c_id>/')
api.add_resource(PriceRes, '/prices/')

if __name__ == '__main__':
    app.run(debug=True)