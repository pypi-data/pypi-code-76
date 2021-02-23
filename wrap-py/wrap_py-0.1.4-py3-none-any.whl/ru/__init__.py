#set module language
import wrap_py
from wrap_py import _transl
_transl.set_lang("ru_RU")

#load pygame constants to use directly
from pygame.locals import *

#Say hi to user
wrap_py.say_hi()

#load modules for external usage
from wrap_py.ru import programma
from wrap_py.ru._event_handler_registrator import *

#init application
def podgotovka(tip_zapuska=wrap_py.SERVER_TYPE_THREAD):
    wrap_py.init(tip_zapuska)