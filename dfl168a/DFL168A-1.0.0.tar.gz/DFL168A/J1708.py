import time
import DFL168A
def getbyte(cmd, Sign=False):
    tryTimes=0
    while not DFL168A.DigitalCommand(cmd):
        tryTimes=tryTimes+1
        DFL168A.ATCommand('AT PC')
        DFL168A.ATCommand('AT TP D')
        if (tryTimes>=5) or DFL168A.SleepWarning: 
            return False, 0
    temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    if temp[0:2]!=cmd:
        return False, 0
    Result=int(temp[0:2],16)
    if Result<128:
        #single byte
        t= int(temp[2:4],16)  
        if Sign :
            if t>=128:
                t=t-256
    elif Result<192:
        #2 bytes
        t= int(temp[4:6]+temp[2:4],16)
        if Sign:
            if t>=32768: 
                t=t-65536
    else:
        #variable bytes
        ByteCount=int(temp[2:4],16)
        if ByteCount==1:
            #Single byte
            t=int(temp[4:6],16)
            if Sign :
                if t>=128:
                    t=t-256
        elif ByteCount==2:
            #2 bytes
            t= int(temp[6:8]+temp[4:6],16)
            if Sign:
                if t>=32768: 
                    t=t-65536
        elif ByteCount==4:
            #4 bytes
            t= int(temp[10:12]+temp[8:10]+temp[6:8]+temp[4:6],16)
            if Sign:
                if t>=2147483648:
                    t=t-4294967296
        else:
            return False,0
    return True, t
def getPhysical_float(cmd,scale,Sign=False):
    r,t=getbyte(cmd,Sign)
    t=t*scale
    return r,t
def getVIN():
    tryTimes=0
    while not DFL168A.DigitalCommand('ED'):
        tryTimes=tryTimes+1
        DFL168A.ATCommand('AT PC')
        DFL168A.ATCommand('AT TP D')
        if (tryTimes>=5) or DFL168A.SleepWarning:
            return False, 0
    temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    if temp[0:2]!='ED':
        return False, ''
    Vin=''    
    temp=temp[4:]
    for i in range(0,len(temp),2):
        onechar=temp[i:i+2] 
        onechar=int(onechar,16)
        Vin=Vin+chr(onechar)
    return True, Vin
def getDTC():
    tryTimes=0
    DTC_Num=0
    while False==DFL168A.ATCommand('AT H1'):
        pass
    while not DFL168A.DigitalCommand('C2'):
        tryTimes=tryTimes+1
        DFL168A.ATCommand('AT PC')
        DFL168A.ATCommand('AT TP D')
        if (tryTimes>=5)  or DFL168A.SleepWarning:
            while False==DFL168A.ATCommand('AT H0'):
                pass
            return False, 0,0,[],[],[],[],[],[]
        
    temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    MID=int(temp[0:2],16)
    if temp[2:4]!='C2':
        while False==DFL168A.ATCommand('AT H0'):
            pass
        return False, 0,MID,[],[],[],[],[],[]
    LEN=int(temp[4:6],16)
    temp=temp[6:]
    if (0==LEN) or (LEN!=len(temp)/2):
        while False==DFL168A.ATCommand('AT H0'):
            pass
        if 0!=LEN:
            return False, 0,MID,[],[],[],[],[],[]
        return True, 0,MID,[],[],[],[],[],[]
    #correct Data
    DataByte=[]    
    for i in range(0,LEN):        
        DataByte.append(int(temp[2*i:2*i+2],16))
    FMI=[]
    PID_SID=[]
    IsActive=[]
    IsPID=[]
    OccurrenceExist=[]
    OccurrenceCount=[]
    i=0
    while True:
        FMI.append(DataByte[i+1]&0x0F)   #b.4 to b.1
        if 0x20==(DataByte[i+1]&0x20):   #b.6
            #standard diagnostic code
            PID_SID.append(DataByte[i])  #a
        else:
            #expansion diagnostic code (PID or SID from page 2) 
            PID_SID.append(DataByte[i]+256)  #a
        if 0x40==(DataByte[i+1]&0x40):   #b.7
            #fault is not active
            IsActive.append(False) 
        else:
            #fault is active   
            IsActive.append(True)     
        if 0x10==(DataByte[i+1]&0x10):   #b.5
            #SID
            IsPID.append(False) 
        else:
            #PID   
            IsPID.append(True)
        if 0x80==(DataByte[i+1]&0x80):   #b.8
            #Occurrence Count included
            OccurrenceExist.append(True)
            OccurrenceCount.append(DataByte[i+2])   #c
            i=i+3
        else:
            #Occurrence Count NOT included
            OccurrenceExist.append(False)
            OccurrenceCount.append(0)   
            i=i+2
        DTC_Num=DTC_Num+1
        if i>=LEN-2:
            break
    while False==DFL168A.ATCommand('AT H0'):
        pass
    return True,DTC_Num,MID,PID_SID,IsPID,FMI,IsActive,OccurrenceExist,OccurrenceCount
