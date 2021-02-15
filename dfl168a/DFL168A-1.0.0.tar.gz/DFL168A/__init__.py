import serial
import time
from enum import Enum,unique,auto
import string
from DFL168A import ISO15765
@unique
class REASON(Enum):
    NORMAL=auto()
    FAIL_IN_OPEN_SERIAL=auto()
    FAIL_IN_AT_CMD=auto()
    FAIL_IN_WRONG_IC=auto()
    SLEEP_WARN=auto()




class PROTOCOL(Enum):
    AUTO=0
    ISO15765_11_500=6
    ISO15765_29_500=7
    ISO15765_11_250=8
    ISO15765_29_250=9
    J1939=10
    USER1=11
    USER2=12
    J1708=13
Ser4DFL168A=None   #Serial port object for DFL168A
currentProtocol=PROTOCOL.AUTO
TransparentSerialAvailable=False
EndTransparentChar=b'\x1b'
TimeOut=0.5   #500ms
SuccessCurrentProtocol=False
ReturnStr=None
SleepWarning=False
GPSTimeOut=0.5

def ATCommand(cmd):
    '''
    cmd is tring without cr lf
    '''
    global Ser4DFL168A  #must have it
    global SleepWarning
    global ReturnStr
    if Ser4DFL168A.is_open==False:
        return False  
    #Feb 03 2021 Add for catch warning and cancel-----Begin
    #Ser4DFL168A.reset_input_buffer()
    temp=Ser4DFL168A.read(Ser4DFL168A.in_waiting)
    if 'S'.encode('utf-8') in temp:  # Sleep Warning
        if 'leep'.encode('utf-8') in temp:
            SleepWarning=True
        else:
            time.sleep(0.01)   
            if  Ser4DFL168A.in_waiting:
                temp=Ser4DFL168A.read_all()
                if 'leep'.encode('utf-8') in temp:
                    SleepWarning=True 
    elif 'C'.encode('utf-8') in temp:  # Cancel Sleep Warning 
        if 'ancel'.encode('utf-8') in temp:
            SleepWarning=False
        else:
            time.sleep(0.01)   
            if  Ser4DFL168A.in_waiting:
                temp=Ser4DFL168A.read_all()
                if 'ancel'.encode('utf-8') in temp:
                    SleepWarning=False                  
    #Feb 03 2021 Add for catch warning and cancel-----End
    cmd=cmd+'\r\n'
    Ser4DFL168A.write(cmd.encode('utf-8'))
    TimeCount=0
    while Ser4DFL168A.in_waiting<6:        
        TimeCount=TimeCount+1
        if TimeCount>10:    #10 not work
            Ser4DFL168A.reset_input_buffer()
            return False
        #time.sleep(0.05)  #50ms
        time.sleep(0.01)  #10ms
    time.sleep(0.05)  # wait 50ms more
    
    ReturnStr=Ser4DFL168A.read(Ser4DFL168A.in_waiting)
    Ser4DFL168A.reset_input_buffer()
    if ReturnStr[-7:-5]=="OK".encode('utf-8'): 
        #Jan 30 2021 add for warning and Cancel-----Begin
        if 'Sleep'.encode('utf-8') in ReturnStr:  # Sleep Warning
            SleepWarning=True
        elif 'Cancel'.encode('utf-8') in ReturnStr:  # Cancel Sleep Warning   
            SleepWarning=False
        #Jan 30 2021 add for warning and Cancel-----End       
        return True
    #Jan 30 2021 add for warning and Cancel-----Begin
    if 'Sleep'.encode('utf-8') in ReturnStr:  # Sleep Warning
        SleepWarning=True
    elif 'Cancel'.encode('utf-8') in ReturnStr:  # Cancel Sleep Warning   
        SleepWarning=False
    #Jan 30 2021 add for warning and Cancel-----End
    return False    



