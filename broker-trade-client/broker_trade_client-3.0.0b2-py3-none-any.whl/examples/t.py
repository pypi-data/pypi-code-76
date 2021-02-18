import time
import random
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=2)


def func():
    sec = random.randint(10, 20) / 100.0
    time.sleep(sec)
    print("func ok after: %s" % sec)


def submit():
    qsize = executor._work_queue.qsize()
    if qsize > 0:
        print("qsize: %s" % qsize)
    else:
        executor.submit(func)
        print("submit ok")


if __name__ == '__main__':
    while True:
        submit()
        time.sleep(0.1)