def clearDTC(MID,PID_SID,IsPID):  #PID=195, and clear all fault related to MID
    ExtendedPID=False
    temp='{:02x}'.format(MID)
    cmd='C303'+temp
    if PID_SID>=256:
        ExtendedPID=True
        PID_SID=PID_SID-256
    temp='{:02x}'.format(PID_SID)
    cmd=cmd+temp
    if ExtendedPID:
        #Extendt PID/SID
        if IsPID:
            cmd=cmd+'8'
        else:
            cmd=cmd+'9'    
    else:
        #Standard PID/SID
        if IsPID:
            cmd=cmd+'A'
        else:
            cmd=cmd+'B' 
    tryTimes=0
    cmd=cmd+'0'
    while not DFL168A.DigitalCommand(cmd):  #pid=195
        tryTimes=tryTimes+1
        DFL168A.ATCommand('AT PC')
        DFL168A.ATCommand('AT TP D')
        if (tryTimes>=5)  or DFL168A.SleepWarning:
            return False
    temp=DFL168A.HandleResponse(DFL168A.ReturnStr) 
    #verify pid=196 which is respond from pid=195
    if temp[0:2]!='C4':
        return False 
    if int(temp[2:4],16)<2:
        return False
    temp=temp[4:]   
    byteD=int(temp[2:4],16)
    if  (byteD&0xC0)!=0x80:
        return False
    return True    

def getFaultDescription(MID,PID_SID,IsPID, FMI):  #PID=195
    FaultDescription=''
    ExtendedPID=False
    cmd='C303'
    cmd=cmd+'{:02x}'.format(MID)
    if PID_SID>=256:
        ExtendedPID=True
        PID_SID=PID_SID-256
    cmd=cmd+ '{:02x}'.format(PID_SID)   
    byteD=0X0F&FMI
    if ExtendedPID:
        #Extend PID/SID
        if IsPID:
            byteD=byteD+0xC0
        else:
            byteD=byteD+0xD0
    else:
        #standard PID/SID
        if IsPID:
            byteD=byteD+0xE0
        else:
            byteD=byteD+0xF0
    cmd=cmd+ '{:02x}'.format(byteD)  
    tryTimes=0
    while not DFL168A.DigitalCommand(cmd):  #pid=195
        tryTimes=tryTimes+1
        DFL168A.ATCommand('AT PC')
        DFL168A.ATCommand('AT TP D')
        if (tryTimes>=5)  or DFL168A.SleepWarning:
            return False,FaultDescription
    temp=DFL168A.HandleResponse(DFL168A.ReturnStr) 
    #get pid=196 which is respond from pid=195
    if temp[0:2]!='C4':
        return False,FaultDescription 
    if int(temp[2:4],16)<3:
        return False,FaultDescription
    temp=temp[4:]   
    byteD=int(temp[0:2],16)
    if  byteD!=PID_SID:
        return False,FaultDescription
    #control field    
    byteD=int(temp[2:4],16)
    if (byteD&0xC0)!=0xC0 :
        #Not: Get DTC description
        return False,FaultDescription
    if (byteD&0x0F)!=(FMI&0x0F):
        #wrong FMI
        return False,FaultDescription
        
    temp=temp[4:]
    for i in range(0,len(temp),2):
        onechar=temp[i:i+2] 
        onechar=int(onechar,16)
        FaultDescription=FaultDescription+chr(onechar)   
    return True, FaultDescription
