from ctypes import *
from bangtal.singleton import *

from enum import Enum, auto

class EventID(Enum):
	ENTER_SCENE		        = 1
	LEAVE_SCENE		        = 2
	PICK_OBJECT		        = 3
	DROP_OBJECT		        = 4
	COMBINE_OBJECT          = 5
	DISMANTLE_OBJECT        = 6
	TIMER                   = 101
	KEYPAD                  = 102
	SOUND                   = 103

class MouseAction(Enum):
	CLICK			    	= 0
	DRAG_UP		        	= 1
	DRAG_DOWN			    = 2
	DRAG_LEFT			    = 3
	DRAG_RIGHT		        = 4

class GameOption(Enum):
	ROOM_TITLE              = 1
	INVENTORY_BUTTON        = 2
	MESSAGE_BOX_BUTTON      = 3

class KeyCode(Enum):
    KEY_NONE                = 0
    KEY_PAUSE               = auto()
    KEY_SCROLL_LOCK         = auto()
    KEY_PRINT               = auto()
    KEY_SYSREQ              = auto()
    KEY_BREAK               = auto()
    KEY_ESCAPE              = auto()
    KEY_BACK                = KEY_ESCAPE
    KEY_BACKSPACE           = auto()
    KEY_TAB                 = auto()
    KEY_BACK_TAB            = auto()
    KEY_RETURN              = auto()
    KEY_CAPS_LOCK           = auto()
    KEY_SHIFT               = auto()
    KEY_LEFT_SHIFT          = KEY_SHIFT
    KEY_RIGHT_SHIFT         = auto()
    KEY_CTRL                = auto()
    KEY_LEFT_CTRL           = KEY_CTRL
    KEY_RIGHT_CTRL          = auto()
    KEY_ALT                 = auto()
    KEY_LEFT_ALT            = KEY_ALT
    KEY_RIGHT_ALT           = auto()
    KEY_MENU                = auto()
    KEY_HYPER               = auto()
    KEY_INSERT              = auto()
    KEY_HOME                = auto()
    KEY_PG_UP               = auto()
    KEY_DELETE              = auto()
    KEY_END                 = auto()
    KEY_PG_DOWN             = auto()
    KEY_LEFT_ARROW          = auto()
    KEY_RIGHT_ARROW         = auto()
    KEY_UP_ARROW            = auto()
    KEY_DOWN_ARROW          = auto()
    KEY_NUM_LOCK            = auto()
    KEY_KP_PLUS             = auto()
    KEY_KP_MINUS            = auto()
    KEY_KP_MULTIPLY         = auto()
    KEY_KP_DIVIDE           = auto()
    KEY_KP_ENTER            = auto()
    KEY_KP_HOME             = auto()
    KEY_KP_UP               = auto()
    KEY_KP_PG_UP            = auto()
    KEY_KP_LEFT             = auto()
    KEY_KP_FIVE             = auto()
    KEY_KP_RIGHT            = auto()
    KEY_KP_END              = auto()
    KEY_KP_DOWN             = auto()
    KEY_KP_PG_DOWN          = auto()
    KEY_KP_INSERT           = auto()
    KEY_KP_DELETE           = auto()
    KEY_F1                  = auto()
    KEY_F2                  = auto()
    KEY_F3                  = auto()
    KEY_F4                  = auto()
    KEY_F5                  = auto()
    KEY_F6                  = auto()
    KEY_F7                  = auto()
    KEY_F8                  = auto()
    KEY_F9                  = auto()
    KEY_F10                 = auto()
    KEY_F11                 = auto()
    KEY_F12                 = auto()
    KEY_SPACE               = auto()
    KEY_EXCLAM              = auto()
    KEY_QUOTE               = auto()
    KEY_NUMBER              = auto()
    KEY_DOLLAR              = auto()
    KEY_PERCENT             = auto()
    KEY_CIRCUMFLEX          = auto()
    KEY_AMPERSAND           = auto()
    KEY_APOSTROPHE          = auto()
    KEY_LEFT_PARENTHESIS    = auto()
    KEY_RIGHT_PARENTHESIS   = auto()
    KEY_ASTERISK            = auto()
    KEY_PLUS                = auto()
    KEY_COMMA               = auto()
    KEY_MINUS               = auto()
    KEY_PERIOD              = auto()
    KEY_SLASH               = auto()
    KEY_0                   = auto()
    KEY_1                   = auto()
    KEY_2                   = auto()
    KEY_3                   = auto()
    KEY_4                   = auto()
    KEY_5                   = auto()
    KEY_6                   = auto()
    KEY_7                   = auto()
    KEY_8                   = auto()
    KEY_9                   = auto()
    KEY_COLON               = auto()
    KEY_SEMICOLON           = auto()
    KEY_LESS_THAN           = auto()
    KEY_EQUAL               = auto()
    KEY_GREATER_THAN        = auto()
    KEY_QUESTION            = auto()
    KEY_AT                  = auto()
    KEY_CAPITAL_A           = auto()
    KEY_CAPITAL_B           = auto()
    KEY_CAPITAL_C           = auto()
    KEY_CAPITAL_D           = auto()
    KEY_CAPITAL_E           = auto()
    KEY_CAPITAL_F           = auto()
    KEY_CAPITAL_G           = auto()
    KEY_CAPITAL_H           = auto()
    KEY_CAPITAL_I           = auto()
    KEY_CAPITAL_J           = auto()
    KEY_CAPITAL_K           = auto()
    KEY_CAPITAL_L           = auto()
    KEY_CAPITAL_M           = auto()
    KEY_CAPITAL_N           = auto()
    KEY_CAPITAL_O           = auto()
    KEY_CAPITAL_P           = auto()
    KEY_CAPITAL_Q           = auto()
    KEY_CAPITAL_R           = auto()
    KEY_CAPITAL_S           = auto()
    KEY_CAPITAL_T           = auto()
    KEY_CAPITAL_U           = auto()
    KEY_CAPITAL_V           = auto()
    KEY_CAPITAL_W           = auto()
    KEY_CAPITAL_X           = auto()
    KEY_CAPITAL_Y           = auto()
    KEY_CAPITAL_Z           = auto()
    KEY_LEFT_BRACKET        = auto()
    KEY_BACK_SLASH          = auto()
    KEY_RIGHT_BRACKET       = auto()
    KEY_UNDERSCORE          = auto()
    KEY_GRAVE               = auto()
    KEY_A                   = auto()
    KEY_B                   = auto()
    KEY_C                   = auto()
    KEY_D                   = auto()
    KEY_E                   = auto()
    KEY_F                   = auto()
    KEY_G                   = auto()
    KEY_H                   = auto()
    KEY_I                   = auto()
    KEY_J                   = auto()
    KEY_K                   = auto()
    KEY_L                   = auto()
    KEY_M                   = auto()
    KEY_N                   = auto()
    KEY_O                   = auto()
    KEY_P                   = auto()
    KEY_Q                   = auto()
    KEY_R                   = auto()
    KEY_S                   = auto()
    KEY_T                   = auto()
    KEY_U                   = auto()
    KEY_V                   = auto()
    KEY_W                   = auto()
    KEY_X                   = auto()
    KEY_Y                   = auto()
    KEY_Z                   = auto()
    KEY_LEFT_BRACE          = auto()
    KEY_BAR                 = auto()
    KEY_RIGHT_BRACE         = auto()
    KEY_TILDE               = auto()
    KEY_EURO                = auto()
    KEY_POUND               = auto()
    KEY_YEN                 = auto()
    KEY_MIDDLE_DOT          = auto()
    KEY_SEARCH              = auto()
    KEY_DPAD_LEFT           = auto()
    KEY_DPAD_RIGHT          = auto()
    KEY_DPAD_UP             = auto()
    KEY_DPAD_DOWN           = auto()
    KEY_DPAD_CENTER         = auto()
    KEY_ENTER               = auto()
    KEY_PLAY                = auto()

