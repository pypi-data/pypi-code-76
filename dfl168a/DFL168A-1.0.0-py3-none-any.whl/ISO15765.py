import time
import DFL168A
PID_13support=False
PID_1Dsupport=False
def get1byte(cmd):
    if not DFL168A.DigitalCommand(cmd):
        return False,0
    temp=DFL168A.HandleResponse(DFL168A.ReturnStr)  
    #cmd[0]='4' 
    #if temp[0:4]!=cmd:
    if temp[0]!='4' and temp[1:4]!=cmd[1:3]:
        return False,0
    Out1byte=int(temp[4:6],16)     
    return True, Out1byte
def get2byte(cmd):  
    if not DFL168A.DigitalCommand(cmd):
        return False,0
    temp=DFL168A.HandleResponse(DFL168A.ReturnStr)  
    #cmd[0]='4' 
    if temp[0]!='4' and temp[1:4]!=cmd[1:3]:
        return False,0
    Out2byte=int(temp[4:8],16)     
    return True, Out2byte   
def getPhysical2byte_float(cmd,offset,scale):  
    r,temp=get2byte(cmd)
    if not r:
        return False,0.0
    outfloat=temp*scale+offset     
    return True, outfloat    
def getPhysicalbyte_float(cmd,offset,scale):  
    r,temp=get1byte(cmd)
    if not r:
        return False,0.0
    outfloat=temp*scale+offset     
    return True, outfloat          


def getVIN():
    if not DFL168A.DigitalCommand('09 02'):
        return False,'' 
    temp=DFL168A.HandleResponse(DFL168A.ReturnStr)    
    if temp[0:4]!='4902':
        return False,''
    temp=temp[6:]   
    temp=temp.encode('utf-8') 
    Vin='' 
    for i in range(0,len(temp),2):
        onechar=temp[i:i+2] 
        onechar=int(onechar,16)
        Vin=Vin+chr(onechar)
    return True, Vin
def clearDTC():
    if False==DFL168A.SuccessCurrentProtocol:  #we don't use DigitalCommand("04") because response is "NO DATA" 
        return False

    # Catch Sleep warning, or cannel warning
    #get all receiving data for catching Sleep Warning
    if DFL168A.Ser4DFL168A.in_waiting!=0:
        temp=DFL168A.Ser4DFL168A.read(DFL168A.Ser4DFL168A.in_waiting)
        if 'S'.encode('utf-8') in temp:  # Sleep Warning
            if 'leep'.encode('utf-8') in temp:
                DFL168A.SleepWarning=True
            else:
                time.sleep(0.01)   
                if  DFL168A.Ser4DFL168A.in_waiting:
                    temp=DFL168A.Ser4DFL168A.read_all()
                    if 'leep'.encode('utf-8') in temp:
                        DFL168A.SleepWarning=True 
        elif 'C'.encode('utf-8') in temp:  # Cancel Sleep Warning 
            if 'ancel'.encode('utf-8') in temp:
                DFL168A.SleepWarning=False
            else:
                time.sleep(0.01)   
                if  DFL168A.Ser4DFL168A.in_waiting:
                    temp=DFL168A.Ser4DFL168A.read_all()
                    if 'ancel'.encode('utf-8') in temp:
                        DFL168A.SleepWarning=False  
    #Now send cmd 
    DFL168A.Ser4DFL168A.write('04\r\n'.encode('utf-8'))    
    temp=DFL168A.Ser4DFL168A.read_until('>') 
    #Jan 30 2021 add for warning and Cancel-----Begin
    if 'Sleep'.encode('utf-8') in temp:  # Sleep Warning
        DFL168A.SleepWarning=True
    elif 'Cancel'.encode('utf-8') in temp:  # Cancel Sleep Warning   
        DFL168A.SleepWarning=False
    #Jan 30 2021 add for warning and Cancel-----End

    if  'NO DATA'.encode('utf-8') in temp:  
        return True
    else:
        return False
