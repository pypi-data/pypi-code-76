

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

eraseSectorAddr = 0x10 #  sector주소 0x10을 Erase한다 

eraseMemAddr = flash.ConvertSectorAddrToMemAddr(eraseSectorAddr)
sectorByteSize = flash.GetFlashSectorByteSize()

print("Erase SectorAddr 0x%08X" % eraseSectorAddr)
print("Erase SectorMem  0x%08X~0x%08X " % (eraseMemAddr, eraseMemAddr+sectorByteSize-1))

isOk = flash.EraseSector(eraseSectorAddr)
assert isOk 

readData=[0 for _ in range(sectorByteSize)]  #1 sector 만큼 읽는다.
isOk = flash.Read(eraseMemAddr, sectorByteSize, readData)
assert isOk 

#Sector Erase했으므로 읽은 모든 데이타가 0xFF 여야 한다.
verify=True
for data in readData :
    if data != 0xFF :
        verify=False
        break

if verify :
    print("Success : Erase Sector")
else :
    print("FAIL: Erase Sector")

#T5 Device 접속 종료
device.Disonnect()
