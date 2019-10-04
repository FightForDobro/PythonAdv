#
# class Example:
#
#     def __init__(self, x):
#         self._x = x
#
#     def get_x(self):
#         return self._x
#
#
#     def __add__(self, other):
#         return Example(
#             self.get_x() + other.get_x()
#         )
#
# a = Example(1)
# b = Example(2)
#
# print(a + b)


# def func1(a):
#     print('I am func1')
#     print(f'My arg is {a}')
#
#
#     def func2(b):
#         print('I am func2')
#         print(f'My arg is {b}')
#
#         def func3(c):
#             print('I am final func')
#             print(f'My arg is {c}')
#
#         return func3
#     return func2
#
# func1('a')('b')('c')

def decorator(num_of_repeats=1):

    def actual_decorator(func):

        def wrapper(*args, **kwargs):
            print('Started wrapping')

            for i in range(num_of_repeats):

                result = func(*args, **kwargs)

            print('Wrapped')
            return result, 'Wrapped'

        return wrapper
    return actual_decorator  # НЕ ЗАБИВАЙ СТАВИТЬ И УБИРАТЬ СКОБКИ ЕСЛИ Я НЕ ХОЧУ ВИЗИВАТЬ НЕ СТАВИТЬ СКОБКИ


@decorator(1)
def say_hello(name):
    return f'Hello {name}!'


print(say_hello('Denys'))

class SingletonExample:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)

            return cls._instance
        raise Exception('Instance already exists')

    def __init__(self):
        self._x = 10
        self._y = 100


a = SingletonExample()
b = SingletonExample()
a._x = 100

print(a._x)
print(b._x)