# coding: utf-8
from multiprocessing import Queue, Process

q = Queue()
q.put(dict(a=1, b=3))


def a():
    q.put(dict(a=1, b=3))


def b():
    import time
    time.sleep(1)
    d = q.get()
    print(d)


if __name__ == '__main__':
    p = Process(target=a)
    p.start()

    Process(target=b).start()
