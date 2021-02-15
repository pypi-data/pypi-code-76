import time
import DFL168A
def getGPSinfo():
    Latitude=0.0
    Longitude=0.0
    Speed=0.0
    Time='' #format:hh:mm::ss
    Date='' #format:dd/mm/yyyy
    DFL168A.Ser4DFL168A.timeout=DFL168A.GPSTimeOut+0.05
    if not DFL168A.ATCommand('ATDEV1SIGBSOF1'):
        DFL168A.Ser4DFL168A.timeout=DFL168A.TimeOut+2.0
        return False,Latitude,Longitude,Speed, Time,Date
    DFL168A.Ser4DFL168A.timeout=DFL168A.TimeOut+2.0

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
    DFL168A.Ser4DFL168A.write('AT DEV1 LAT\r\n'.encode('utf-8'))    
    temp=DFL168A.Ser4DFL168A.read_until('>') 
    #Jan 30 2021 add for warning and Cancel-----Begin
    if 'Sleep'.encode('utf-8') in temp:  # Sleep Warning
        DFL168A.SleepWarning=True
        return False,Latitude,Longitude,Speed, Time,Date
    elif 'Cancel'.encode('utf-8') in temp:  # Cancel Sleep Warning   
        DFL168A.SleepWarning=False
        return False,Latitude,Longitude,Speed, Time,Date
    #Jan 30 2021 add for warning and Cancel-----End    

    if temp[-1:]!='>'.encode('utf-8'):
        return False,Latitude,Longitude,Speed, Time,Date
    temp=temp[:-1]  #remove '>'
    temp=temp.decode('utf-8')
    temp=temp.strip()
    temp=temp.upper()  #in case lowercase
    if temp=='':
        return False,Latitude,Longitude,Speed, Time,Date
    if temp[0]=='?':
        return False,Latitude,Longitude,Speed, Time,Date 
    if temp[0]=='N':
        return False,Latitude,Longitude,Speed, Time,Date 
    if '-'==temp[0]:
        Minus_Result=True
    else:
        Minus_Result=False
    Space_Index=temp.find(' ')
    if Space_Index!=-1:
        Latitude=float(temp[0:Space_Index])
        temp=temp[Space_Index+1:]
    else:
        Latitude=0.0        
    Space_Index=temp.find('\'')
    tempF=float(temp[0:Space_Index])
    tempF=tempF/60.0
    if Minus_Result: 
        Latitude=Latitude-tempF
    else: 
        Latitude=Latitude+tempF

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
    DFL168A.Ser4DFL168A.write('AT DEV1 LONG\r\n'.encode('utf-8'))    
    temp=DFL168A.Ser4DFL168A.read_until('>') 
    #Jan 30 2021 add for warning and Cancel-----Begin
    if 'Sleep'.encode('utf-8') in temp:  # Sleep Warning
        DFL168A.SleepWarning=True
        return False,Latitude,Longitude,Speed, Time,Date
    elif 'Cancel'.encode('utf-8') in temp:  # Cancel Sleep Warning   
        DFL168A.SleepWarning=False
        return False,Latitude,Longitude,Speed, Time,Date
    #Jan 30 2021 add for warning and Cancel-----End    

    if temp[-1:]!='>'.encode('utf-8'):
        return False,Latitude,Longitude,Speed, Time,Date
    temp=temp[:-1]  #remove '>'
    temp=temp.decode('utf-8')
    temp=temp.strip()
    temp=temp.upper()  #in case lowercase
    if temp=='':
        return False,Latitude,Longitude,Speed, Time,Date
    if temp[0]=='?':
        return False,Latitude,Longitude,Speed, Time,Date 
    if temp[0]=='N':
        return False,Latitude,Longitude,Speed, Time,Date 
    if '-'==temp[0]:
        Minus_Result=True
    else:
        Minus_Result=False
    Space_Index=temp.find(' ')
    if Space_Index!=-1:
        Longitude=float(temp[0:Space_Index])
        temp=temp[Space_Index+1:]
    else:
        Longitude=0.0        
    Space_Index=temp.find('\'')
    tempF=float(temp[0:Space_Index])
    tempF=tempF/60.0
    if Minus_Result: 
        Longitude=Longitude-tempF 
    else: 
        Longitude=Longitude+tempF

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
    DFL168A.Ser4DFL168A.write('AT DEV1 SPEED\r\n'.encode('utf-8'))    
    temp=DFL168A.Ser4DFL168A.read_until('>') 
    #Jan 30 2021 add for warning and Cancel-----Begin
    if 'Sleep'.encode('utf-8') in temp:  # Sleep Warning
        DFL168A.SleepWarning=True
        return False,Latitude,Longitude,Speed, Time,Date
    elif 'Cancel'.encode('utf-8') in temp:  # Cancel Sleep Warning   
        DFL168A.SleepWarning=False
        return False,Latitude,Longitude,Speed, Time,Date
    #Jan 30 2021 add for warning and Cancel-----End    

    if temp[-1:]!='>'.encode('utf-8'):
        return False,Latitude,Longitude,Speed, Time,Date
    temp=temp[:-1]  #remove '>'
    temp=temp.decode('utf-8')
    temp=temp.strip()
    temp=temp.upper()  #in case lowercase
    if temp=='':
        return False,Latitude,Longitude,Speed, Time,Date
    if temp[0]=='?':
        return False,Latitude,Longitude,Speed, Time,Date 
    if temp[0]=='N':
        return False,Latitude,Longitude,Speed, Time,Date 
    Speed=float(temp) 
    Speed=Speed*1.852

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
    DFL168A.Ser4DFL168A.write('AT DEV1 TIME\r\n'.encode('utf-8'))    
    temp=DFL168A.Ser4DFL168A.read_until('>') 
    #Jan 30 2021 add for warning and Cancel-----Begin
    if 'Sleep'.encode('utf-8') in temp:  # Sleep Warning
        DFL168A.SleepWarning=True
        return False,Latitude,Longitude,Speed, Time,Date
    elif 'Cancel'.encode('utf-8') in temp:  # Cancel Sleep Warning   
        DFL168A.SleepWarning=False
        return False,Latitude,Longitude,Speed, Time,Date
    #Jan 30 2021 add for warning and Cancel-----End    

    if temp[-1:]!='>'.encode('utf-8'):
        return False,Latitude,Longitude,Speed, Time,Date
    temp=temp[:-1]  #remove '>'
    temp=temp.decode('utf-8')
    temp=temp.strip()
    temp=temp.upper()  #in case lowercase
    if temp=='':
        return False,Latitude,Longitude,Speed, Time,Date
    if temp[0]=='?':
        return False,Latitude,Longitude,Speed, Time,Date 
    if temp[0]=='N':
        return False,Latitude,Longitude,Speed, Time,Date 
    Time=temp  

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
    DFL168A.Ser4DFL168A.write('AT DEV1 DATE\r\n'.encode('utf-8'))    
    temp=DFL168A.Ser4DFL168A.read_until('>') 
    #Jan 30 2021 add for warning and Cancel-----Begin
    if 'Sleep'.encode('utf-8') in temp:  # Sleep Warning
        DFL168A.SleepWarning=True
        return False,Latitude,Longitude,Speed, Time,Date
    elif 'Cancel'.encode('utf-8') in temp:  # Cancel Sleep Warning   
        DFL168A.SleepWarning=False
        return False,Latitude,Longitude,Speed, Time,Date
    #Jan 30 2021 add for warning and Cancel-----End    

    if temp[-1:]!='>'.encode('utf-8'):
        return False,Latitude,Longitude,Speed, Time,Date
    temp=temp[:-1]  #remove '>'
    temp=temp.decode('utf-8')
    temp=temp.strip()
    temp=temp.upper()  #in case lowercase
    if temp=='':
        return False,Latitude,Longitude,Speed, Time,Date
    if temp[0]=='?':
        return False,Latitude,Longitude,Speed, Time,Date 
    if temp[0]=='N':
        return False,Latitude,Longitude,Speed, Time,Date 
    Date=temp
    return True, Latitude,Longitude,Speed, Time,Date

