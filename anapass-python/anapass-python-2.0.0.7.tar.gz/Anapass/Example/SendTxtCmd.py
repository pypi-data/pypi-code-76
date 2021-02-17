

from Anapass.TModule import *
import time

###########################################################################################
#
#  T5에 연결후,  
#       Test1 :  Pattern명령 전송
#            PTRN_SET = PAINT, [Color]
#            PTRN_SET = Write, 0 
#
#       Test2 :  Read Register 명령 전송
#            RREG0=0xD6, 5
###########################################################################################

print("----------------------------------------------")
print("[anapass-python::Example] Test Send Text Command")
print("----------------------------------------------")

###########################################################################################
#
#TDevice 객체 생성, T5연결하는 Device객체이다.
#
###########################################################################################
device = TDevice(TDevice.Type.T5)


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
#       Test1 :  Pattern명령 전송
#            PTRN_SET = PAINT, 0xFF00FF
#            PTRN_SET = Write, 0 
# 
###########################################################################################

Color=(0xFF0000, 0x00FF00, 0x0000FF)
for i in range(6) :

    colIdx = i % len(Color);
    cmd = "PTRN_SET=PAINT, 0x%08X" %Color[colIdx] 
    device.SendTxtCmd(cmd) 
    print("SendTxtCmd: " + cmd)

    cmd = "PTRN_SET = Write, 0"
    device.SendTxtCmd(cmd)
    print("SendTxtCmd: " + cmd)

    time.sleep(0.5)
print()

###########################################################################################
#
#       Test2 :  Read Register 명령 전송
#            RREG0=0xD6, 5
# 
###########################################################################################

cmd = "RREG0=0xD6, 5"
maxRespBytes=1024  # 최대 1024 byte까지 받는다.
resp=device.SendTxtCmdReadResp(cmd, maxRespBytes) 
print("SendTxtCmd: " + cmd)
#if resp == TDevice.ErrorString.GetResp :
#    print("Resp Error")
#else :
print("Resp: " + resp)
print()


###########################################################################################
#
#연결을 끊는다.     
#
###########################################################################################

print("Disconnect from " + device.GetName() )
device.Disonnect()

###########################################################################################
#
# 프로그램종료
#
###########################################################################################

print("End of Exam. Bye!!")
print()



