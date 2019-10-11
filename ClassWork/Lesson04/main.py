# # a = tuple([1, 2])
# #
# # print(type(int))
#
# my_class = type(
#     'ClassExample',
#     (),
#
#     {
#         'attr_1': 100,
#         'attr_2': 200,
#         'get_attr_1': lambda self: self.attr_1,  # Место селф может быить что угодно
#         'get_attr_2': lambda self: self.attr_2,
#
#     }
# )
#
#
# obj = my_class()
# print(obj.get_attr_2())
#
# class MyMetaClass(type):
#
#     def __new__(mcs, name, base, attrs):
#         print(name, base, attrs)
#
#         if attrs.get('FIELD1', 0) < 100:
#             attrs['FIELD1'] = 1000
#
#         if not attrs.get('verywellfield'):
#             attrs['verywellfield'] = 'my_value'
#
#         return super().__new__(mcs, name, base, attrs)
#
#
# class OurClass(metaclass=MyMetaClass):
#     FIELD1 = 1
#     FIELD2 = 2
#
#     def __init__(self, value):
#         self.value = value
#
#
# print(OurClass.FIELD1)
# print(OurClass.verywellfield)

# from abc import ABC, abstractmethod, ABCMeta
#
#
# # class Vehicle():
# #
# #     def move(self):
# #         print('Move')
# #
# #     def get_fuel(self):
# #         return self._fuel
# #
# # class Car(Vehicle):
# #
# #     def __init__(self, model, fuel=110):
# #         self._model = model
# #         self._fuel = fuel
# #
# #     def move(self):
# #         super().move()
# #
# #
# # Car('Audi').move()
# # print(Car('AudiRs').get_fuel())
# #
#
#
# class PropertyExample:
#
#     def __init__(self, arg1):
#         self._x = arg1
#
#     @property
#     def x(self):
#         return self._x
#
#     @x.setter
#     def x(self, value):
#         if value == 100:
#             raise ValueError()
#         self._x = value
#
#     @x.deleter
#     def x(self, value):
#         del self._x
#
#
# obj = PropertyExample(200)
#
# print(obj.x)
# obj.x = 2000
# print(obj.x)
#
#     def get_x(self):
#         return self._x
#
#     def set_x(self, value):
#         self.get_x()
#
#     x = property(get_x(), set_x())


# class DecoratorExample:
#
#     NUM = 0
#
#     def __init__(self):
#         self._value = 100
#
#     @classmethod
#     def increacse_num(cls, num):
#
#         cls.NUM += num
#
#     @classmethod
#     def get_num(cls):
#         return cls.NUM
#
#     @classmethod
#     def create_one_more(cls):
#         return cls()
#
#     @staticmethod
#     def print_func():
#         print('Im static')
#
#
# print(DecoratorExample().print_func())

# class Singleton(type):
#     instance = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls.instance:
#             cls.instance[cls] = super().__call__(*args, **kwargs)
#             return cls.instance[cls]
#
#         else:
#             raise Exception()
#
#
# class MyClass(metaclass=Singleton):
#     def __init__(self):
#         self._x = 100
#
#
# a = MyClass()
#
# print(Singleton.instance)
