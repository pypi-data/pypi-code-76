# +---------------------------------------------------------------------------+
#
#      Program:    direction_converter.py
#
#      Purpose:    translation table
#                  referenced by the RC Camera daisy adapter
#
#      Target:     am65x, sitara
#
#      Author:     Martin Shishkov
#
#      License:    GPL 3
# +---------------------------------------------------------------------------+

from enum import IntEnum
class directions(IntEnum):
    Stop	= 0
    PT	  	= 1


def directionToInt(direction):
    switcher = {
        "Stop"      	: directions.Stop,
        "PT" 		: directions.PT
    }
    return switcher.get(direction)

def directionToArray(direction):
    switcher = {
        "Stop"      	: [0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0],
        "DI" 		: [0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x1,0x0]
    }

    #high, low = byte >> 4, byte & 0x0F
    print ("Command:----------------- ", direction, " ------------------------")
    sequence = ("".join(hex(byte) for byte in switcher.get(direction)))
    sequence = sequence.replace("0x", "")
    sequence = sequence.upper()
    print (sequence)
    print ("-----------------------------------------------------------")
    return (sequence)

def directionToJoystick(direction, P : int, T : int):
    P = int(P)
    T = int(T)
    LP = 0 if abs(P) < 10 else abs(P) - 9
    LT = 0 if abs(T) < 10 else abs(T) - 9
    DP = 0 if P > 0 else 1
    DT = 0 if T > 0 else 1
    switcher = {
        "PT"      	: [DP, abs(P) % 10, LP, DT, abs(T) % 10, LT,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0],
    }

    #high, low = byte << 4, byte & 0x0F
    print ("Command:----------------- ", direction, " ------------------------")
    sequence = ("".join(hex(byte) for byte in switcher.get(direction)))
    sequence = sequence.replace("0x", "")
    sequence = sequence.upper()
    print (sequence)
    print ("-----------------------------------------------------------")
    return (sequence)


