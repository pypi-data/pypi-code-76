from Anapass.TModule import *
from Anapass.ANA6705 import ANA6705_FlashMipiToSpi
from Anapass.ANA6706 import ANA6706_FlashMipiToSpi
from abc import ABCMeta, abstractmethod
from Anapass import Util
import enum

class Type(enum.IntEnum) : 
        MipiToSpi=0

def CreateInstance(device, chipType, flashType, boardType=TBoard.Type.Common) :
        if chipType == TChip.Type.ANA6705 :
            flash = FlashMipiToSpiANA6705(device)
        elif chipType == TChip.Type.ANA6706 :
            flash = FlashMipiToSpiANA6706(device)
        else : 
            raise ArgumentError("[Flash::CreateInstance] The value of ChipType is invalid")
        return flash


########################################################################################################################
#
#  class Flash
#
########################################################################################################################
class Flash(metaclass=ABCMeta) :
    def __init__(this, device):
        this._Device = device

    @abstractmethod
    def GetCapacityByteSize(this) : pass
    @abstractmethod
    def GetSectorMaxCount(this) : pass
    @abstractmethod
    def ConvertMemAddrToSectorAddr(this, memAddr) : pass
    @abstractmethod
    def ConvertSectorAddrToMemAddr(this, sectorAddr) : pass
    @abstractmethod
    def GetFlashReadChunkByteSize(this) : pass
    @abstractmethod
    def GetFlashWriteChunkByteSize(this) : pass
    @abstractmethod
    def GetFlashSectorByteSize(this) : pass

    @abstractmethod
    def ReadStatus1(this) : pass
    @abstractmethod
    def ReadStatus2(this) : pass
    @abstractmethod
    def WriteStatus1(this, status) : pass
    @abstractmethod
    def WriteStatus2(this, status) : pass
    @abstractmethod
    def Lock(this) : pass
    @abstractmethod
    def Unlock(this) : pass
    @abstractmethod
    def IsLock(this) : pass
    @abstractmethod
    def EraseSector(this, sectorAddr) : pass
    @abstractmethod
    def ReadDataFromHW(this, memAddr, readByteSize, dataList, dataListStartIdx) : pass
    @abstractmethod
    def WriteDataToHW(this, memmAddr, writeByteSize, writeData, dataIdx) : pass

    #API
    def Read(this, memAddr, readDataByteSize, outData, workAgent=None) : 
        bRet = False
        flashChunkByteSize = this.GetFlashReadChunkByteSize()
        flashSectorByteSize = this.GetFlashSectorByteSize()
        curDataIdx = 0;
        curMemAddr = memAddr; 

        while curDataIdx < readDataByteSize :
            if ((curDataIdx + flashChunkByteSize) > readDataByteSize) :
                readByteSize = readDataByteSize - curDataIdx;
            else :
                readByteSize = flashChunkByteSize;

            bRet = this.ReadDataFromHW(curMemAddr, readByteSize, outData, curDataIdx);
            if bRet != True :
                break

            curDataIdx += readByteSize;
            curMemAddr += readByteSize;

            if workAgent != None :
                workAgent.IncCurValue(readByteSize)
       
        return bRet;

    #API
    def WriteToSector(this, sectorAddr, writeData, writeDataStartIdx, workAgent=None) : 

        bRet = False
        flashChunkByteSize = this.GetFlashWriteChunkByteSize();
        flashSectorByteSize = this.GetFlashSectorByteSize();
        curDataIdx = 0;
        curMemAddr = this.ConvertSectorAddrToMemAddr(sectorAddr);

        while (curDataIdx < flashSectorByteSize) :

            if ((curDataIdx + flashChunkByteSize) > flashSectorByteSize) :
                writeByteSize = flashSectorByteSize - curDataIdx;
            else :
                writeByteSize = flashChunkByteSize;
            

            bRet = this.WriteDataToHW(curMemAddr, writeByteSize, writeData, curDataIdx + writeDataStartIdx)
            assert bRet

            curDataIdx += writeByteSize;
            curMemAddr += writeByteSize;

            if workAgent != None :
                workAgent.IncCurValue(writeByteSize)
        
        return bRet;

    #API  //임의 크기의 데이타를  임의의 메모리에 쓴다.
    def WriteToMemory(this, memAddr, writeBytes, writenData, writeDataStartIdx, workAgent=None) : 
        bRet = False
        flashChunkByteSize = this.GetFlashWriteChunkByteSize();
        curDataIdx = 0
        curMemAddr = memAddr

        assert ((memAddr + writeDataSize) < this.GetCapacityByteSize())

        while (curDataIdx < writeDataSize) :

            if ((curDataIdx + flashChunkByteSize) > writeDataSize) :
                writeByteSize = writeDataSize - curDataIdx;
            else :
                writeByteSize = flashChunkByteSize;
            
            bRet = this.WriteDataToHW(curMemAddr, writeByteSize, writeData, curDataIdx+writeDataStartIdx)
            assert bRet

            curDataIdx += writeByteSize;
            curMemAddr += writeByteSize;

            #if (curWrittenByteSize) *curWrittenByteSize += writeByteSize;
            #if (isBreak) {
            #    if (*isBreak) {
            #        break;
            #    }
            #}

            if workAgent != None :
                workAgent.IncCurValue(writeByteSize)

        
        return bRet;

    #API
    def Write(this, memAddr, writeDataByteSize, writeData, workAgent=None) : 

        bRet = False
        dataIdx = 0
        curWriteMemAddr = memAddr;
        sectorByteSize = this.GetFlashSectorByteSize();

        assert  (memAddr + writeDataByteSize) <= this.GetCapacityByteSize()

        while (dataIdx < writeDataByteSize) :

            writeBytes = 0
            availWriteBytes = 0
            curWriteSectorAddr = this.ConvertMemAddrToSectorAddr(curWriteMemAddr);
            curWriteSectorStartMemAddr = this.ConvertSectorAddrToMemAddr(curWriteSectorAddr);
            
            #현재 Sector에서 Write가능한 ByteSize를 구한다. 
            if (curWriteSectorStartMemAddr != curWriteMemAddr) :
                assert  (curWriteMemAddr > curWriteSectorStartMemAddr)
                availWriteBytes = sectorByteSize - (curWriteMemAddr - curWriteSectorStartMemAddr);
            else :
                availWriteBytes = sectorByteSize;

            #실제 Write할 ByteSize를 구한다. 
            if ((dataIdx + availWriteBytes) < writeDataByteSize) :
                writeBytes = availWriteBytes;
            else :
                writeBytes = writeDataByteSize - dataIdx;

            #writeBytes가 Sector전체 크기와 같다면, Erase한다음  WriteToSector를 호출한다 
            if (writeBytes == sectorByteSize) :

                bRet = this.EraseSector(curWriteSectorAddr);
                assert bRet

                bRet = this.WriteToSector(curWriteSectorAddr, writeData, dataIdx, workAgent)
                assert bRet
            
            #writeBytes가 Sector보다 작다면, Sector를 읽고, Erase한다음 , Write한다.
            elif (writeBytes < sectorByteSize) :
            
                assert (curWriteMemAddr >= curWriteSectorStartMemAddr)

                #Read시간이 너무 오래 걸린다.  Sector단위로 Write한다. 
                tmpData = [0 for _ in range(sectorByteSize)] 
                secotrMemOffset = curWriteMemAddr - curWriteSectorStartMemAddr  # Sector시작 주소로부터의 메모리 Offset

                Util.ListCopy(tmpData, secotrMemOffset, writeData, dataIdx, writeBytes)

                #Sector Erase한다. 
                bRet = this.EraseSector(curWriteSectorAddr)
                assert bRet

                #Data를 쓴다. 
                bRet = this.WriteToSector(curWriteSectorAddr, tmpData, 0, workAgent);
                assert bRet


                # 1Sector를 읽은다음, 값변경후 Write하기 때문에  WriteToSector에 curWrittenByteSize를 넣으면  실제 쓴값보다 큰 값이 나온다.
                #if (curWrittenByteSize) *curWrittenByteSize += writeBytes;
            else :
                bRet = this.WriteToMemory(curWriteMemAddr, writeBytes, writenData, dataIdx, workAgent);
                assert bRet
            
            
            curWriteMemAddr += writeBytes;
            dataIdx += writeBytes;

        return bRet;



