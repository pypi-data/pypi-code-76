# +---------------------------------------------------------------------------+
#
#      Program:    maxmotion.py
#
#      Purpose:    A daisy backend for the RC maxmotion camere sw
#
#      Target:     MULTIARCH
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
    #import rocket.daisy as daisy
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
	#daisy.sleep(1)
	global command
	if command is not None:	
		print ("Command:----------------- SENT --------------------------")
		print (command)
		print ("-----------------------------------------------------------")


# destroy function is called at Daisy shutdown
def destroy():
        deb.disconnect()


def Forward():
        global posTilt
        posTilt += 1
        global posPan
        Move(posPan, posTilt)


def TurnLeft():
        global posTilt
        global posPan
        posPan -= 1
        Move(posPan, posTilt)


def Reverse():
        global posTilt
        posTilt -= 1
        global posPan
        Move(posPan, posTilt)


def TurnRight():
        global posTilt
        global posPan
        posPan += 1
        Move(posPan, posTilt)


def Stop():
        global command
        global SIZE
        global posTilt
        posTilt = 0
        global posPan
        posPan = 0
        command = direction_converter.directionToArray("Stop")
        assert deb.send(command, SIZE) == OK


def WakeUp():
        global command
        global SIZE
        command = direction_converter.directionToArray("DI")
        assert deb.send(command, SIZE) == OK
        daisy.sleep(1)


def Move(P, T):
        global command
        global SIZE
        command = direction_converter.directionToJoystick("PT", P, T)
        assert deb.send(command, SIZE) == OK

#test of the byte transformation beside the command interface
allDirections = [-1,-10,-15,-20,-25,-50,-100,-255,1,10,15,20,25,50,100,255]
for x in range(0, len(allDirections), 1):
   print(allDirections[x])
   Move(allDirections[x],0)
