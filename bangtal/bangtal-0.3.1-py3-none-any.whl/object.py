from bangtal.singleton import *
from bangtal.game import *

@CFUNCTYPE(None, c_int32, c_int32)
def objectCallback(object, event):
    o = ObjectManager.instance().getObject(object)
    if event == EventID.PICK_OBJECT.value:
        o.onPick()
    elif event == EventID.DROP_OBJECT.value:
        o.onDrop()
    elif event == EventID.COMBINE_OBJECT.value:
        o.onCombine()
    elif event == EventID.DISMANTLE_OBJECT.value:
        o.onDismantle()
    elif event == EventID.KEYPAD.value:
        o.onKeypad()

@CFUNCTYPE(None, c_int32, c_int32, c_int32, c_int32)
def mouseCallback(object, x, y, action):
    o = ObjectManager.instance().getObject(object)
    o.onMouseAction(x, y, MouseAction(action))

class ObjectManagerImpl:
    __list = {}

    def __init__(self):
        global objectCallback, mouseCallback
        GameServer.instance().setObjectCallback(objectCallback)
        GameServer.instance().setMouseCallback(mouseCallback)

    def register(self, id, object):
        self.__list[id] = object

    def getObject(self, id):
        if id > 0:
            return self.__list[id]
        return None

class ObjectManager(ObjectManagerImpl, SingletonInstance):
    pass


class Object:
    @staticmethod
    def onPickDefault(object):
        pass

    @staticmethod
    def onDropDefault(object):
        pass

    @staticmethod
    def onCombineDefault(object):
        pass

    @staticmethod
    def onDismantleDefault(object):
        pass

    @staticmethod
    def onMouseActionDefault(object,x, y, action):
        pass

    @staticmethod
    def onKeypadDefault(object):
        pass

    def __init__(self, file):
        id = GameServer.instance().createObject(file)
        ObjectManager.instance().register(id, self)

        self._file = file
        self.ID = id

    def setImage(self, file):
        GameServer.instance().setObjectImage(self.ID, file)

    def locate(self, scene, x, y):
        GameServer.instance().locateObject(self.ID, scene.ID, x, y)

    def setScale(self, scale):
        GameServer.instance().scaleObject(self.ID, scale)

    def inHand(self):
        return self.ID == GameServer.instance().getHandObject()

    def defineCombination(self, obj1, obj2):
        GameServer.instance().defineCombination(obj1.ID, obj2.ID, self.ID)

    def show(self):
        GameServer.instance().showObject(self.ID)

    def hide(self):
        GameServer.instance().hideObject(self.ID)

    def pick(self):
        GameServer.instance().pickObject(self.ID)

    def drop(self):
        GameServer.instance().dropObject(self.ID)

    def onPick(self):
        Object.onPickDefault(self)

    def onDrop(self):
        Object.onDropDefault(self)

    def onCombine(self):
        Object.onCombineDefault(self)

    def onDismantle(self):
        Object.onDismantleDefault(self)

    def onMouseAction(self, x, y, action):
        Object.onMouseActionDefault(self, x, y, action)

    def onKeypad(self):
        Object.onKeypadDefault(self)