def getPIDSIDDescription(MID,PID_SID,IsPID):  #PID=195
    PID_SID_Description=''
    ExtendedPID=False
    cmd='C303'
    cmd=cmd+'{:02x}'.format(MID)
    if PID_SID>=256:
        ExtendedPID=True
        PID_SID=PID_SID-256
    cmd=cmd+ '{:02x}'.format(PID_SID)   
    byteD=0
    if ExtendedPID:
        #Extend PID/SID
        if IsPID:
            byteD=byteD+0x0
        else:
            byteD=byteD+0x10
    else:
        #standard PID/SID
        if IsPID:
            byteD=byteD+0x20
        else:
            byteD=byteD+0x30
    cmd=cmd+ '{:02x}'.format(byteD)  
    tryTimes=0
    while not DFL168A.DigitalCommand(cmd):  #pid=195
        tryTimes=tryTimes+1
        DFL168A.ATCommand('AT PC')
        DFL168A.ATCommand('AT TP D')
        if (tryTimes>=5) or DFL168A.SleepWarning:
            return False,PID_SID_Description 
    temp=DFL168A.HandleResponse(DFL168A.ReturnStr) 
    #get pid=196 which is respond from pid=195
    if temp[0:2]!='C4':
        return False,PID_SID_Description 
    if int(temp[2:4],16)<3:
        return False,PID_SID_Description 
    temp=temp[4:]   
    byteD=int(temp[0:2],16)
    if  byteD!=PID_SID:
        return False,PID_SID_Description 
    #control field    
    byteD=int(temp[2:4],16)
    if (byteD&0xC0)!=0x00 :
        #Not: Get PID/SID description
        return False,PID_SID_Description 
            
    temp=temp[4:]
    for i in range(0,len(temp),2):
        onechar=temp[i:i+2] 
        onechar=int(onechar,16)
        PID_SID_Description =PID_SID_Description +chr(onechar)   
    return True, PID_SID_Description 
def getAirPressure():
    r,t=getPhysical_float(cmd='07',scale=4.14)  
    return r,t    
def getEngineOilPressure():
    r,t=getPhysical_float(cmd='13',scale=4.00)  
    return r,t      
def getEngineCoolantPressure():
    r,t=getPhysical_float(cmd='14',scale=2.00)  
    return r,t  
def getFuelLevel1():
    r,t=getPhysical_float(cmd='60',scale=0.5)  
    return r,t           

def getFuelLevel2():
    r,t=getPhysical_float(cmd='26',scale=0.5)  
    return r,t 
def getBarometricPressure():
    r,t=getPhysical_float(cmd='30',scale=0.6)  
    return r,t 
def getEngineThrottlePos():
    r,t=getPhysical_float(cmd='33',scale=0.4)  
    return r,t 
def getWasherFluidLevel():
    r,t=getPhysical_float(cmd='50',scale=0.5)  
    return r,t  
def getVehicleSpeed():
    r,t=getPhysical_float(cmd='54',scale=0.805)  
    return r,t
def getAccelPedalPosi1():
    r,t=getPhysical_float(cmd='5B',scale=0.4)  
    return r,t  
def getAccelPedalPosi2():
    r,t=getPhysical_float(cmd='1D',scale=0.4)  
    return r,t
def getAccelPedalPosi3():
    r,t=getPhysical_float(cmd='1C',scale=0.4)  
    return r,t
def getEngineLoad():
    r,t=getPhysical_float(cmd='5C',scale=0.5)  
    return r,t  
def getEngineOilLevel():
    r,t=getPhysical_float(cmd='62',scale=0.5)  
    return r,t  
def getCoolantTemperature():  #We still use °C even though definition: 0.0 to 255.0 °F, 1.0 °F, PID=110
    r,t=getPhysical_float(cmd='6E',scale=1.0)
    t=(t-32)/1.8      
    return r,t  
def getEngineCoolantLevel():
    r,t=getPhysical_float(cmd='6F',scale=0.5)  
    return r,t  
def getTransmissionOilLevel():
    r,t=getPhysical_float(cmd='7C',scale=0.5)  
    return r,t 
def getTransmissionOilLevelHighLow():
    r,t=getPhysical_float(cmd='7D',scale=0.473,Sign=True)  
    return r,t
def getTransmissionOilPressure():
    r,t=getPhysical_float(cmd='7F',scale=13.8)  
    return r,t
def getTransmissionOilTemp():  #We still use °C even though definition:
    r,t=getPhysical_float(cmd='B1',scale=0.25,Sign=True)
    t=(t-32)/1.8     
    return r,t 
def getPowerSpecificInstantFuelEconomy():
    r,t=getPhysical_float(cmd='82',scale=0.00197)  
    return r,t
def getAvgFuelRate():
    r,t=getPhysical_float(cmd='85',scale=0.000016428)  
    return r,t
def getInstantFuelEconomy():
    r,t=getPhysical_float(cmd='B8',scale=0.00166072)  
    return r,t
