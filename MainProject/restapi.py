from flask import Flask
from flask_restful import Api

from res.res import (CategoryRes,
                     ProductRes,
                     NewsRes,
                     TextsRes)


app = Flask(__name__)
api = Api(app)

api.add_resource(CategoryRes,  '/category/', '/category/<string:c_id>')
api.add_resource(ProductRes, '/product/', '/product/<string:p_id>')
api.add_resource(NewsRes, '/news/', '/news/<string:n_id>')
api.add_resource(TextsRes, '/text/', '/text/<string:t_id>')

app.run(debug=True)
