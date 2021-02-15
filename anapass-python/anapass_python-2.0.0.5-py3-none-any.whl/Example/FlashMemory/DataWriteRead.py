


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


writeMemAddr = 0x1000
writeByteSize = 512 
writeData=[x&0xFF for x in range(writeByteSize)]  #1 sector 만큼 읽는다.

print("DataWrite.... ", end= ' ')
isOk = flash.Write(writeMemAddr, writeByteSize, writeData )
assert isOk
print("OK")
Util.Print.ListHex(writeMemAddr, writeData)
print()

print("DataRead.... ", end= ' ')
readData=[0 for _ in range(writeByteSize)]  
isOk = flash.Read(writeMemAddr, writeByteSize, readData )
assert isOk
print("OK")
Util.Print.ListHex(writeMemAddr, readData)
print()

print("Data Verify ... ", end= ' ')
isVerify=True
for idx in range(writeByteSize) :
    if writeData[idx] != readData[idx] :
        isVerify = False
        break

if isVerify : 
    print("Success")
else :
    print("Fail")
    print("Fail")

#T5 Device 접속 종료
device.Disonnect()



