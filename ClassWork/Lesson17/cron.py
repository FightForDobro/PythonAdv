from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()


@tl.job(interval=timedelta(seconds=1))
def check():
    print('check')


tl.start()

while True:
    pass