def getAvgFuelEconomy():
    r,t=getPhysical_float(cmd='B9',scale=0.00166072)  
    return r,t
def getElectricalVoltage():
    r,t=getPhysical_float(cmd='9E',scale=0.05)  
    return r,t
def getRatedEnginePower():
    r,t=getPhysical_float(cmd='A6',scale=0.745)  
    return r,t
def getBatteryVoltage():
    r,t=getPhysical_float(cmd='A8',scale=0.05)  
    return r,t
def getAlternatorVoltage():
    r,t=getPhysical_float(cmd='A7',scale=0.05)  
    return r,t
def getAmbientTemp():  #We still use °C even though definition:
    r,t=getPhysical_float(cmd='AB',scale=0.25,Sign=True)
    t=(t-32)/1.8     
    return r,t 
def getCargoAmbientTemp():  #We still use °C even though definition:
    r,t=getPhysical_float(cmd='A9',scale=0.25,Sign=True)
    t=(t-32)/1.8      
    return r,t 
def getRoadTemp():  #We still use °C even though definition:
    r,t=getPhysical_float(cmd='4F',scale=2.5,Sign=True)
    t=(t-32)/1.8     
    return r,t 
def getCabInteriorTemp():  #We still use °C even though definition:
    r,t=getPhysical_float(cmd='AA',scale=0.25,Sign=True)
    t=(t-32)/1.8      
    return r,t 
def getInletTemp():  #We still use °C even though definition:
    r,t=getPhysical_float(cmd='AC',scale=0.25,Sign=True)
    t=(t-32)/1.8     
    return r,t 
def getFuelTemp():  #We still use °C even though definition:
    r,t=getPhysical_float(cmd='AE',scale=0.25,Sign=True)
    t=(t-32)/1.8      
    return r,t 
def getOilTemp():  #We still use °C even though definition:
    r,t=getPhysical_float(cmd='AF',scale=0.25,Sign=True)
    t=(t-32)/1.8      
    return r,t 
def getCargoWeight():
    r,t=getPhysical_float(cmd='B5',scale=17.792)  
    return r,t
def getEngineTripFuel():
    r,t=getPhysical_float(cmd='B6',scale=0.473)  
    return r,t
def getEngineTotalFuelUsed():
    r,t=getPhysical_float(cmd='FA',scale=0.473)     
    return r,t
def getFuelRate():
    r,t=getPhysical_float(cmd='B7',scale=0.000016428)  
    return r,t
def getRatedEngineSpeed():
    r,t=getPhysical_float(cmd='BD',scale=0.25)  
    return r,t
def getEngineSpeed():
    r,t=getPhysical_float(cmd='BE',scale=0.25)  
    return r,t
def getIntakeManifoldTemp():  #We still use °C even though definition:
    r,t=getPhysical_float(cmd='69',scale=1.0)
    t=(t-32)/1.8     
    return r,t 
def getPowerTakeoffStatus():
    PTOModeActive=False
    ClutchSwitchOn=False
    BrakeSwitchOn=False
    AccelSwitchOn=False
    ResumeSwitchOn=False
    CoastSwitchOn=False
    SetSwitchOn=False
    PTOControlSwitchOn=False
    r,tempV=getbyte(cmd='59')
    if 0x80==(tempV&0x80):
        PTOModeActive=True
    if 0x40==(tempV&0x40):
        ClutchSwitchOn=True
    if 0x20==(tempV&0x20):
        BrakeSwitchOn=True
    if 0x10==(tempV&0x10):
        AccelSwitchOn=True
    if 0x08==(tempV&0x08):
        ResumeSwitchOn=True
    if 0x04==(tempV&0x04):
        CoastSwitchOn=True
    if 0x02==(tempV&0x02):
        SetSwitchOn=True
    if 0x01==(tempV&0x01):
        PTOControlSwitchOn=True
    return r, PTOModeActive,ClutchSwitchOn,BrakeSwitchOn,AccelSwitchOn,ResumeSwitchOn,CoastSwitchOn,SetSwitchOn,PTOControlSwitchOn   
def getTripDistance():
    r,t=getPhysical_float(cmd='F4',scale=0.160934)  
    return r,t
def getTotalDistance():
    r,t=getPhysical_float(cmd='F5',scale=0.160934)  
    return r,t
def getTotalEngineHours():
    r,t=getPhysical_float(cmd='F7',scale=0.05)  
    return r,t 
def getTotalEngineRevolutions():
    r,t=getPhysical_float(cmd='F9',scale=1000.0)  
    return r,t
