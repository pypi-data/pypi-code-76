# +---------------------------------------------------------------------------+
#
#      Program:    RC_car.py
#
#      Purpose:    daisy backend for the RC car, skidloader				
#      
#      Target:     ARMV61A
#
#      Author:     Martin Shishkov
#
#      License:    GPL 3
# +---------------------------------------------------------------------------+

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

import RC_car_direction_converter

if os.name == 'nt':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'standalone'))
    import mock_dataexchange as deb
    import mock_webiopi as webiopi
else:
    import webiopi
    import _DataExchangeBuffer as deb

SIZE = 15
OK = 0

scriptpath = os.path.dirname(os.path.realpath(__file__))
command = None


 
# setup function is automatically called at WebIOPi startup
def setup():
    assert deb.connect() == OK

# loop function is repeatedly called by WebIOPi 
def loop():
	webiopi.sleep(1)
	global command
	if command is not None:	
		print ("Command:----------------- SENT --------------------------")
		print (command)
		print ("-----------------------------------------------------------")
	

# destroy function is called at daisy shutdown
def destroy():
	deb.disconnect()


@daisy.macro
def Forward():
	global command
	global SIZE
	command = Combine(command, direction_converter.directionToArray("Ahead"))
	assert deb.send(command, SIZE) == OK

@daisy.macro
def TurnLeft():
	global command
	global SIZE
	command = Combine(command, direction_converter.directionToArray("Left"))
	assert deb.send(command, SIZE) == OK

@daisy.macro
def Reverse():
	global command
	global SIZE
	command = Combine(command, direction_converter.directionToArray("Backward"))
	assert deb.send(command, SIZE) == OK

@daisy.macro
def TurnRight():
	global command
	global SIZE
	command = Combine(command, direction_converter.directionToArray("Right"))
	assert deb.send(command, SIZE) == OK

@daisy.macro
def Stop():
	global command
	global SIZE
	command = direction_converter.directionToArray("Stop")
	assert deb.send(command, SIZE) == OK
	

@daisy.macro
def ArmUp():
	global command
	global SIZE
	command = Combine(command, direction_converter.directionToArray("ArmUp"))
	assert deb.send(command, SIZE) == OK
	
@daisy.macro
def ArmDown():
	global command
	global SIZE
	command = direction_converter.directionToArray("ArmDown")
	assert deb.send(command, SIZE) == OK
	
@daisy.macro
def TiltUp():
	global command
	global SIZE
	command = Combine(command, direction_converter.directionToArray("TiltUp"))
	assert deb.send(command, SIZE) == OK
	
	
@daisy.macro
def TiltDown():
	global command
	global SIZE
	command = direction_converter.directionToArray("TiltDown")
	assert deb.send(command, SIZE) == OK
	
@daisy.macro
def Lights():
	global command
	global SIZE
	command = Combine(command, direction_converter.directionToArray("Lights"))
	assert deb.send(command, SIZE) == OK

@daisy.macro
def FlashAll():
	global command
	global SIZE
	command = direction_converter.directionToArray("Parked")
	assert deb.send(command, SIZE) == OK
	webiopi.sleep(1)
	command = Combine(command,direction_converter.directionToArray("DI"))
	assert deb.send(command, SIZE) == OK
	webiopi.sleep(1)
	command = Combine(command, direction_converter.directionToArray("GG"))
	assert deb.send(command, SIZE) == OK
	webiopi.sleep(1)
	command = Combine(command,direction_converter.directionToArray("ER"))
	assert deb.send(command, SIZE) == OK

@daisy.macro	
def Move(L, R):
	global command
	global SIZE
	command = direction_converter.directionToJoystick("LR", L, R)
	assert deb.send(command, SIZE) == OK

#Parameter                  Byte number
DIRECTION_LEFT_WHEELS       = 0
SPEED_LEFT_WHEELS           = 1
DIRECTION_RIGHT_WHEELS      = 3
SPEED_RIGHT_WHEELS          = 4
ARM_POS                     = 6
TILT_POS                    = 9

def Combine(cmd1 :list, cmd2 :list):
        sum = []
        for x in range(0, len(cmd1), 1):
            sum.append(int(cmd1[x], 16) + int(cmd2[x], 16))

        sum[SPEED_LEFT_WHEELS] %= 0xFF
        sum[SPEED_RIGHT_WHEELS] %= 0xFF
        sum[ARM_POS] %= (0xC - 0x4)
        sum[TILT_POS] %= (0xC - 0x4)
        sequence = ("".join(hex(byte & 0x0F) for byte in sum))
        sequence = sequence.replace("0x", "")
        sequence = sequence.upper()
        return sequence




	#Byte number	Parameter
	#0	Drive direction left wheels, 0=forward, 1=backwards
	#1	Drive speed left wheels, range 0..255, 0=stop, 255=full speed (1st nibble)
	#2	Drive speed left wheels, range 0..255, 0=stop, 255=full speed (2nd nibble)
	#3	Drive direction right wheels, 0=forward, 1=backwards
	#4	Drive speed right wheels, range 0..255, 0=stop, 255=full speed (1st nibble)
	#5	Drive speed right wheels, range 0..255, 0=stop, 255=full speed (2nd nibble)
	#6	Shovel arm position, range 1382..2764 (1st nibble), details on handling tbd
	#7	Shovel arm position, range 1382..2764 (2st nibble), details on handling tbd
	#8	Shovel arm position, range 1382..2764 (3st nibble), details on handling tbd
	#9	Shovel tilting position, range 1382..2764 (1st nibble), details on handling tbd
	#10	Shovel tilting position, range 1382..2764 (2st nibble), details on handling tbd
	#11	Shovel tilting position, range 1382..2764 (3st nibble), details on handling tbd
	#12	Reserved for actor control (lights, camera on/on, sound module, etc.) (1st nibble)
	#13	Reserved for actor control (lights, camera on/on, sound module, etc.) (2st nibble)
	#14	CR (carriage return), ASCII 13, as telegram termination flag
