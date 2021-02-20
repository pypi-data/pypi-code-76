from bangtal.singleton import *
from bangtal.game import *

@CFUNCTYPE(None, c_int32, c_int32)
def sceneCallback(scene, event):
    s = SceneManager.instance().getScene(scene)
    if event == EventID.ENTER_SCENE.value:
        SceneManager.instance().setCurrentScene(scene)
        s.onEnter()
    elif event == EventID.LEAVE_SCENE.value:
        s.onLeave()

@CFUNCTYPE(None, c_int32, c_int32)
def keyboardCallback(key, state):
    s = SceneManager.instance().getCurrentScene()
    s.onKeyboard(KeyCode(key), state == 1)

class SceneManagerImpl:
    __list = {}
    __currentScene = None

    def __init__(self):
        global sceneCallback, keyboardCallback
        GameServer.instance().setSceneCallback(sceneCallback)
        GameServer.instance().setKeyboardCallback(keyboardCallback)

    def register(self, id, scene):
        self.__list[id] = scene

    def getScene(self, id):
        return self.__list[id]

    def setCurrentScene(self, id):
        self.__currentScene = id

    def getCurrentScene(self):
        return self.getScene(self.__currentScene)

class SceneManager(SceneManagerImpl, SingletonInstance):
    pass


class Scene:
    @staticmethod
    def onEnterDefault(scene):
        pass

    @staticmethod
    def onLeaveDefault(scene):
        pass

    @staticmethod
    def onKeyboardDefault(scene, key, pressed):
        pass

    def __init__(self, name, file):
        id = GameServer.instance().createScene(name, file)
        SceneManager.instance().register(id, self)

        self._name = name
        self._file = file
        self.ID = id

    def __str__(self):
        return self._name

    def setImage(self, file):
        GameServer.instance().setSceneImage(self.ID, file)

    def setLight(self, light):
        GameServer.instance().setSceneLight(self.ID, light)

    def enter(self):
        GameServer.instance().enterScene(self.ID)

    def onEnter(self):
        Scene.onEnterDefault(self)

    def onLeave(self):
        Scene.onLeaveDefault(self)

    def onKeyboard(self, key, pressed):
        Scene.onKeyboardDefault(self, key, pressed)
