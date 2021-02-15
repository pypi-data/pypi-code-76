
#
# Ana6705/FlashMipiToSpi
#
from Anapass import Register
import time

ModuleName="Anapass.ANA6705.FlashMipiToSpi"
FlashCapacity = 0x1000000   # 16MByte
FlashSectorMaxCount = FlashCapacity >> 12
CtrlRegCount = 5 
FlashReadChunkByteSize = 128
FlashWriteChunkByteSize = 128
FlashSectorByteSize = 4096

#Spi Command 
COMMAND_READ = 0
COMMAND_ERASE = 1
COMMAND_SECTOR_ERASE = 2
COMMAND_WRITE = 3
COMMAND_READ_STATUS1 = 4
COMMAND_READ_STATUS2 = 5
COMMAND_WRITE_STATUS1 = 6
COMMAND_WRITE_STATUS2 = 7

def ConvertSectorAddrToMemAddr(sectorAddr) :
    return (sectorAddr << 12) & 0x00FFF000;

def ConvertMemAddrToSectorAddr(memAddr) :
    return (memAddr >> 12)

def MakeCmdValue(command, op_start) :
    c = ((command<<1) & 0x0E) | (op_start&0x1)
    return c

def WaitDone(device, spiCmd) :
    sleepMSec = 0.03; #30ms
    expectedResponse = spiCmd & 0xFE
    byteOffset=4
    bRet = False
    while 1 :
        c = device.ReadReg1Byte(Register.ANA6705.SPICTL, byteOffset)
        if c == -1 :
            raise AssertionError(ModuleName+ "." + "WaitDone")
        elif (c & 0x01) == 0 :
            if c == expectedResponse :
                bRet = True
            else :
                raise AssertionError(ModuleName+ "." + "WaitDone" + ":  NotExpected Value ")
            break
        else :
            time.sleep(sleepMSec)
            if sleepMSec < 1 :
                sleepMSec += 0.03 # 이 루프를 반복할때마다 30ms씩 대기시간 증가 (최대 1초) 
            else  :
                raise AssertionError(ModuleName+ "." + "WaitDone" + ":  TimeOut, check device")

    return bRet

def ReadStatus(device, command) :
    regValue=[0, 0, 0, 0, 0]  
    spiCmd = MakeCmdValue(command, 1)
    regValue[4] = spiCmd
    byteOffset=0
    isOK = device.WriteReg(Register.ANA6705.SPICTL, byteOffset, len(regValue), regValue) 
    if isOK != True :
        raise AssertionError(ModuleName+ "." + "ReadStatus")

    WaitDone(device, spiCmd)

    byteOffset = 0
    status = device.ReadReg1Byte(Register.ANA6705.SPIDATA, byteOffset)
    if status == -1 :
        raise AssertionError(ModuleName+ "." + "ReadStatus")
    return status

def ReadStatus1(device) :
    return ReadStatus(device, COMMAND_READ_STATUS1)

def ReadStatus2(device) :
    return ReadStatus(device, COMMAND_READ_STATUS2)


def WriteStatus(device, command, status) :

    byteOffset = 0
    bRet = device.WriteReg1Byte(Register.ANA6705.SPIDATA, byteOffset, status)
    if bRet != True :
        raise AssertionError(ModuleName+ "." + "WriteStatus")

    regValue=[0, 0, 0, 0, 0]  
    spiCmd = MakeCmdValue(command, 1)
    regValue[4] = spiCmd
    byteOffset=0
    isOK = device.WriteReg(Register.ANA6705.SPICTL, byteOffset, len(regValue), regValue) 
    if isOK != True :
        raise AssertionError(ModuleName+ "." + "ReadStatus")

    WaitDone(device, spiCmd)

def WriteStatus1(device,status) :
    return WriteStatus(device, COMMAND_WRITE_STATUS1, status)

def WriteStatus2(device,status) :
    return WriteStatus(device, COMMAND_WRITE_STATUS2, status)


def Lock(device) :
    status2 = ReadStatus2(device)
    if (status2&0x02) != 0 :   #두번째 bit가 High이면 Unlock이다. 
        status2 &= ~0x02
        WriteStatus2(status2)
    return True

