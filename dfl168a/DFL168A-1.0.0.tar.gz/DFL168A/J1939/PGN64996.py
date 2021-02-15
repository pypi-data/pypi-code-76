import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FDE4'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  
def getPayLoad():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[0:2]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    PayLoad=temp
    return True, PayLoad