import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FEE0'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  
def getTripDistance():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[6:8]+DFL168A.ReturnStr[4:6]+DFL168A.ReturnStr[2:4]+DFL168A.ReturnStr[0:2]
    temp=int(temp,16) 
    if temp>0xfaffffff:
        return False,0.0
    TripDistance=temp*0.125
    return True, TripDistance
def getTotalDistance():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[14:16]+DFL168A.ReturnStr[12:14]+DFL168A.ReturnStr[10:12]+DFL168A.ReturnStr[8:10]
    temp=int(temp,16) 
    if temp>0xfaffffff:
        return False,0.0
    TotalDistance=temp*0.125
    return True, TotalDistance    