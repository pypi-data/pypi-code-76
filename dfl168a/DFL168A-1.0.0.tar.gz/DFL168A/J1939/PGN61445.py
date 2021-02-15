import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('F005'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  
def getCurrentGear():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[6:8]
    temp=int(temp,16) 
    if temp>0xfb:
        return False,0
    CurrentGear=temp-125
    if 126==CurrentGear:
        CurrentGear=251
    return True, CurrentGear 
def getSelectedGear():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[0:2]
    temp=int(temp,16) 
    if temp>0xfb:
        return False,0
    SelectedGear=temp-125
    if 126==SelectedGear:
        SelectedGear=251
    return True, SelectedGear         