def Unlock(device) :
    status2 = ReadStatus2(device)
    if (status2&0x02) == 0 :   #두번째 bit가 Low이면 Lock상태이다.
        status2 = 0x02
        WriteStatus2(device, status2)
    return True

def IsLock(device) :
    status2 = ReadStatus2(device)
    if (status2&0x02) != 0 : 
        isLock = False   #두번째 bit가 High이면 Unlock이다. 
    else :
        isLock = True
    return isLock


def EraseSector(device, sectorAddr) :

    regValue=[0, 0, 0, 0, 0]  

    assert sectorAddr < FlashSectorMaxCount 
    memAddr = ConvertSectorAddrToMemAddr(sectorAddr)
    
    #Set Addr
    regValue[2] = memAddr & 0xFF;
    regValue[1] =(memAddr >>8) & 0xFF;
    regValue[0] = (memAddr >>16) & 0xFF;

    spiCmd = MakeCmdValue(COMMAND_SECTOR_ERASE, 1)
    regValue[4] = spiCmd
    
    byteOffset=0
    isOK = device.WriteReg(Register.ANA6705.SPICTL, byteOffset, len(regValue), regValue) 
    assert isOK

    bRet = WaitDone(device, spiCmd)
    
    return bRet

def EraseChip(device) :

    regValue=[0, 0, 0, 0, 0]  

    assert sectorAddr < FlashSectorMaxCount 
    memAddr = ConvertSectorAddrToMemAddr(sectorAddr)
    
    spiCmd = MakeCmdValue(COMMAND_CHIP_ERASE, 1)
    regValue[4] = spiCmd
    
    byteOffset=0
    isOK = device.WriteReg(Register.ANA6705.SPICTL, byteOffset, len(regValue), regValue) 
    assert isOK

    bRet = WaitDone(device, spiCmd)

    return bRet
    
def ReadDataFromHW(device, memAddr, readByteSize, dataList, dataListStartIdx=0) :

    regValue=[0, 0, 0, 0, 0]  

    assert (memAddr+readByteSize) < FlashCapacity
    assert readByteSize <= FlashReadChunkByteSize

    #Set Addr
    regValue[2] = memAddr & 0xFF
    regValue[1] =(memAddr >>8) & 0xFF
    regValue[0] = (memAddr >>16) & 0xFF

    #읽을 개수 설정 
    regValue[3] = readByteSize - 1

    #Set Cmd
    spiCmd = MakeCmdValue(COMMAND_READ, 1)
    regValue[4] = spiCmd;
    isOK = device.WriteReg(Register.ANA6705.SPICTL, 0 , len(regValue), regValue) 
    assert isOK 

    bRet = WaitDone(device, spiCmd)

    if bRet :
        isOK = device.ReadReg(Register.ANA6705.SPIDATA, 0, readByteSize, dataList, dataListStartIdx)
        assert isOK 

    return bRet


def WriteDataToHW(device, memAddr, writeByteSize, writeData, writeDataStartIdx) : 

    bRet = True
    regValue = [0,0,0,0,0]
    
    dataIdx = 0;

    assert ((memAddr + writeByteSize) <= FlashCapacity)
    assert (writeByteSize <= FlashWriteChunkByteSize)

    #//Step1. Write To Buffer
    isOK = device.WriteReg(Register.ANA6705.SPIDATA, 0 , writeByteSize, writeData, writeDataStartIdx) 
    assert isOK 

    #Set Addr
    regValue[2] = memAddr & 0xFF
    regValue[1] = (memAddr >> 8) & 0xFF
    regValue[0] = (memAddr >> 16) & 0xFF

    #Write할 개수 
    regValue[3] = writeByteSize - 1; #//SPI_LENG[0,7] SPI_LENG+1 Bytes

    #Set Cmd
    spiCmd = MakeCmdValue(COMMAND_WRITE, 1)
    regValue[4] = spiCmd
    isOK = device.WriteReg(Register.ANA6705.SPICTL, 0 , len(regValue), regValue) 
    assert isOK

    #//Step3. Wait
    bRet = WaitDone(device, spiCmd)
        
    return bRet;
