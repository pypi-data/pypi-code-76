import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('E000'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True    
def getSeatBelt():
    global SuccessFresh
    if not SuccessFresh:
        return False,False
    temp=DFL168A.ReturnStr[6:8]
    temp=int(temp,16) 
    temp=temp>>6
    if temp==1:
        buckled=True
    elif temp==0:
        buckled=False
    else:
        buckled=False
        return False,buckled
    return True, buckled        