def  getDTC():
    DTCNum=0
    DTC=[]
    def P0():
        DTC.append('P0')
        return
    def P1():
        DTC.append('P1')
        return 
    def P2():
        DTC.append('P2')
        return 
    def P3():
        DTC.append('P3')
        return     
    def C0():
        DTC.append('C0')
        return 
    def C1():
        DTC.append('C1')
        return 
    def C2():
        DTC.append('C2')
        return 
    def C3():
        DTC.append('C3')
        return                      
    def B0():
        DTC.append('B0')
        return 
    def B1():
        DTC.append('B1')
        return 
    def B2():
        DTC.append('B2')
        return
    def B3():
        DTC.append('B3')
        return              
    def U0():
        DTC.append('U0')
        return 
    def U1():
        DTC.append('U1')
        return 
    def U2():
        DTC.append('U2')
        return 
    def U3():
        DTC.append('U3')
        return             
    switcher={0:P0,1:P1,2:P2,3:P3,4:C0,5:C1,6:C2,7:C3,8:B0,9:B1,10:B2,11:B3,12:U0,13:U1,14:U2,15:U3}
    
    if not DFL168A.DigitalCommand('03'):
        return False,DTCNum,DTC
    temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
    if temp[0:2]!='43':
        return False,DTCNum,DTC
    if temp[2:4]=='00':
        return True,DTCNum,DTC
    temp=temp[4:]    
    for i in range(0,len(temp),4):
        switcher[int(temp[i],16)]()
        DTC[DTCNum]=DTC[DTCNum]+temp[i+1:i+4]
        DTCNum=DTCNum+1
    return True,DTCNum,DTC 
    
def getCoolantTemperature():
    r,t=getPhysicalbyte_float(cmd='0105',offset=-40.0,scale=1.0)
    return r,t
def getEngineSpeed():
    r,t=getPhysical2byte_float(cmd='010c',offset=0.0,scale=0.25)
    return r,t
def getVehicleSpeed():
    r,t=getPhysicalbyte_float(cmd='010d',offset=0.0,scale=1.0)
    return r,t 
def getIntakeManifoldPressure():
    r,t=getPhysicalbyte_float(cmd='010b',offset=0.0,scale=1.0)
    return r,t 
def getFuelSystemStatus():
    r,Temp=get2byte(cmd='0103')
    if 0x100==(Temp&0x100):
        A_Openloop=True
    else:
        A_Openloop=False
    if 0x200==(Temp&0x200):
        A_Closedloop=True
    else:
        A_Closedloop=False 
    if 0x400==(Temp&0x400):
        A_OpenloopByDriving_Con=True
    else:
        A_OpenloopByDriving_Con=False  
    if 0x800==(Temp&0x800):
        A_OpenloopByFault=True
    else:
        A_OpenloopByFault=False
    if 0x1000==(Temp&0x1000):
        A_ClosedloopButFault=True
    else:
        A_ClosedloopButFault=False   
    if 0x001==(Temp&0x001):
        B_Openloop=True
    else:
        B_Openloop=False
    if 0x002==(Temp&0x002):
        B_Closedloop=True
    else:
        B_Closedloop=False
    if 0x004==(Temp&0x004):
        B_OpenloopByDriving_Con=True
    else:
        B_OpenloopByDriving_Con=False 
    if 0x008==(Temp&0x008):
        B_OpenloopByFault=True
    else:
        B_OpenloopByFault=False  
    if 0x0010==(Temp&0x0010):
        B_ClosedloopButFault=True
    else:
        B_ClosedloopButFault=False 
    return r,A_Openloop,A_Closedloop,A_OpenloopByDriving_Con,A_OpenloopByFault,A_ClosedloopButFault,B_Openloop,B_Closedloop,B_OpenloopByDriving_Con,B_OpenloopByFault,B_ClosedloopButFault
def getCalculatedLoadValue():
    r,t=getPhysicalbyte_float(cmd='0104',offset=0.0,scale=0.3921568627450980392156862745098)
    return r,t 
