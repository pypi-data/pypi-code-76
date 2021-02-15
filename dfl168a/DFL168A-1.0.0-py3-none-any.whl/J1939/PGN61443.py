import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('F003'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  
def getAccelPedalPosi1():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[2:4]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0.0
    AccelPedalPosi1=temp*0.4  
    return True, AccelPedalPosi1
def getAccelPedalPosi2():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[8:10]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0.0
    AccelPedalPosi2=temp*0.4  
    return True, AccelPedalPosi2

def getEnginePerLoadAtCurrSpeed():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[4:6]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    EnginePerLoadAtCurrSpeed=temp  
    return True, EnginePerLoadAtCurrSpeed    