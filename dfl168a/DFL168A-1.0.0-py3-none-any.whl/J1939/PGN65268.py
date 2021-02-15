import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FEF4'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  

def getTirePressure():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[2:4]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    TirePressure=temp*4 
    return True, TirePressure

def getTireTemperature():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[6:8]+DFL168A.ReturnStr[4:6]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    TireTemperature=temp* 0.03125 - 273
    return True, TireTemperature   


def getTireLocation():
    global SuccessFresh
    if not SuccessFresh:
        return False,0,0
    temp=DFL168A.ReturnStr[0:2]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0,0
    Front2RearNumber = temp >> 4
    Left2RighNumber = temp & 0x0f
    return True, Front2RearNumber,Left2RighNumber

def getTireValvePressureMonitor():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[14:16]
    temp=int(temp,16) 
    if (temp & 0b11100000) == 0b11100000:
        return False,0
    TireValvePressureMonitor = temp >> 5
    return True, TireValvePressureMonitor