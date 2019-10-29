from flask_restful import Resource
from flask import request, jsonify
from PythonAdv.PythonAdv.ClassWork.Lesson10.models.workers import Person
from PythonAdv.PythonAdv.ClassWork.Lesson10.schemes.workers_scheme import PersonSchema

class WorkerResources(Resource):

    def get(self, id=None):

        if not id:

            objects = Person.objects
            return PersonSchema().dump(objects, many=True)  # Может сеаридизовать куарисет

        return PersonSchema().dump(Person.objects(id=id).get())

    def post(self):
        return jsonify(**{'mothod': 'post'})

    def put(self, id):

        obj = Person.objects(id=id).get()
        obj.update(**request.json)  # Апдейт адейти куери сети адетй оне адпейти обьект

        return PersonSchema().dump(obj.reload())


    def delete(self):
        return jsonify(**{'mothod': 'delete'})