def getShortTermFuelTrimBank13():
    r,Temp=get2byte(cmd='0106')
    Bank1=((Temp>>8)-128)*100/128.0  
    Bank3= ((Temp&0xff)-128)*100/128.0 
    return r,Bank1,Bank3
def getLongTermFuelTrimBank13():
    r,Temp=get2byte(cmd='0107')
    Bank1=((Temp>>8)-128)*100/128.0  
    Bank3= ((Temp&0xff)-128)*100/128.0 
    return r,Bank1,Bank3
def getShortTermFuelTrimBank24():
    r,Temp=get2byte(cmd='0108')
    Bank2=((Temp>>8)-128)*100/128.0  
    Bank4= ((Temp&0xff)-128)*100/128.0 
    return r,Bank2,Bank4
def getLongTermFuelTrimBank24():
    r,Temp=get2byte(cmd='0109')
    Bank2=((Temp>>8)-128)*100/128.0  
    Bank4= ((Temp&0xff)-128)*100/128.0 
    return r,Bank2,Bank4
def getIgnitionTimingAdvance():
    r,t=getPhysicalbyte_float(cmd='010E',offset=-64.0,scale=0.5)
    return r,t
def getIntakeAirTemperature():
    r,t=getPhysicalbyte_float(cmd='010F',offset=-40.0,scale=1.0)
    return r,t 
def getAirFlowRateFrmMAF():
    r,t=getPhysical2byte_float(cmd='0110',offset=0.0,scale=0.01)
    return r,t 
def getAbsThrottlePosition():
    r,t=getPhysicalbyte_float(cmd='0111',offset=0.0,scale=0.3921568627450980392156862745098)
    return r,t 
def getOxygenSensorLocation():
    global PID_13support
    global PID_1Dsupport
    Bank1_Sensor1Present=False
    Bank1_Sensor2Present=False
    Bank1_Sensor3Present=False
    Bank1_Sensor4Present=False
    Bank3_Sensor1Present=False
    Bank3_Sensor2Present=False
    Bank2_Sensor1Present=False
    Bank2_Sensor2Present=False
    Bank2_Sensor3Present=False
    Bank2_Sensor4Present=False
    Bank4_Sensor1Present=False
    Bank4_Sensor2Present=False
    r=False
    if PID_13support:
        r,Temp=get1byte(cmd='0113')
        if 0x001==(Temp&0x001) :
            Bank1_Sensor1Present=True; 
        if 0x002==(Temp&0x002):
            Bank1_Sensor2Present=True
        if 0x004==(Temp&0x004):
            Bank1_Sensor3Present=True 
        if 0x008==(Temp&0x008):
            Bank1_Sensor4Present=True

        if 0x0010==(Temp&0x0010):
            Bank2_Sensor1Present=True
        if 0x0020==(Temp&0x0020):
            Bank2_Sensor2Present=True
        if 0x0040==(Temp&0x0040):
            Bank2_Sensor3Present=True
        if 0x0080==(Temp&0x0080):
            Bank2_Sensor4Present=True 
    elif PID_1Dsupport:
        r,Temp=get1byte(cmd='011D')
        if 0x001==(Temp&0x001) :
            Bank1_Sensor1Present=True; 
        if 0x002==(Temp&0x002):
            Bank1_Sensor2Present=True
        if 0x004==(Temp&0x004):
            Bank2_Sensor1Present=True 
        if 0x008==(Temp&0x008):
            Bank2_Sensor2Present=True

        if 0x0010==(Temp&0x0010):
            Bank3_Sensor1Present=True
        if 0x0020==(Temp&0x0020):
            Bank3_Sensor2Present=True
        if 0x0040==(Temp&0x0040):
            Bank4_Sensor1Present=True
        if 0x0080==(Temp&0x0080):
            Bank4_Sensor2Present=True
    return r,Bank1_Sensor1Present,Bank1_Sensor2Present,Bank1_Sensor3Present,Bank1_Sensor4Present, \
        Bank2_Sensor1Present,Bank2_Sensor2Present,Bank2_Sensor3Present,Bank2_Sensor4Present,  \
        Bank3_Sensor1Present, Bank3_Sensor2Present,Bank4_Sensor1Present,Bank4_Sensor2Present   
