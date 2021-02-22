import RPi.GPIO as GPIO
import time

devices = None
devicelist = {}
i = 0

def startposition(pos):
    global servopos
    servopos = 1
    servopos = 0.06 * pos
    servopos = servopos + 1
    servopos = round(servopos, 2)
    return servopos
        
        

def write(angle):
    servoangle = 1
    servoangle = 0.06 * angle
    servoangle = servoangle + 1
    servoangle = round(servoangle, 2)
    return servoangle
       
        
        





