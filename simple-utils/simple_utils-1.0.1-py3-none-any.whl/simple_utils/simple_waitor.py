import time
import queue

class Waiter():
    def __init__(self, items=[], count=0):
        if count == 0 and len(items) == 0:
            raise ValueError("items or count must be filled.")

        self.q = queue.Queue()

        if count == 0:
            for item in items:
                self.q.put(item)
        else:
            for index in range(count):
                self.q.put(index)

    def get(self):
        item = None
        while True:
            try:
                item = self.q.get(block=False)
            except:
                time.sleep(1)
            else:
                return item


    def put(self, item=""):
        self.q.put(item)
