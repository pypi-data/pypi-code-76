import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FEF6'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  
def getIntakeManifoldPressure():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[2:4]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    IntakeManifoldPressure=temp*2  
    return True, IntakeManifoldPressure

def getIntakeManifoldTemp():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[4:6]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    IntakeManifoldTemp=temp-40  
    return True, IntakeManifoldTemp  

def getEngineAirInletPressure():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[6:8]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    EngineAirInletPressure=temp*2  
    return True, EngineAirInletPressure      

def getEngineExhaustGasTemp():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[12:14]+DFL168A.ReturnStr[10:12]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    EngineExhaustGasTemp=temp*0.03125-273.0
    return True, EngineExhaustGasTemp   

def getEngineAirFilterDiffPressure():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[8:10]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0.0
    EngineAirFilterDiffPressure=temp*0.05  
    return True, EngineAirFilterDiffPressure 