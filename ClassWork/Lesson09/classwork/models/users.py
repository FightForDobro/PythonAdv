from mongoengine import *
import names
from random import randint, choice
from datetime import datetime

connect('user_db')


class Student(Document):

    student_id = IntField(required=True)
    name = StringField(min_length=1, max_length=128, required=True)
    surname = StringField(min_length=1, max_length=128, required=True)
    m_name = StringField(min_length=1, max_length=128, required=True)
    group = StringField(min_length=1, max_length=128, required=True)
    marks = ListField()
    curator = StringField(min_length=1, max_length=128, required=True)
    faculty = StringField(min_length=1, max_length=128, required=True)

    @classmethod
    def create_student(cls, **kwargs):

        kwargs['student_id'] = Student.objects.count() + 1

        if not kwargs:

            kwargs = {

                    'name': input('Student name --> '),
                    'surname': input('Student surname --> '),
                    'm_name': input('Student middle name --> '),
                    'group': input('Student group --> '),
                    'marks': [int(m) for m in input('Enter mark or separate by "," each mark\n').split(',')],
                    'curator': input('Student curator --> '),
                    'faculty': input('Student faculty --> ')

            }

        if type(kwargs['marks']) is not list:

            kwargs['marks'] = kwargs['marks'].split(',')

        cls(**kwargs).save()

    @classmethod
    def read_student(cls, student_id):

        try:
            return cls.objects(student_id=student_id).as_pymongo()

        except DoesNotExist:
            raise DoesNotExist()

    @classmethod
    def update_student(cls, **kwargs):

        try:
            return cls.objects(student_id=kwargs['student_id']).get().update(**kwargs)

        except DoesNotExist:
            raise DoesNotExist()

    @classmethod
    def delete_student(cls, student_id):
        try:
            return cls.objects(student_id=student_id).get().delete()

        except DoesNotExist:
            raise DoesNotExist()


def add_some_students(amount: int):

    groups = ['CS-50', 'CS-10', 'AD-255', 'CP-228']
    curators = ['Yoda', 'Darth Sidious', 'Snoke']
    faculties = ['Computer Science', 'ART Design', 'Chemistry and Physic']

    for _ in range(amount):

        name_surname = names.get_full_name().split(' ')
        m_names = name_surname[0][:3] + name_surname[1][:3:-1]
        marks = [randint(60, 101) for _ in range(10)]

        stud = {
                'student_id': Student.objects.count() + 1,
                'name': name_surname[0],
                'surname': name_surname[1],
                'm_name': m_names,
                'group': choice(groups),
                'marks': marks,
                'curator': choice(curators),
                'faculty': choice(faculties)
        }

        student = Student(**stud).save()

    return f'{amount} students added to db'

