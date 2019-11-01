from flask import (Flask,
                   request,
                   jsonify,
                   Response)

from flask_restful import Api
from models.user import Post
from schemes.user_scheme import PostScheme
from res.user_res import UserRes
from res.user_res import PostRes


app = Flask(__name__)
api = Api(app)

api.add_resource(PostRes, '/blog/', '/blog/<string:teg>/')
api.add_resource(UserRes, '/user/', '/user/<string:nickname>/')

if __name__ == '__main__':
    app.run(debug=True)