def begin(SerialName,BaudRate=57600,Protocol=PROTOCOL.AUTO,BaudRate4Protocol=250000,Timeout=0.5,BaudRate4GPS=9600,TimeOut4GPS=0.5,Intrude=True,Fast=False):
    global Ser4DFL168A
    global currentProtocol
    global TransparentSerialAvailable
    global EndTransparentChar
    global TimeOut
    global SuccessCurrentProtocol
    global ReturnStr
    global SleepWarning
    global GPSTimeOut
    currentProtocol=Protocol
    TimeOut=Timeout
    GPSTimeOut=TimeOut4GPS
    try:
        Ser4DFL168A=serial.Serial(SerialName,BaudRate,timeout=Timeout+2.0)  #due to DFL168A time out must < UART Timeout, otherwise, you cannot get 'No Data' ,+2.0:ok, +1.9 fail        
    except Exception as e:
        print(e)
        return False,REASON.FAIL_IN_OPEN_SERIAL
    else:
        ATCommand("AT Z")  #repower for Sync
        time.sleep(0.075)  #wait for "Searching and version " pass
        Ser4DFL168A.reset_input_buffer()
        ATCommand("ATi")
        if ReturnStr==None:
            SuccessCurrentProtocol=False
            return False,REASON.FAIL_IN_AT_CMD        
        if len(ReturnStr)<17 or ReturnStr[5:12]!='DFL168A'.encode('utf-8'):
            SuccessCurrentProtocol=False
            return False, REASON.FAIL_IN_WRONG_IC
        if Fast:
            SuccessCurrentProtocol=True
            time.sleep(4.8)  #4.6 cannot catch warning, 4.7 can catch
            temp=Ser4DFL168A.read(Ser4DFL168A.in_waiting) 
            if 'Warning'.encode('utf-8') in temp:
                SleepWarning=True
                SuccessCurrentProtocol=False
            if Intrude==False:
                while False==ATCommand('AT INTRUDE 0'):
                    pass
            if PROTOCOL.AUTO==currentProtocol or \
            PROTOCOL.ISO15765_11_250==currentProtocol or \
            PROTOCOL.ISO15765_11_500==currentProtocol or \
            PROTOCOL.ISO15765_29_250==currentProtocol or \
            PROTOCOL.ISO15765_29_500==currentProtocol :
                r,temp=ISO15765.get2byte('0100')                         
                if r:
                    if temp & 0x00002000:
                        ISO15765.PID_13support=True
                    else:
                        ISO15765.PID_13support=False
                    if temp & 0x00000008:
                        ISO15765.PID_1Dsupport=True
                    else:
                        ISO15765.PID_1Dsupport=False   
            if SleepWarning:
                return True,REASON.SLEEP_WARN                         
            return True,REASON.NORMAL  
        if (currentProtocol!=PROTOCOL.J1939) or (currentProtocol==PROTOCOL.J1939 and BaudRate4Protocol==250000):
            if False==ATCommand('AT SP'+'{:x}'.format(currentProtocol.value)):
                SuccessCurrentProtocol=False
                return False,REASON.FAIL_IN_AT_CMD
        else:
            #j1939, but baud rate is not 250000
            if False==ATCommand('AT SPB'):
                SuccessCurrentProtocol=False
                return False,REASON.FAIL_IN_AT_CMD
            #set baud rate
            #Baud rate=500k/setting value, so setting value=500000/baud rate
            temp=int(500000/BaudRate4Protocol+0.5)
            if False==ATCommand('AT PP 34 SV'+'{:02x}'.format(temp)):
                SuccessCurrentProtocol=False
                return False,REASON.FAIL_IN_AT_CMD
            if False==ATCommand('AT PP 34 ON'):
                SuccessCurrentProtocol=False
                return False,REASON.FAIL_IN_AT_CMD
            if False==ATCommand('AT PP 33 SV 02'):    #J1939 Format
                SuccessCurrentProtocol=False
                return False,REASON.FAIL_IN_AT_CMD 
            if False==ATCommand('AT PP 33 ON'):
                SuccessCurrentProtocol=False
                return False,REASON.FAIL_IN_AT_CMD 
            if False==ATCommand('AT PPP'):
                SuccessCurrentProtocol=False
                return False,REASON.FAIL_IN_AT_CMD 
        #Re-power on
        ATCommand('AT Z')  
        while Ser4DFL168A.out_waiting!=0:
            pass
        if False==ATCommand('AT E 0'):
            SuccessCurrentProtocol=False
            return False ,REASON.FAIL_IN_AT_CMD
        time.sleep(0.07) 
        #Ser4DFL168A.reset_input_buffer() #clear " Search... cannot connect " 
        time.sleep(4.8)  #4.6 cannot catch warning, 4.7 can catch
        temp=Ser4DFL168A.read(Ser4DFL168A.in_waiting) 
        if 'Warning'.encode('utf-8') in temp:
            SleepWarning=True
            SuccessCurrentProtocol=False
        else:
            SuccessCurrentProtocol=True    
        if TimeOut<=1:
            temp='AT ST '+'{:02x}'.format(int(TimeOut*1000/4+0.5)) 
        elif TimeOut<=2:
            temp='AT ST FB'
        elif TimeOut<=4:
            temp='AT ST FC'
        elif TimeOut<=6:
            temp='AT ST FD' 
        elif TimeOut<=8:
            temp='AT ST FE'
        else:
            temp='AT ST FF' 
        if False==ATCommand(temp):
            SuccessCurrentProtocol=False
            return False ,REASON.FAIL_IN_AT_CMD 
        #AT S 0
        while False==ATCommand('AT S 0'):
            pass
        #at dev1 tp 6  : GPS
        while False==ATCommand('AT DEV1 TP 6'):
            pass
        #AT DEV1 PC
        if False==ATCommand('AT DEV1 PC'):
            SuccessCurrentProtocol=False
            return False,REASON.FAIL_IN_AT_CMD  
        #Change DEV1 baud rate:  DEV1 BRD  hh
        if BaudRate4GPS==4800:
            temp='AT DEV1 BRD 01' 
        elif BaudRate4GPS==2400:
            temp='AT DEV1 BRD 02'    
        elif BaudRate4GPS==9600:
            temp='AT DEV1 BRD 00' 
        else:
            temp='AT DEV1 BRD '+'{:02x}'.format(int(5000000/BaudRate4GPS+0.5))
        while False==ATCommand(temp):
            pass  
        #Time out= 500ms for gps
        if TimeOut4GPS==0.5:
            temp='AT DEV1 ST 00'    
        elif TimeOut4GPS<=1:
            temp='AT DEV1 ST'+'{:02x}'.format(int(TimeOut4GPS*1000/4+0.5))       
        elif TimeOut4GPS<=2:
            temp='AT DEV1 ST FB'  
        elif TimeOut4GPS<=4:
            temp='AT DEV1 ST FC'
        elif TimeOut4GPS<=6:
            temp='AT DEV1 ST FD'
        elif TimeOut4GPS<=8:
            temp='AT DEV1 ST FE'
        else:
            temp='AT DEV1 ST FF'  
        while False==ATCommand(temp):
            pass 
        #at DEV1 TPT 0: Disable exit transparant by timeout 
        while False==ATCommand('AT DEV1 TPT 0'):
            pass
        #at dev1 tp 6  : GPS
        while False==ATCommand('AT DEV1 TP 6'):
            pass  
        if Intrude==False:
            while False==ATCommand('AT INTRUDE 0'):
                pass
        #SuccessCurrentProtocol=True
        if PROTOCOL.AUTO==currentProtocol or \
        PROTOCOL.ISO15765_11_250==currentProtocol or \
        PROTOCOL.ISO15765_11_500==currentProtocol or \
        PROTOCOL.ISO15765_29_250==currentProtocol or \
        PROTOCOL.ISO15765_29_500==currentProtocol : 
            r,temp=ISO15765.get2byte('0100')           
            if r:
                if temp & 0x00002000:
                    ISO15765.PID_13support=True
                else:
                    ISO15765.PID_13support=False
                if temp & 0x00000008:
                    ISO15765.PID_1Dsupport=True
                else:
                    ISO15765.PID_1Dsupport=False        
        time.sleep(0.01)  
        #clear all data received
        Ser4DFL168A.reset_input_buffer()
        if  SleepWarning:
            return True,REASON.SLEEP_WARN         
        return True,REASON.NORMAL
