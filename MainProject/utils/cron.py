from threading import Thread
from time import sleep
from datetime import timedelta


def cron_decorator(func):

    def wrapper(*args):

        while True:

            t = Thread(target=func, args=args)
            t.start()

            sleep(int(timedelta(days=1).total_seconds()))

        return func

    return wrapper



