
from bangtal.game import EventID
from bangtal.game import MouseAction
from bangtal.game import GameOption
from bangtal.game import KeyCode
from bangtal.game import GameServer
from bangtal.scene import Scene
from bangtal.object import Object
from bangtal.object import ObjectManager
from bangtal.timer import Timer
from bangtal.sound import Sound

class Game:
    pass

def startGame(scene):
    GameServer.instance().startGame(scene.ID)

def endGame():
    GameServer.instance().endGame()

def showTimer(timer):
    GameServer.instance().showTimer(timer.ID)

def hideTimer():
    GameServer.instance().hideTimer()

def showMessage(message):
    GameServer.instance().showMessage(message)

def showKeypad(password, object):
    GameServer.instance().showKeypad(password, object.ID)

def showImageViewer(file):
    GameServer.instance().showImageViewer(file)

def showAudioPlayer(file):
    GameServer.instance().showAudioPlayer(file)

def showVideoPlayer(file):
    GameServer.instance().showVideoPlayer(file)

def setGameOption(option, value):
    GameServer.instance().setGameOption(option, value)

def getGameOption(option):
    return GameServer.instance().getGameOption(option)