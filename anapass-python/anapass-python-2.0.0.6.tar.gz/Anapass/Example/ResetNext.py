
from Anapass.TModule import *
import time

#
#  T5에 연결후,  Reset, Next수행후 ChipID를 읽는 동작을 3번 반복 
#
print("----------------------------------------------")
print("[anapass-python::Example] ReadChipID")
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
if isConnect != True :
    print("Connect Fail")
    quit()

for loop in range(3) :

    print("----------------------------------------------")
    print("Loop :  ", loop )
    print("----------------------------------------------")

    #Reset
    print("Reset " + device.GetName())
    device.Reset()

    #1초 대기 
    print("sleep 1 second")
    time.sleep(1)

    #Next
    print("1st Next " + device.GetName())
    device.Next()

    #1초 대기 
    print("sleep 1 second")
    time.sleep(1)

    #Next
    print("2nd Next " + device.GetName())
    device.Next()

    #3초 대기 
    print("sleep 3 second")
    time.sleep(3)

    # ChipID를 읽는다.
    print("Read ChipID...")
    regAddr=0xD6 # ChipID
    byteOffset=0 # Level2Offset
    readCount=5  # 5바이트 
    regValueList=[0 for _ in range(readCount)]  #읽을 Register 값 개수만큼 리스트 할당 
    isOK = device.ReadReg(regAddr, byteOffset, readCount, regValueList)  #레지스터 Read함수 
    if isOK != True :
        print("FAIL: ReadReg,  Check the connection between TMonitor and T4/T5 Device")
        quit()
    # ChipID 읽은 결과 출력
    for regValue in regValueList :
        print(hex(regValue))
    print()


#연결을 끊는다.     
print("Disconnect from " + device.GetName())
device.Disonnect()

print("End of Exam. Bye!!")
print()



