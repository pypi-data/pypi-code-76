# +---------------------------------------------------------------------------+
#
#      Program:    maxmotion.py
#
#      Purpose:    Daisy backend for the RC maxmotion camera sw
#
#      Target:     ARM64
#
#      Author:     Martin Shishkov
#
#      License:    GPL 3
# +---------------------------------------------------------------------------+

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

import direction_converter

if os.name == 'nt':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'standalone'))
    import mock_dataexchange as deb
    import mock_daisy as daisy
else:
    import rocket.daisy as daisy
    import _DataExchangeBuffer as deb

SIZE = 15
OK = 0
posPan = 0x1
posTilt = 0x1

scriptpath = os.path.dirname(os.path.realpath(__file__))
command = None



# setup function is automatically called at Daisy startup
def setup():
    assert deb.connect() == OK

# loop function is repeatedly called by Daisy
def loop():
        daisy.sleep(1)
        global command
        if command is not None:	
              print ("Command:----------------- SENT --------------------------")
              print (command)
              print ("-----------------------------------------------------------")


# destroy function is called at Daisy shutdown
def destroy():
        deb.disconnect()

@daisy.macro
def Forward():
        global posTilt
        posTilt += 1
        global posPan
        Move(posPan, posTilt)

@daisy.macro
def TurnLeft():
        global posTilt
        global posPan
        posPan -= 1
        Move(posPan, posTilt)

@daisy.macro
def Reverse():
        global posTilt
        posTilt -= 1
        global posPan
        Move(posPan, posTilt)

@daisy.macro
def TurnRight():
        global posTilt
        global posPan
        posPan += 1
        Move(posPan, posTilt)

@daisy.macro
def Stop():
        global command
        global SIZE
        global posTilt
        posTilt = 0
        global posPan
        posPan = 0
        command = direction_converter.directionToArray("Stop")
        assert deb.send(command, SIZE) == OK

@daisy.macro
def WakeUp():
        global command
        global SIZE
        command = direction_converter.directionToArray("DI")
        assert deb.send(command, SIZE) == OK
        daisy.sleep(1)

@daisy.macro
def Move(P, T):
        global command
        global SIZE
        command = direction_converter.directionToJoystick("PT", P, T)
        assert deb.send(command, SIZE) == OK


