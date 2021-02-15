import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FEEF'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  

def getFueDeliveryPressure():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[0:2]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    FueDeliveryPressure=temp*4
    return True, FueDeliveryPressure

def getEngineOilLevel():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[4:6]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0.0
    EngineOilLevel=temp*0.4   # %
    return True, EngineOilLevel  

def getEngineOilPressure():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[6:8]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    EngineOilPressure=temp*4  
    return True, EngineOilPressure       

def getEngineCoolantPressure():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[12:14]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    EngineCoolantPressure=temp*2  
    return True, EngineCoolantPressure 

def getEngineCoolantLevel():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[14:16]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0.0
    EngineCoolantLevel=temp*0.4  #%  
    return True, EngineCoolantLevel    