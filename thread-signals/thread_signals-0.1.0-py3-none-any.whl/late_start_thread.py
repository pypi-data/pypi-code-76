from threading import Thread, Event

class LateStartThread(Thread):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)

        self._start_event = Event()
        super().start()

    def start(self):
        self._start_event.set()

    def run(self):
        self._start_event.wait()
        super().run()

