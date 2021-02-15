import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FEF1'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  
def getWheelBasedVehicleSpeed():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[4:6]+DFL168A.ReturnStr[2:4]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    WheelBasedVehicleSpeed=temp/256.0
    return True, WheelBasedVehicleSpeed

def getParkingBrake():
    global SuccessFresh
    if not SuccessFresh:
        return False,False
    temp=DFL168A.ReturnStr[0:2]
    temp=int(temp,16) 
    temp=(temp>>2) & 0x03
    if 0b01==temp:
        ParkingBrake=True
    elif 0b00==temp:
        ParkingBrake=False
    else:        
        return False,False    
    return True, ParkingBrake  

def getBrake():
    global SuccessFresh
    if not SuccessFresh:
        return False,False
    temp=DFL168A.ReturnStr[6:8]
    temp=int(temp,16) 
    temp=(temp>>4) & 0x03
    if 0b01==temp:
        BreakPedalDepressed=True
    elif 0b00==temp:
        BreakPedalDepressed=False
    else:        
        return False,False    
    return True, BreakPedalDepressed       