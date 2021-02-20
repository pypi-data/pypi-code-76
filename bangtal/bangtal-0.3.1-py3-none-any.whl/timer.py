from bangtal.singleton import *
from bangtal.game import *

@CFUNCTYPE(None, c_int32)
def timerCallback(timer):
    t = TimerManager.instance().getTimer(timer)
    t.onTimeout()

class TimerManagerImpl:
    __list = {}

    def __init__(self):
        global timerCallback
        GameServer.instance().setTimerCallback(timerCallback)

    def register(self, id, timer):
        self.__list[id] = timer

    def getTimer(self, id):
        return self.__list[id]

class TimerManager(TimerManagerImpl, SingletonInstance):
    pass


class Timer:
    @staticmethod
    def onTimeoutDefault(timer):
        pass

    def __init__(self, seconds):
        id = GameServer.instance().createTimer(seconds)
        TimerManager.instance().register(id, self)
        self.ID = id

    def set(self, seconds):
        GameServer.instance().setTimer(self.ID, seconds)

    def get(self):
        return GameServer.instance().getTimer(self.ID)

    def increase(self, seconds):
        GameServer.instance().increaseTimer(self.ID, seconds)

    def decrease(self, seconds):
        GameServer.instance().decreaseTimer(self.ID, seconds)

    def start(self):
        GameServer.instance().startTimer(self.ID)

    def stop(self):
        GameServer.instance().stopTimer(self.ID)

    def onTimeout(self):
        Timer.onTimeoutDefault(self)