class FlashMipiToSpiANA6705(Flash) :
    def __init__(this, device):
        Flash.__init__(this, device)

    def GetCapacityByteSize(this) : 
        return ANA6705_FlashMipiToSpi.FlashCapacity

    def GetSectorMaxCount(this) : 
        return ANA6705_FlashMipiToSpi.FlashSectorMaxCount
        
    def GetFlashReadChunkByteSize(this) : 
        return ANA6705_FlashMipiToSpi.FlashReadChunkByteSize

    def GetFlashWriteChunkByteSize(this) : 
        return ANA6705_FlashMipiToSpi.FlashWriteChunkByteSize

    def GetFlashSectorByteSize(this) : 
        return ANA6705_FlashMipiToSpi.FlashSectorByteSize

    def ConvertMemAddrToSectorAddr(this, memAddr) : 
        return ANA6705_FlashMipiToSpi.ConvertMemAddrToSectorAddr(memAddr)

    def ConvertSectorAddrToMemAddr(this, sectorAddr) : 
        return ANA6705_FlashMipiToSpi.ConvertSectorAddrToMemAddr(sectorAddr)

    def ReadStatus1(this) : 
        return ANA6705_FlashMipiToSpi.ReadStatus1(this._Device)

    def ReadStatus2(this) : 
        return ANA6705_FlashMipiToSpi.ReadStatus2(this._Device)

    def WriteStatus1(this, status) : 
        return ANA6705_FlashMipiToSpi.WriteStatus1(this._Device, status)

    def WriteStatus2(this, status) : 
        return ANA6705_FlashMipiToSpi.WriteStatus2(this._Device, status)

    def Lock(this) : 
        ANA6705_FlashMipiToSpi.Lock(this._Device)

    def Unlock(this) : 
        ANA6705_FlashMipiToSpi.Unlock(this._Device)

    def IsLock(this) : 
        return ANA6705_FlashMipiToSpi.IsLock(this._Device)

    def EraseSector(this, sectorAddr) : 
        return ANA6705_FlashMipiToSpi.EraseSector(this._Device, sectorAddr)

    def ReadDataFromHW(this, memAddr, readByteSize, dataList, dataListStartIdx) : 
        return ANA6705_FlashMipiToSpi.ReadDataFromHW(this._Device, memAddr, readByteSize, dataList, dataListStartIdx)

    def WriteDataToHW(this, memAddr, writeByteSize, writeData, dataIdx) : 
        return ANA6705_FlashMipiToSpi.WriteDataToHW(this._Device, memAddr, writeByteSize, writeData, dataIdx)

