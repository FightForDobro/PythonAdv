# class Example:
#
#     def __init__(self, arg1, arg2):
#         self._arg = arg1
#         self._arg2 = arg2
#
#     def __call__(self, *args, **kwargs):
#         print(self.__dict__)
#
# obj = Example(1, 2)
#
# obj()
#
# class Dec:
#
#     def __init__(self, f):
#         self._f = f
#
#     def __call__(self, *args, **kwargs):
#         print('sssss')
#         self._f()
#         print('sssfsf')
#
# @Dec
# def func():
#     print('Hello World!')
#
# func()

# new_list_var = [i for i in range(10)]
# print(new_list_var)
# $$$$$$$$$$$$$$$$$$$$
#       THREADS
# $$$$$$$$$$$$$$$$$$$$$

from threading import Thread
import time
import random
#
#
# def random_time_sleep(ti):
#     print('thread started')
#     time.sleep(random.randint(ti, 5))
#     print('thread ended')
#
#
# t = Thread(target=random_time_sleep, args=(5, ), kwargs={}, daemon=True)
# t.start()
#
# print('Main thread process .....')
#
# for _ in range(10):
#     print('Works')
#     t.join()
#     time.sleep(0.5)
#     print('Iteration ended')
#
#
#
#
# class MyThread(Thread):
#
#     def __init__(self, name, is_daemon):
#         super().__init__(name=name, daemon=is_daemon)
#
#     def run(self):
#
#         for i in range(5):
#             print('I am class Thread')
#             time.sleep(0.2)
#
#
# t = MyThread('name', False)
# t.start()
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$
#       CONTEXT MANAGER
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$
#
# with open('file.txt', 'w') as file:
#     file.write('str')
#
#
# class ContextManagerExample:
#
#     def __init__(self, a):
#         self._a = a
#         self._state = 'Active'
#
#     def __enter__(self):
#         print('You are in Context Manager')
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print('Exit Context Manager')
#         self._state = 'Inactive'
#
#     def process(self):
#         print('Processing data')
#
#
# obj = ContextManagerExample(10)
#
# print(obj._state)
# print(obj.process())
#
# with ContextManagerExample(10) as new_obj:
#     new_obj.process()
#
# print(new_obj._state)
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$
#           Shelve
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$
import shelve
#
filename = 'our_db'
#
# with shelve.open(filename) as db:
#     db['key'] = '1000'
#
# with shelve.open(filename) as db:
#     print(db.get('key'))  # db.items по нему можно итерироваться


def creat_user(username):

    with shelve.open(filename) as db:
        db.has_key(username)  # Если есть юзер експшен

        db[f'{username}_posts'] = ['post_1', 'post_2']


def add_post(username):

    with shelve.open(filename) as db:
        username = db.get(f'{username}_post')