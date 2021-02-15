import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FEF7'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  

def getAlternatorVoltage():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[6:8]+DFL168A.ReturnStr[4:6]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    AlternatorVoltage=temp*0.05
    return True, AlternatorVoltage  
def getElectricalVoltage():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[10:12]+DFL168A.ReturnStr[8:10]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    ElectricalVoltage=temp*0.05
    return True, ElectricalVoltage      

def getBatteryVoltage():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[14:16]+DFL168A.ReturnStr[12:14]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    BatteryVoltage=temp*0.05
    return True, BatteryVoltage     