def DigitalCommand(Cmd):
    '''
        Arguments input Cmd------Digital command string without tail '\r\n'
        Result is in global ReturnStr (without '\r\n' head)
        success: return true
    '''
    global SuccessCurrentProtocol
    global ReturnStr
    global Ser4DFL168A
    global SleepWarning
    if False==SuccessCurrentProtocol:
        ReturnStr=""
        return False
    '''    
    #remove space
    #temp=filter(lambda c:c!=' ',Cmd)
    temp=(c for c in Cmd if c!=' ') 
    cmd=''.join(temp)        
    temp=all(c in string.hexdigits for c in cmd)
    if not temp :
        ReturnStr=""
        return False        
    cmd=cmd+'\r\n' 
    '''
    cmd=Cmd+'\r\n'
    #Ser4DFL168A.reset_input_buffer() #clear old receiving data ----must : in case old digital cmd has "No data"   
    #get all receiving data for catching Sleep Warning
    if Ser4DFL168A.in_waiting!=0:
        temp=Ser4DFL168A.read(Ser4DFL168A.in_waiting)
        if 'S'.encode('utf-8') in temp:  # Sleep Warning
            if 'leep'.encode('utf-8') in temp:
                SleepWarning=True
            else:
                time.sleep(0.01)   
                if  Ser4DFL168A.in_waiting:
                    temp=Ser4DFL168A.read_all()
                    if 'leep'.encode('utf-8') in temp:
                        SleepWarning=True 
        elif 'C'.encode('utf-8') in temp:  # Cancel Sleep Warning 
            if 'ancel'.encode('utf-8') in temp:
                SleepWarning=False
            else:
                time.sleep(0.01)   
                if  Ser4DFL168A.in_waiting:
                    temp=Ser4DFL168A.read_all()
                    if 'ancel'.encode('utf-8') in temp:
                        SleepWarning=False 
    #Feb 02 /2021 Add because stuck if we send digital command more than 2 times when protocol off-----Begin                    
    #if currentProtocol==PROTOCOL.J1708:  #Only J1708 have chance to send more than 2 times digital command
    if SleepWarning:
        #we don't send digital command
        ReturnStr=""
        return False
    #Feb 02 /2021 Add because stuck if we send digital command more than 2 times when protocol off-----End

    Ser4DFL168A.write(cmd.encode('utf-8'))    
    
    #temp=Ser4DFL168A.read_until('>')    too slow
    global TimeOut
    tC=0
    MyC=TimeOut*100  #10 ms counter
    MyC=MyC+10  #extra 100ms
    while Ser4DFL168A.in_waiting<6:        
        tC=tC+1
        if tC>MyC:    #10 not work
            break        
        time.sleep(0.01)  #10ms
    time.sleep(0.05)  # wait 50ms more
    temp=Ser4DFL168A.read(Ser4DFL168A.in_waiting)
    if 'Sleep'.encode('utf-8') in temp:  # Sleep Warning
        SleepWarning=True
    elif 'Cancel'.encode('utf-8') in temp:  # Cancel Sleep Warning   
        SleepWarning=False

    if temp[-1:]!='>'.encode('utf-8'):
        ReturnStr=""
        
        #Feb 02 /2021 Add because stuck if we send digital command more than 2 times when protocol off
        if currentProtocol==PROTOCOL.J1708:  #Only J1708 have chance to send more than 2 times digital command
            #send 'CTRL+C'
            if temp=='\r\n'.encode('utf-8'):
                Ser4DFL168A.write(0x03)
                while Ser4DFL168A.out_waiting!=0:
                    pass
            Ser4DFL168A.reset_input_buffer()   # cannot have warning because warning causes stuck when 2 times digital cmd
            
        return False
    temp=temp[:-1]  #remove '>'
    #remove first '\r\n'
    temp=temp[2:]
    try:        
        temp=temp.decode('utf-8')
    except Exception as e:
        print(e)
        ReturnStr=""
        return False
    else:       
        ReturnStr=temp
        c=any(c not in string.hexdigits for c in temp if c!=':' and c!=' ' and c!='\r' and c!='\n' ) 
        if c:
            ReturnStr=""
            return False
        if  ReturnStr=='':
            return False   
        return True
