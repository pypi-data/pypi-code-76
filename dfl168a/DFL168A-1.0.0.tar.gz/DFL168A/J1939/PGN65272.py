import time
import DFL168A
SuccessFresh=False
def refresh():
    global SuccessFresh
    if not DFL168A.DigitalCommand('FEF8'):
        SuccessFresh=False
        return False
    Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    DFL168A.ReturnStr=Temp
    SuccessFresh=True
    return True  

def getTransmissionOilLevel():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[2:4]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0.0
    TransmissionOilLevel=temp*0.4 
    return True, TransmissionOilLevel

def getTransmissionOilLevelHighLow():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[12:14]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0.0
    TransmissionOilLevelHighLow=temp*0.5-62.5 
    return True, TransmissionOilLevelHighLow   

def getTransmissionOilPressure():
    global SuccessFresh
    if not SuccessFresh:
        return False,0
    temp=DFL168A.ReturnStr[6:8]
    temp=int(temp,16) 
    if temp>0xfa:
        return False,0
    TransmissionOilPressure=temp*16 
    return True, TransmissionOilPressure   


def getTransmissionOilTemp():
    global SuccessFresh
    if not SuccessFresh:
        return False,0.0
    temp=DFL168A.ReturnStr[10:12]+DFL168A.ReturnStr[8:10]
    temp=int(temp,16) 
    if temp>0xfaff:
        return False,0.0
    TransmissionOilTemp=temp* 0.03125 - 273
    return True, TransmissionOilTemp   

