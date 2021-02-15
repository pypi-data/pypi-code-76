import time
import DFL168A
def getVin():    
    if not DFL168A.DigitalCommand('FEEC'):
        return False, ''
    else:
        Temp=DFL168A.HandleResponse(DFL168A.ReturnStr)
        Temp=Temp.encode('utf-8') 
        Vin='' 
        for i in range(0,len(Temp),2):
            onechar=Temp[i:i+2] 
            onechar=int(onechar,16)
            Vin=Vin+chr(onechar)
    return True,Vin    
def getDTC(DTCFormat=1):
    DTC_Num=0
    SPN=[]
    FMI=[]
    CM=[]
    OC=[]
    if DTCFormat!=1 and DTCFormat!=2 and DTCFormat!=3 and DTCFormat!=4:
        return False, DTC_Num,SPN,FMI,CM,OC
    if not DFL168A.DigitalCommand('FECA'):
        return False,DTC_Num,SPN,FMI,CM,OC
    StrDTC=DFL168A.HandleResponse(DFL168A.ReturnStr)
    LEN=len(StrDTC)
    if ('0'==StrDTC[0] or '3'==StrDTC[0] or 'C'==StrDTC[0] or 'F'==StrDTC[0]) and \
       ('0'==StrDTC[1] or '3'==StrDTC[1] or 'C'==StrDTC[1] or 'F'==StrDTC[1]) and \
       ('0'==StrDTC[2] or '3'==StrDTC[2] or 'C'==StrDTC[2] or 'F'==StrDTC[2]) and \
       ('0'==StrDTC[3] or '3'==StrDTC[3] or 'C'==StrDTC[3] or 'F'==StrDTC[3]):
        return True,DTC_Num,SPN,FMI,CM,OC         #no fault
    #has fault
    if LEN<12:
        return False, DTC_Num,SPN,FMI,CM,OC
    StrDTC=StrDTC[4:]
        
    for i in range(0,LEN-11,8):
        temp=StrDTC[i:i+8]
        DTC4bytes=int(temp,16) 
        if DTC4bytes==0xFFFFFFFF:
            return True, DTC_Num,SPN,FMI,CM,OC
        OC.append(DTC4bytes & 0x7f) 
        CM.append((DTC4bytes>>7) & 0x01)
        FMI.append((DTC4bytes>>8) & 0x1F)
        if DTCFormat==1:
            SPN.append((DTC4bytes>>13) & 0x7ffff)  #19 bits's SPN
        elif DTCFormat==2:
            SPN.append(((DTC4bytes>>13)& 0x7)|((DTC4bytes>>5) & 0x07f800)|((DTC4bytes>>21) & 0x07f8) )
        else:
            SPN.append(((DTC4bytes<<3)&0X70000)|((DTC4bytes>>8)&0X0ff00)|((DTC4bytes>>24)&0X0ff))    
        DTC_Num=DTC_Num+1        
    return True,DTC_Num,SPN,FMI,CM,OC        
def clearDTC():
    if not DFL168A.DigitalCommand('FED3'):
        return False
    return True    