def HandleResponse(Resp):
    '''
       It will process Digital command response
       Arguments:
       Input: Resp is response String, no CR LF for begining, but it has CR LF at end
       Return:  String, It will be pure resonse String no matter long frame or short frame,
                    And it won't contains any CR LF
                    Author: Jack Xia, Dafulai Electronics Inc, Jan 29 2021
    '''  
    
    LongFrame=':' in Resp
    if not LongFrame:
        # short frame handle
        '''
        temp=(c for c in Resp if c!='\r' and c!='\n' and c!=' ') 
        Resp=''.join(temp) 
        '''
        Resp=Resp.strip()
        return  Resp
    else:
        #long frame handle
        DataLen=Resp[:3]
        DataLen=int(DataLen,16)
        temp_Resp=Resp
        Resp=''
        pos=temp_Resp.find(':')        
        while pos!=-1:
            temp_Resp=temp_Resp[pos+1:]
            pos=temp_Resp.find(':')
            if pos!=-1:
                temp=temp_Resp[:pos-3]
                if temp.find('\r')>0:
                    temp=temp[:temp.find('\r')]
                Resp=Resp+temp
            else:
                Resp=Resp+temp_Resp
                break
        '''    
        temp=(c for c in Resp if c!=' ')   #remove space
        Resp=''.join(temp) 
        '''  
        Resp=Resp.strip()
        Resp=Resp[:2*DataLen]  
        return  Resp  
    return   
