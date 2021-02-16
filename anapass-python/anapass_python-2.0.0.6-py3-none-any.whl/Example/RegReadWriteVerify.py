

from Anapass.TModule import *

###########################################################################################
#
#  T5에 연결후,  
#    Test1. ChipID(0xD6) 2nd Parm값을 읽고,  1 더한값을 Write/Verify 한다.
#    Test2. ChiID 3rd/4th/5th Parm값을 읽고,  1 더한값을 Write/Verify 한다. 
#
###########################################################################################
print("----------------------------------------------")
print("[anapass-python::Example] Register Read/Write/Verify")
print("----------------------------------------------")

###########################################################################################
#
#TDevice 객체 생성, T5연결하는 Device객체이다.
#
###########################################################################################
device = TDevice(TDevice.Type.T5)
#device = TDevice(TDevice.Type.TESys)

###########################################################################################
#
# Python프로그램을 Device를  연결하는 코드이다.
# T4/T5 에 연결해서 사용하기 위해서는, 먼저  TEDTools의 TMonitor가 활성화되어야 한다. 
# http://aits.anapass.com:8090/display/SI/TED+Tools  에서 UserManual Chap2. 'T4/T5구동기 연결하기' 참고 
#
###########################################################################################
print("Connect To " + device.GetName() )
isConnect = device.Connect()
if isConnect != True :
    print("Connect Fail")
    quit()

###########################################################################################
#
# Test1. ChipID(0xD6) 2nd Parm값을 읽고,  1 더한값을 Write/Verify 한다.
# 
###########################################################################################
regAddr=0xD6    # ChipID
byteOffset = 1  #2nd Parm

print("Test1. RegAddr=", hex(regAddr), " 2nd Parm R/W" )
regValue = device.ReadReg1Byte(regAddr, byteOffset)  
if regValue == -1 :
    print("FAIL: ReadReg1Byte,  Check the connection between TMonitor and T4/T5 Device")
    quit()

print("\tRead: ", hex(regValue))

regValue = (regValue+1)%0xFF
isOK=device.WriteReg1Byte(regAddr, byteOffset, regValue)
if isOK != True :
    print("FAIL: ReadReg,  Check the connection between TMonitor and T4/T5 Device")
    quit()
print("\tWrite: ", hex(regValue))

regValue = 0
regValue = device.ReadReg1Byte(regAddr, byteOffset)  
if regValue == -1 :
    print("FAIL: ReadReg1Byte,  Check the connection between TMonitor and T4/T5 Device")
    quit()
print("\tVerify: ", hex(regValue))
print()


###########################################################################################
#
# Test2. ChiID 3rd/4th/5th Parm값을 읽고,  1 더한값을 Write/Verify 한다. 
# 
###########################################################################################
print("Test1. RegAddr=", hex(regAddr), " 3rd/4th/5th Parm R/W" )
regAddr=0xD6 # ChipID
byteOffset=2 # byteOffset  3rd
readCount=3  # 읽을 개수 
regValueList=[0 for _ in range(readCount)]  #읽을 Register 값 개수만큼 리스트 할당 
isOK = device.ReadReg(regAddr, byteOffset, readCount, regValueList)  #레지스터 Read함수 
if isOK != True :
    print("FAIL: ReadReg,  Check the connection between TMonitor and T4/T5 Device")
    quit()
print("\tRead: ", str.join("", ("0x%02X " %i for i in regValueList)) )

#값을 1씩 더한다
for idx, regValue in enumerate(regValueList) :
     regValue += 1
     regValue %=256
     regValueList[idx] = regValue

isOK = device.WriteReg(regAddr, byteOffset, readCount, regValueList) 
if isOK != True :
    print("FAIL: WriteReg,  Check the connection between TMonitor and T4/T5 Device")
    quit()
print("\tWrite: ", str.join("", ("0x%02X " %i for i in regValueList)) )

regValueVerifyList=[0 for _ in range(readCount)]  #읽을 Register 값 개수만큼 리스트 할당 
isOK = device.ReadReg(regAddr, byteOffset, readCount, regValueVerifyList)  #레지스터 Read함수 
if isOK != True :
    print("FAIL: ReadReg,  Check the connection between TMonitor and T4/T5 Device")
    quit()
print("\tVerify: ", str.join("", ("0x%02X " %i for i in regValueVerifyList)) )
print()

###########################################################################################
#
#연결을 끊는다.     
#
###########################################################################################
print("Disconnect from " + device.GetName())
device.Disonnect()

###########################################################################################
#
# 프로그램종료
#
###########################################################################################
print("End of Exam. Bye!!")
print()