class FlashMipiToSpiANA6706(Flash) :
    def __init__(this, device):
        Flash.__init__(this, device)

    def GetCapacityByteSize(this) : 
        return ANA6706_FlashMipiToSpi.FlashCapacity

    def GetSectorMaxCount(this) : 
        return ANA6706_FlashMipiToSpi.FlashSectorMaxCount
        
    def GetFlashReadChunkByteSize(this) : 
        return ANA6706_FlashMipiToSpi.FlashReadChunkByteSize

    def GetFlashWriteChunkByteSize(this) : 
        return ANA6706_FlashMipiToSpi.FlashWriteChunkByteSize

    def GetFlashSectorByteSize(this) : 
        return ANA6706_FlashMipiToSpi.FlashSectorByteSize

    def ConvertMemAddrToSectorAddr(this, memAddr) : 
        return ANA6706_FlashMipiToSpi.ConvertMemAddrToSectorAddr(memAddr)

    def ConvertSectorAddrToMemAddr(this, sectorAddr) : 
        return ANA6706_FlashMipiToSpi.ConvertSectorAddrToMemAddr(sectorAddr)

    def ReadStatus1(this) : 
        return ANA6706_FlashMipiToSpi.ReadStatus1(this._Device)

    def ReadStatus2(this) : 
        return ANA6706_FlashMipiToSpi.ReadStatus2(this._Device)

    def WriteStatus1(this, status) : 
        return ANA6706_FlashMipiToSpi.WriteStatus1(this._Device, status)

    def WriteStatus2(this, status) : 
        return ANA6706_FlashMipiToSpi.WriteStatus2(this._Device, status)

    def Lock(this) : 
        ANA6706_FlashMipiToSpi.Lock(this._Device)

    def Unlock(this) : 
        ANA6706_FlashMipiToSpi.Unlock(this._Device)

    def IsLock(this) : 
        return ANA6706_FlashMipiToSpi.IsLock(this._Device)

    def EraseSector(this, sectorAddr) : 
        return ANA6706_FlashMipiToSpi.EraseSector(this._Device, sectorAddr)

    def ReadDataFromHW(this, memAddr, readByteSize, dataList, dataListStartIdx) : 
        return ANA6706_FlashMipiToSpi.ReadDataFromHW(this._Device, memAddr, readByteSize, dataList, dataListStartIdx)

    def WriteDataToHW(this, memAddr, writeByteSize, writeData, dataIdx) : 
        return ANA6706_FlashMipiToSpi.WriteDataToHW(this._Device, memAddr, writeByteSize, writeData, dataIdx)

