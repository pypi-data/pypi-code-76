

from Anapass.TModule import *

#
#  T5에 연결후,  ChipID를 읽고, 화면에 출력하는 예제 
#
print("----------------------------------------------")
print("[anapass-python::Example] File Transfer")
print("----------------------------------------------")

#TDevice 객체 생성, T5연결하는 Device객체이다.
device = TDevice(TDevice.Type.T5)

#
# Python프로그램을 Device를  연결하는 코드이다.
# T4/T5 에 연결해서 사용하기 위해서는, 먼저  TEDTools의 TMonitor가 활성화되어야 한다. 
# http://aits.anapass.com:8090/display/SI/TED+Tools  에서 UserManual Chap2. 'T4/T5구동기 연결하기' 참고 
#
print("Connect To " + device.GetName() )
isConnect = device.Connect()
assert isConnect 

# FileTransfer 객체 생성
fileTransfer = TFileTransfer(TFileTransfer.Type.T5, device)
assert fileTransfer

#ret = fileTransfer.Start("d:\\work\\A2-655UV01-OTP-DEV190904-ANA6705_hthwang.TMD")
#ret = fileTransfer.Start("D:\Work\업무\AAA-업무 완성\2. Product\A2-655UV01-OTP-DEV190904-ANA6705_hthwang.TMD")
#ret = fileTransfer.Start("D:\Work\업무\AAA-업무 완성\2.Product\A2-655UV01-OTP-DEV190904-ANA6705_hthwang.TMD")
#ret = fileTransfer.Start("D:\\Work\\업무\\AAA-업무 완성\\2Product\\A2-655UV01-OTP-DEV190904-ANA6705_hthwang.TMD")
#ret = fileTransfer.Start("D:\\Work\업무\AAA-업무 완성\Product\A2-655UV01-OTP-DEV190904-ANA6705_hthwang.TMD")
#ret = fileTransfer.Start("D:\Work\업무\AAA-업무 완성\A2-655UV01-OTP-DEV190904-ANA6705_hthwang.TMD")

# hht12/hht13 은 이름만 다른 같은 파일이다.  
ret = fileTransfer.Start("\\\\nas\\13_Data\\SoC\\SoC_SI\\업무공유\\2. Product\\ANA6705(FHD+)\\3. EEPROM_TMD_VEC\\TMD\\HHT\\TMD-전송-Test\\A2-655UV01-OTP-DEV190904-ANA6705_hht12.TMD")
#ret = fileTransfer.Start("\\\\nas\\13_Data\\SoC\\SoC_SI\\업무공유\\2. Product\\ANA6705(FHD+)\\3. EEPROM_TMD_VEC\\TMD\\HHT\\TMD-전송-Test\\A2-655UV01-OTP-DEV190904-ANA6705_hht13.TMD")
#ret = fileTransfer.Start("\\\\nas\\13_Data\\SoC\\SoC_SI\\업무공유\\2. Product\\ANA6705(FHD+)\\3. EEPROM_TMD_VEC\\TMD\\HHT\\MAIN_V5_190624.dll")


#ret = fileTransfer.Start("T:\SoC\SoC_SI\업무공유\2. Product\ANA6705(FHD+)\3. EEPROM_TMD_VEC\TMD\HHT\TMD-전송-Test\A2-655UV01-OTP-DEV190904-ANA6705_hht13.TMD")
if ret != True :
    raise AssertionError(fileTransfer.LastErrorString + "  FileName: " + fileTransfer.FileName)

fileByteSize = fileTransfer.GetFileByteSize()
while True :
    transferSize = fileTransfer.GetTransferByteSize()
    if fileTransfer.IsDone() :
        print("File Transfer Success " )
        break
    elif fileTransfer.IsError() :
        print("File Transfer Error "  + fileTransfer.LastErrorString )
        break
    else :
        print("%d / %d " % (transferSize, fileByteSize) , end='\r' )


#연결을 끊는다.     
print("Disconnect from " + device.GetName() )
device.Disonnect()

print("End of Exam. Bye!!")
print()

