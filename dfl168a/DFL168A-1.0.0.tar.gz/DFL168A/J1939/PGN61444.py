import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('F004'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  
def getActualEngineTorque():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[4:6]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    ActualEngineTorque=temp-125
    return True, ActualEngineTorque
def getEngineSpeed():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[8:10] + DFL168A.ReturnStr[6:8]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    EngineSpeed=temp*0.125
    return True, EngineSpeed     