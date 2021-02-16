


from Anapass.TModule import *

###########################################################################################
#
#  T5에 연결후,  Power정보를 읽는다 (VBAT1, ELVSS, VDD1...)
#
###########################################################################################
print("----------------------------------------------")
print("[anapass-python::Example] Read PowerInfo")
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
# Read Power Info
# 
###########################################################################################

power = TPower()

for i in range(10) :
    isOK = device.CatchPower(power)
    if isOK == True :
        print(power.Avail)
        print(power.Voltage)
        print(power.Current)
        print(power.Range1)
        print(power.Range2)

        for p in TPower.Type :
          if power.Avail[p] == 1 :
            print(p, "V=", round(power.Voltage[p],4), "A=", round(power.Current[p],4),  "Range=", round(power.Range1[p],4), " ~ ", round(power.Range2[p],4) )
        

    else :
        print("Fail to catch PowerInfo, Retry")
    time.sleep(1)
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