def getBank1OSensor1Voltage():
    r,t=getPhysicalbyte_float(cmd='0114',offset=0.0,scale=0.005)
    return r,t
def getBank1OSensor2Voltage():
    r,t=getPhysicalbyte_float(cmd='0115',offset=0.0,scale=0.005)
    return r,t 
def getBank1OSensor3Voltage():
    r,t=getPhysicalbyte_float(cmd='0116',offset=0.0,scale=0.005)
    return r,t 
def getBank1OSensor4Voltage():
    r,t=getPhysicalbyte_float(cmd='0117',offset=0.0,scale=0.005)
    return r,t 
def getBank2OSensor1Voltage():
    global PID_13support
    if PID_13support:
        r,t=getPhysicalbyte_float(cmd='0118',offset=0.0,scale=0.005)
    else:
        r,t=getPhysicalbyte_float(cmd='0116',offset=0.0,scale=0.005)
    return r,t 
def getBank2OSensor2Voltage():
    global PID_13support
    if PID_13support:
        r,t=getPhysicalbyte_float(cmd='0119',offset=0.0,scale=0.005)
    else:
        r,t=getPhysicalbyte_float(cmd='0117',offset=0.0,scale=0.005)
    return r,t
def getBank2OSensor3Voltage():
    global PID_13support
    if PID_13support:
        r,t=getPhysicalbyte_float(cmd='011A',offset=0.0,scale=0.005)
    else:
        r=False; t=0.0
    return r,t
def getBank2OSensor4Voltage():
    global PID_13support
    if PID_13support:
        r,t=getPhysicalbyte_float(cmd='011B',offset=0.0,scale=0.005)
    else:
        r=False; t=0.0
    return r,t  
def getBank3OSensor1Voltage():
    global PID_13support
    if PID_13support:
        r,t=getPhysicalbyte_float(cmd='0118',offset=0.0,scale=0.005)
    else:
        r=False; t=0.0
    return r,t
def getBank3OSensor2Voltage():
    global PID_13support
    if PID_13support:
        r,t=getPhysicalbyte_float(cmd='0119',offset=0.0,scale=0.005)
    else:
        r=False; t=0.0
    return r,t
def getBank4OSensor1Voltage():
    global PID_13support
    if PID_13support:
        r,t=getPhysicalbyte_float(cmd='011A',offset=0.0,scale=0.005)
    else:
        r=False; t=0.0
    return r,t
def getBank4OSensor2Voltage():
    global PID_13support
    if PID_13support:
        r,t=getPhysicalbyte_float(cmd='011B',offset=0.0,scale=0.005)
    else:
        r=False; t=0.0
    return r,t    
def getOBDCertified():
    OBDType=('','OBD II','OBD','OBD and OBD II','OBD I','NO OBD','EOBD',  \
             'EOBD and OBD II','EOBD and OBD', 'EOBD, OBD and OBD II','JOBD', \
             'JOBD and OBD II','JOBD and EOBD','JOBD,EOBD,and OBD II','','','', \
             'EMD','EMD+','HD OBD-C','HD OBD','WWH OBD','','HD EOBD-I',  \
             'HD EOBD-I N','HD EOBD-II','HD EOBD-II N','','OBDBr-1','obdbr-2')
    r,t=get1byte(cmd='011C')
    if t<=29:
        OBD=OBDType[t]
    else:
        OBD=''
    return r, OBD
def getTimeSinceEngineStart():
    r,t=get2byte(cmd='011F')
    return r,t
def getDistanceTraveledMIL():
    r,t=get2byte(cmd='0121')
    return r,t
def getFuelRailPressure():
    r,t=getPhysical2byte_float(cmd='0123',offset=0.0,scale=10.0)
    return r,t 
def getFuelLevelInput():
    r,t=getPhysicalbyte_float(cmd='012F',offset=0.0,scale=0.3921568627450980392156862745098)
    return r,t 
