from PythonAdv.ClassWork.Lesson10.models.workers import Person, Location


location_obj = Location(street='Khreschatik', city='Kyiv')
person_dict = {
    'name': 'Jonh',
    'surname': 'Lehnon',
    'age': 40,
    'experience': 400,
    'location': location_obj
}

Person(**person_dict).save()
