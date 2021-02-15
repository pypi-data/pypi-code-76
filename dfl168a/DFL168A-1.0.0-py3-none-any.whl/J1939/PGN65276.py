import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FEFC'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  
def getWasherFluidLevel():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[0:2]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0.0
    WasherFluidLevel=temp*0.4  # %
    return True, WasherFluidLevel

def getFuelLevel1():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[2:4]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0.0
    FuelLevel1=temp*0.4   #  %
    return True, FuelLevel1

def getFuelLevel2():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[12:14]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0.0
    FuelLevel2=temp*0.4   #  %
    return True, FuelLevel2    
