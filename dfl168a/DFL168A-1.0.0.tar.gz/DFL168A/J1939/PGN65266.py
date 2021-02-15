import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FEF2'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  

def getFuelRate():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[2:4]+DFL168A.ReturnStr[0:2]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    FuelRate=temp*0.05
    return True, FuelRate   

def getInstantFuelEconomy():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[6:8]+DFL168A.ReturnStr[4:6]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    InstantFuelEconomy=temp/512.0
    return True, InstantFuelEconomy       
def getAvgFuelEconomy():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[10:12]+DFL168A.ReturnStr[8:10]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    AvgFuelEconomy=temp/512.0
    return True, AvgFuelEconomy       

def getEngineThrottlePos():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[12:14]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0.0
    EngineThrottlePos=temp*0.4  #%
    return True, EngineThrottlePos
