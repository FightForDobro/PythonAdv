# TODO GETATTR SETATTR


from flask import (Flask,
                   request,
                   jsonify,
                   Response)

from .models.workers import Person
from .schemes.workers_scheme import PersonSchema
from flask_restful import Api
from .resources.worker_resources import WorkerResources

app = Flask(__name__)
api = Api(app)

api.add_resource(WorkerResources, '/workers/', '/workers/<string:id>/')


# @app.route('/', methods=['GET', 'POST'])
# def hello_world():
#
#     if request.method == 'GET':
#
#         obj = Person.objects.first()
#         return PersonSchema().dump(obj)
#
#     else:
#         validity = PersonSchema().validate(request.json)
#
#         if validity:
#             return validity
#         Person(**request.json).save()
#         return Response(status=201)

if __name__ == '__main__':
    app.run(debug=True)
