from threading import Thread
from time import sleep
from inspect import stack


def decorator(is_daemon: bool):

    def actual_decorator(func):
        thread_name = str(func)

        def wrapper(*args, **kwargs):

            t = Thread(target=func, args=args, kwargs={**kwargs}, daemon=is_daemon, name=thread_name)
            t.start()

        return wrapper
    return actual_decorator


@decorator(False)
def func_func():
    print(f'Thread {stack()[0][3]} start')
    for _ in range(10):
        print('i am func')
        sleep(0.2)
    print(f'Thread {stack()[0][3]} finish')


def func_func2():

    print('Main thread start')
    for _ in range(10):
        print('1')
        sleep(0.2)
    print('Main thread finish')


if __name__ == '__main__':
    func_func()
    func_func2()