def getOnewireID():
    '''
         read one wire Button ID
       return bool:success/fail and 7 bytes ID to list
    '''
    global ReturnStr
    ID=[]
    ATCommand('AT OW RD')
    time.sleep(0.002)
    ReturnStr=ReturnStr[0:-1]  #remove '>'
    ReturnStr=ReturnStr.strip()

    if ReturnStr!='No Device Connected'.encode('utf-8'):
        for i in range(0,14,2):
            if ReturnStr[i:i+2].decode('utf-8') not in string.hexdigits: 
                return False, ID
            temp=int(ReturnStr[i:i+2],16)
            ID.append(temp)
        return True,ID
    else:
        return False,ID
def getDIN(PortNo):
    '''
       Input : Digital port number
       Return: bool:success/fail and Digital Value: True/False . True is Logic High, False is Logic Low
    '''
    global ReturnStr
    cmd='AT RD' + '{:x}'.format(PortNo)
    ATCommand(cmd)
    ReturnStr=ReturnStr[0:-1]   #remove '>'
    ReturnStr=ReturnStr.strip()
    if ReturnStr=="1".encode('utf-8'):
        return True,True
    if ReturnStr=="0".encode('utf-8'):
        return True, False
    return False, False
def setDOUT(portNo, Value):
    '''
       Input : Digital port number, and value: True: High, False: Low
       Return: bool:success/fail
    '''
    cmd='AT WD' + '{:x}'.format(portNo)
    if Value: 
        cmd=cmd+'1'
    else:
        cmd=cmd+'0'
    if ATCommand(cmd):
        return True
    else:
        return False
def getAnalog():
    '''
       return bool:success/fail  and analog input value
    '''
    global ReturnStr
    ATCommand('AT RV')
    ReturnStr=ReturnStr[0:-1]  #remove '>'
    ReturnStr=ReturnStr.strip()
    ReturnStr=ReturnStr[0:-1]    #remove 'V'
    try:
      r=float(ReturnStr)
      return True, r
    except:
      return False,0
def setExitTransparentKey(charactor):
    """Set exit transparant charactor, must call after begin()

    Args:
        charactor (byte): This is one byte for exit charactor ascii code
    return:
         True: Success, False: Fail    
    """
    global EndTransparentChar
    cmd="ATDEV1EXITT"
    cmd=cmd+'{:02x}'.format(charactor)+'\r\n'
    if ATCommand(cmd):
        EndTransparentChar=charactor
        return True
    else:
        return False

def beginTransparentSerial():
    """
    Serila Port access DEV1 transparently
    """
    global TransparentSerialAvailable
    global Ser4DFL168A
    Ser4DFL168A.write('ATDEV1TRANSP\r\n'.encode("utf-8"))
    TransparentSerialAvailable=True
def endTransparentSerial():
    '''
       End Transparant mode       
    '''
    global TransparentSerialAvailable
    global Ser4DFL168A
    global EndTransparentChar
    if TransparentSerialAvailable:
        Ser4DFL168A.write(EndTransparentChar)        
        temp=Ser4DFL168A.read_until('>'.encode('utf-8'))
        if '>'.encode('utf-8') in temp:
            TransparentSerialAvailable=False
            
def setSleepDelay(sleepDelay_seconds):
    '''
    Set sleep delay seconds count if no any Vehicle bus activity
        Args:
        sleepDelay_seconds (integer) : Seconds for delay 
        Maximum sleepDelay_seconds=65535 seconds=18.2 hours
        return: True--Success,  False -- Fail
    '''
    if sleepDelay_seconds>0xffff:
        return False
    cmd='AT Sleep '+'{:04x}'.format(sleepDelay_seconds)
    if ATCommand(cmd):
        return True
    return False

def End():
    global Ser4DFL168A
    if Ser4DFL168A!=None:
        if Ser4DFL168A.is_open:
            Ser4DFL168A.close
        