def getDistanceTraveledSinceDTC_Clear():
    r,t=get2byte(cmd='0131')
    return r,t
def getBarometricPressure():
    r,t=get1byte(cmd='0133')
    return r,t   
def getControlModuleVoltage():
    r,t=getPhysical2byte_float(cmd='0142',offset=0.0,scale=0.001)
    return r,t  
def getRelativeThrottlePosition():
    r,t=getPhysicalbyte_float(cmd='0145',offset=0.0,scale=0.3921568627450980392156862745098)
    return r,t       
def getAmbientTemp():
    r,t=get1byte(cmd='0146')
    t=t-40
    return r,t  
def getCommandedThrottleActuatorControl():
    r,t=getPhysicalbyte_float(cmd='014C',offset=0.0,scale=0.3921568627450980392156862745098)
    return r,t          
def getEngineRunTimeMIL():
    r,t=get2byte(cmd='014D')
    return r,t    
def getEngineRunTimeSinceDTC_Clear():
    r,t=get2byte(cmd='014E')
    return r,t
def getTypeOfFuelUsedCurrently():
    OilType=('','Gasoline/petrol','Methanol','Ethanol','Diesel','Liquefied Petroleum Gas (LPG)','Compressed Natural Gas (CNG)', \
             'Propane','Battery/electric', 'Bi-fuel vehicle using gasoline','Bi-fuel vehicle using methanol', \
             'Bi-fuel vehicle using ethanol','Bi-fuel vehicle using LPG','Bi-fuel vehicle using CNG','Bi-fuel vehicle using propane','Bi-fuel vehicle using battery','Bi-fuel vehicle using battery and combustion engine', \
             'Hybrid vehicle using gasoline engine','Hybrid vehicle using gasoline engine on ethanol','Hybrid vehicle using diesel engine','Hybrid vehicle using battery','Hybrid vehicle using battery and combustion engine','Hybrid vehicle in regeneration mode')
             
    r,t=get1byte(cmd='0151')
    if t<=22:
        Oil=OBDType[t]
    else:
        Oil=''
    return r, Oil  
def getRelativeAcceleratorPedalPosition():
    r,t=getPhysicalbyte_float(cmd='015A',offset=0.0,scale=0.3921568627450980392156862745098)
    return r,t 
def getHybridBatteryPackRemainingLife():
    r,t=getPhysicalbyte_float(cmd='015B',offset=0.0,scale=0.3921568627450980392156862745098)
    return r,t   
def getEngineOilTemperature():
    r,t=get1byte(cmd='015C')
    t=t-40
    return r,t  
def getFuelRate():
    r,t=getPhysical2byte_float(cmd='015E',offset=0.0,scale=0.05)
    return r,t 
def getActualEngineTorque():
    r,t=get1byte(cmd='0162')
    t=t-125
    return r,t 
def getMILStatus():
    r,t=get1byte(cmd='0101')
    if 0x08==(t&0x08) :
        MIL_IS_ON=True
    else:
        MIL_IS_ON=False
    return r,MIL_IS_ON  
def getEngineRunTime():
    if not DFL168A.DigitalCommand('017F'):
        return False,0,0,0
    temp=DFL168A.HandleResponse(DFL168A.ReturnStr)    
    if temp[0:4]!='417F':
        return False,0,0,0
    temp=temp[4:]
    Judge=int(temp[0:2],16)
    if 0x1==(Judge&0x01):
        #Supported TotalEngineRunTime
        TotalEngineRunTime=int(temp[2:10],16)
    else:
        TotalEngineRunTime=0
    if 0x2==(Judge&0x2)  :
        #Supported TotalIdleRunTime      
        TotalIdleRunTime=int(temp[10:18],16)
    else:
        TotalIdleRunTime=0
    if 0x4==(Judge&0x4):
        #Supported TotalRunTimeWithPTOActive          
        TotalRunTimeWithPTOActive=int(temp[18:26],16)
    else:
        TotalRunTimeWithPTOActive=0
    return True, TotalEngineRunTime,TotalIdleRunTime,TotalRunTimeWithPTOActive
    