def getAltitude():
    Altitude=0
    DFL168A.Ser4DFL168A.timeout=DFL168A.GPSTimeOut+0.05
    if not DFL168A.ATCommand('ATDEV1SIGBSOF2'):
        DFL168A.Ser4DFL168A.timeout=DFL168A.TimeOut+2.0
        return False,Altitude
    DFL168A.Ser4DFL168A.timeout=DFL168A.TimeOut+2.0

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
    DFL168A.Ser4DFL168A.write('AT DEV1 ALT\r\n'.encode('utf-8'))    
    temp=DFL168A.Ser4DFL168A.read_until('>') 
    #Jan 30 2021 add for warning and Cancel-----Begin
    if 'Sleep'.encode('utf-8') in temp:  # Sleep Warning
        DFL168A.SleepWarning=True
        return False,Altitude
    elif 'Cancel'.encode('utf-8') in temp:  # Cancel Sleep Warning   
        DFL168A.SleepWarning=False
        return False,Altitude
    #Jan 30 2021 add for warning and Cancel-----End    

    if temp[-1:]!='>'.encode('utf-8'):
        return False,Altitude
    temp=temp[:-1]  #remove '>'
    temp=temp.decode('utf-8')
    temp=temp.strip()
    temp=temp.upper()  #in case lowercase
    if temp=='':
        return False,Altitude
    if temp[0]=='?':
        return False,Altitude 
    if temp[0]=='N':
        return False,Altitude 
    Altitude=float(temp)
    return True,Altitude