class GameImpl:
    _bt = None

    def __init__(self):
        self._bt = windll.LoadLibrary("bangtal")

    def startGame(self, scene):
        self._bt._startGame(scene)

    def enterScene(self, scene):
        self._bt._enterScene(scene)

    def endGame(self):
        self._bt._endGame()

    def createScene(self, name, file):
        return self._bt._createScene(name, file)

    def setSceneImage(self, scene, file):
        self._bt._setSceneImage(scene, file)

    def setSceneLight(self, scene, light):
        self._bt._setSceneLight(scene, c_float(light))

    def createObject(self, file):
        return self._bt._createObject(file)

    def setObjectImage(self, object, file):
        self._bt._setObjectImage(object, file)

    def locateObject(self, object, scene, x, y):
        self._bt._locateObject(object, scene, x, y)

    def scaleObject(self, object, scale):
        self._bt._scaleObject(object, c_float(scale))

    def showObject(self, object):
        self._bt._showObject(object)

    def hideObject(self, object):
        self._bt._hideObject(object)

    def pickObject(self, object):
        self._bt._pickObject(object)

    def dropObject(self, object):
        self._bt._dropObject(object)

    def defineCombination(self, object1, object2, object3):
        self._bt._defineCombination(object1, object2, object3)

    def getHandObject(self):
        return self._bt._getHandObject()

    def showMessage(self, message):
        self._bt._showMessage(message)

    def showKeypad(self, password, object):
        self._bt._showKeypad(password, object)

    def showImageViewer(self, file):
        self._bt._showImageViewer(file)

    def showAudioPlayer(self, file):
        self._bt._showAudioPlayer(file)

    def showVideoPlayer(self, file):
        self._bt._showVideoPlayer(file)

    def createSound(self, file):
        return self._bt._createSound(file)

    def playSound(self, sound, loop):
        self._bt._playSound(sound, loop)

    def stopSound(self, sound):
        self._bt._stopSound(sound)

    def createTimer(self, seconds):
        return self._bt._createTimer(c_float(seconds))

    def setTimer(self, timer, seconds):
        self._bt._setTimer(timer, c_float(seconds))

    def increaseTimer(self, timer, seconds):
        self._bt._increaseTimer(timer, c_float(seconds))

    def decreaseTimer(self, timer, seconds):
        self._bt._decreaseTimer(timer, c_float(seconds))

    def getTimer(self, timer):
        self._bt._getTimer.restype = c_float
        return self._bt._getTimer(timer)

    def startTimer(self, timer):
        self._bt._startTimer(timer)

    def stopTimer(self, timer):
        self._bt._stopTimer(timer)

    def showTimer(self, timer):
        self._bt._showTimer(timer)

    def hideTimer(self):
        self._bt._hideTimer()

    def setSceneCallback(self, callback):
        self._bt._setSceneCallback(callback)

    def setObjectCallback(self, callback):
        self._bt._setObjectCallback(callback)

    def setMouseCallback(self, callback):
        self._bt._setMouseCallback(callback)

    def setTimerCallback(self, callback):
        self._bt._setTimerCallback(callback)

    def setSoundCallback(self, callback):
        self._bt._setSoundCallback(callback)

    def setKeyboardCallback(self, callback):
        self._bt._setKeyboardCallback(callback)

    def setGameOption(self, option, value):
        self._bt._setGameOption(option.value, c_bool(value))

    def getGameOption(self, option):
        self._bt._getGameOption.restype = c_int32
        return bool(self._bt._getGameOption(option.value))

class GameServer(GameImpl, SingletonInstance):
    pass
