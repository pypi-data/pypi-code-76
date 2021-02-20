from bangtal.singleton import *
from bangtal.game import *

@CFUNCTYPE(None, c_int32)
def soundCallback(sound):
    s = SoundManager.instance().getSound(sound)
    s.onCompleted()

class SoundManagerImpl:
    __list = {}

    def __init__(self):
        global soundCallback
        GameServer.instance().setSoundCallback(soundCallback)

    def register(self, id, sound):
        self.__list[id] = sound

    def getSound(self, id):
        return self.__list[id]

class SoundManager(SoundManagerImpl, SingletonInstance):
    pass


class Sound:
    @staticmethod
    def onCompletedDefault(sound):
        pass

    def __init__(self, file):
        id = GameServer.instance().createSound(file)
        SoundManager.instance().register(id, self)
        self.ID = id

    def play(self, loop = False):
        GameServer.instance().playSound(self.ID, loop)

    def stop(self):
        GameServer.instance().stopSound(self.ID)

    def onCompleted(self):
        Sound.onCompletedDefault(self)

