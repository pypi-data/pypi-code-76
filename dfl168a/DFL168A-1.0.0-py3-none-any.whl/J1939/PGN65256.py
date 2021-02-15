import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FEE8'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  
def getAltitude():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[14:16]+DFL168A.ReturnStr[12:14]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    Altitude=temp*0.125-2500.0
    return True, Altitude
def getNavBasedSpeed():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[6:8]+DFL168A.ReturnStr[4:6]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    BasedSpeed=temp/256.0
    return True, BasedSpeed   