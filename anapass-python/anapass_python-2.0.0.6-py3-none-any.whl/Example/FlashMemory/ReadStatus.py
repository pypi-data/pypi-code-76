
from Anapass.TModule import *
from Anapass import FlashMemory


#T5 Device에 연결한다. 
device = TDevice(TDevice.Type.T5)
isOk = device.Connect()
if isOk != True :
    raise ConnectionRefusedError("Fail to connect to TDevice(%s)"%device.GetName())

#Flash Memory Instacne 생성
#  TChip.Type.ANA6705 :  Anapass/ANA6705/ANA6705_FlashMipiToSp.py 에  코드 구현됨 
#  TChip.Type.ANA6706 :  Anapass/ANA6706/ANA6706_FlashMipiToSp.py 에  코드 구현됨 
chipType = TChip.Type.ANA6705
#chipType = TChip.Type.ANA6706
flash = FlashMemory.CreateInstance(device, chipType, FlashMemory.Type.MipiToSpi)

status1 =  flash.ReadStatus1()
status2  = flash.ReadStatus2()
if status2&0x02 : 
    isLock = False
else :
    isLock = True

print("status1 =  0x%02X" % status1)
print("status2 =  0x%02X" % status2)
print("isLock =  " , isLock)

#T5 Device 접속 종료
device.Disonnect()
