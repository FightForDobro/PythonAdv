# class Cat:
#
#     CATS_CREATED = 0
#
#     def __init__(self, name, color):
#         self._name = name
#         self._color = color
#         Cat.CATS_CREATED += 1
#
#     def say_meow(self):
#         print('MeoW!')
#
#     def walk_around(self):
#         print('The cat walks around')
#
#     def eat(self):
#         print('Cat eats')
#
#     def who_am_i(self):
#         print(f'I am {self._name}')
#         print(f'My color is {self._color}')
#
#     def get_name(self):  # ЄТО ГЕТТЕР
#         return self._name
#
#     def set_name(self, name):  # ЄТО СЕТТЕР
#         self._name = name
#
#
# cat = Cat('Denys', 'White')
# cat1 = Cat('Katya', 'White')
#
# print(cat.get_name())
# print(cat1.get_name())
#
# print(f'Cat count = {Cat.CATS_CREATED}')
# Перменые и сами класи
#
#
# class GlobalVarExampleClass:
#
#     GLOBAL_VAR_VALUE = 1
#
#     def check_access_to_calss_var(self):
#         return self.GLOBAL_VAR_VALUE
#
#     def set_calss_var_value(self, value):
#
#         self.GLOBAL_VAR_VALUE = value
#
#
# obj = GlobalVarExampleClass()
# print(obj.check_access_to_calss_var())
# obj.set_calss_var_value(10)
# print(obj.check_access_to_calss_var())
# print(GlobalVarExampleClass.GLOBAL_VAR_VALUE)

class Vehicle:

    NUM_OF_DOORS = 4
    FUEL_TYPE = 'Petrol'

    def move(self):
        print('Car moving')

    def set_fuel(self, value):
        self._fuel += value

    def get_fuel(self):
        return self._fuel

    def get_brand(self):
        return self._brand

    def set_brand(self, value):
        self._brand = value

    def get_engine(self):
        return self._engine

    def set_engine(self, value):
        self._engine = value


class Car(Vehicle):

    def __init__(self, brand, engine):
        self._brand = brand
        self._engine = engine
        self._fuel = 0

    def move(self):
        print('Move speed is: 278 km/h')
        print('Audi move so fast Vzhyyyyyyy!')

    def __str__(self):
        return f'Brand is {self._brand} and engine is {self._engine}'


car = Car('audi', 'V12')
print(car.get_brand())
print(car.get_engine())
car.move()
print(car)


class Example:

    __slots__ = ('_name')  # Разрешает использовать только выбраные обьекты Название пременой

    def __init__(self, name):
        self._name = name


obj = Example('example object')

obj._name = 'new name'
obj.Coolvar = 1000
