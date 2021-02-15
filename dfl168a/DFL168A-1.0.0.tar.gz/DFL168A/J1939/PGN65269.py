import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FEF5'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  

def getBarometricPressure():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[0:2]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0.0
    BarometricPressure=temp*0.5  #0.5kpa/bit
    return True, BarometricPressure

def getAmbientTemp():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[8:10]+DFL168A.ReturnStr[6:8]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    AmbientTemp=temp*0.03125-273.0
    return True, AmbientTemp   

def getInletTemp():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[10:12]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    InletTemp=temp-40  
    return True, InletTemp

def getRoadTemp():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[14:16]+DFL168A.ReturnStr[12:14]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    RoadTemp=temp*0.03125-273.0
    return True, RoadTemp  

def getCabInteriorTemp():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[4:6]+DFL168A.ReturnStr[2:4]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    CabInteriorTemp=temp*0.03125-273.0
    return True, CabInteriorTemp       

