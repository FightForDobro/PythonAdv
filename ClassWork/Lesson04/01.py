from abc import ABC, abstractmethod
from time import strftime


class Person(ABC):
    """
    Class describe simple Person
    """

    DATABASE = []

    def __init__(self, surname: str, name: str, birthday: int, faculty: str):
        """
        Function construct person
        :param surname: Person surname
        :param name: Person name
        :param birthday: Person birthday
        :param faculty: Person faculty
        """
        self._surname = surname
        self._name = name
        self._birthday = birthday
        self._age = self.get_age_in_current_year()
        self._faculty = faculty

        Person.DATABASE.append(self.__dict__)

    @abstractmethod
    def person_info(self):
        """
        Function prints person info
        """
        info = self.__dict__

        for key, value in info.items():
            print(f'{key.replace("_", "").capitalize()}: {value}')

    def get_age_in_current_year(self):
        """
        Function gets person age in current year
        :return: Age
        """
        return int(strftime('%Y')) - self._birthday

    @classmethod
    def get_person_in_current_age(cls, age_range_1: int, age_range_2: int):
        """
        Function prints person in current range
        :param age_range_1: Start
        :param age_range_2: End
        :return: Person in range
        :rtype: str
        """
        suitable_persons = []

        for i in cls.DATABASE:
            if age_range_1 <= i['_age'] <= age_range_2:
                suitable_persons.append(i['_surname'] + ' ' + i['_name'])

        return f'Your persons in range {age_range_1} to {age_range_2}:\n{suitable_persons}' or 'No person in range'


class Enrollee(Person):
    """
    Class describe enrolle
    """

    def __init__(self, surname, name, birthday, faculty):
        super().__init__(surname, name, birthday, faculty)

    def person_info(self):
        print('This is Enrollee')
        super().person_info()


class Student(Person):
    """
    Class describe student
    """

    def __init__(self, surname, name, birthday, faculty, course):
        super().__init__(surname, name, birthday, faculty)
        self._course = course

    def person_info(self):
        print('This is Student')
        super().person_info()


class Teacher(Person):
    """
    Class describe teacher
    """

    def __init__(self, surname, name, birthday, faculty, job_position, experience):
        super().__init__(surname, name, birthday, faculty)
        self._job_position = job_position
        self._experience = experience

    def person_info(self):

        print('This is Teacher')
        super().person_info()


denys = Student('Ushakov', 'Denys', 2000, 'Сybersecurity', '3')
maxim = Student('Kaznach', 'Maxim', 2001, 'Artist', '2')
koylan = Student('Marchinkevich', 'Koylan', 2002, 'Security', '1')
katya = Student('Shukhnina', 'Katya', 1999, 'Web Development', '5')
lydmila = Student('Borisovna', 'Lydminla', 1998, 'Law', '6')

denys.person_info()

print(Person.get_person_in_current_age(17, 18))



