import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FEEE'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  
def getCoolantTemperature():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[0:2]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    CoolantTemperature=temp-40
    return True, CoolantTemperature

def getFuelTemp():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[2:4]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    FuelTemp=temp-40
    return True, FuelTemp

def getOilTemp():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[6:8]+DFL168A.ReturnStr[4:6]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    OilTemp=temp*0.03125-273.0
    return True, OilTemp    