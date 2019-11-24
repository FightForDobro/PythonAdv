from threading import Thread
from time import sleep


def cron_decorator(func):

    def wrapper(*args):

        t = Thread(target=func, args=args)
        t.start()

        sleep(*args)
        return func

    return wrapper


# date = timedelta(days=2).total_seconds()
# date = timedelta(seconds=5)
# print(date)