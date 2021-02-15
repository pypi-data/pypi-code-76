from Anapass import TModule
from Anapass import FlashMemory
from Anapass.AppShell import AppClass
from Anapass import Util
import easygui 
import time
import threading

def ReadStatus(app, tupleArg) :
    flash = FlashMemory.CreateInstance(app.GetDevice(), app.GetChipType(), FlashMemory.Type.MipiToSpi)
    status1 = flash.ReadStatus1()
    status2 = flash.ReadStatus2()
    print("status1= ", "0x%02X"%status1)
    print("status2= ", "0x%02X"%status2)

def ReadStatus1(app, tupleArg) :
    flash = FlashMemory.CreateInstance(app.GetDevice(), app.GetChipType(), FlashMemory.Type.MipiToSpi)
    status1 = flash.ReadStatus1()
    print("status1= ", "0x%02X"%status1)
    
def ReadStatus2(app, tupleArg) :
    flash = FlashMemory.CreateInstance(app.GetDevice(), app.GetChipType(), FlashMemory.Type.MipiToSpi)
    status2 = flash.ReadStatus2()
    print("status2= ", "0x%02X"%status2)

def WriteStatus1(app, tupleArg) :
    try :
        writeStatus = int(tupleArg[0], 16)
    except IndexError :
        print("[WriteStatus1] tupleArg[0] IndexError, input StatusNumber(Hex)")
    except ValueError :
        print("[WriteStatus1] tupleArg[0] ValueError,  Value is not convertable to Hex-Integer")
    else :
        print("[WriteStatus1] writeStaus= 0x%02X" % writeStatus)
        flash = FlashMemory.CreateInstance(app.GetDevice(), app.GetChipType(), FlashMemory.Type.MipiToSpi)
        flash.WriteStatus1(writeStatus)
        vefifyStatus = flash.ReadStatus1()
        print("[WriteStatus1] vefifyStatus= 0x%02X" % vefifyStatus)
        
def WriteStatus2(app, tupleArg) :
    try :
        writeStatus = int(tupleArg[0], 16)
    except IndexError :
        print("[WriteStatus2] tupleArg[0] IndexError, input StatusNumber(Hex)")
    except ValueError :
        print("[WriteStatus2] tupleArg[0] ValueError,  Value is not convertable to Hex-Integer")
    else :
        print("[WriteStatus2] writeStaus= 0x%02X" % writeStatus)
        flash = FlashMemory.CreateInstance(app.GetDevice(), app.GetChipType(), FlashMemory.Type.MipiToSpi)
        flash.WriteStatus2(writeStatus)
        vefifyStatus = flash.ReadStatus2()
        print("[WriteStatus2] vefifyStatus= 0x%02X" % vefifyStatus)

def Lock(app, tupleArg) :
    flash = FlashMemory.CreateInstance(app.GetDevice(), app.GetChipType(), FlashMemory.Type.MipiToSpi)
    flash.Lock();
        
def Unlock(app, tupleArg) :
    flash = FlashMemory.CreateInstance(app.GetDevice(), app.GetChipType(), FlashMemory.Type.MipiToSpi)
    flash.Unlock();

def IsLock(app, tupleArg) :
    flash = FlashMemory.CreateInstance(app.GetDevice(), app.GetChipType(), FlashMemory.Type.MipiToSpi)
    isLock = flash.IsLock()
    if(isLock) :
        print("TFlash is Lock")
    else :
        print("TFlash is Unlock")

def EraseSector(app, tupleArg) :
    try :
        sectorAddr = int(tupleArg[0], 16)
    except IndexError :
        print("IndexError, input sectorAddress(Hex) ex) tflash eraseSector 0x01 ")
    except ValueError :
        print("ValueError,  Value is not convertable to Hex-Integer ex) tflash eraseSector 0x01")
    else :
        flash = FlashMemory.CreateInstance(app.GetDevice(), app.GetChipType(), FlashMemory.Type.MipiToSpi)
        sectorMaxCount = flash.GetSectorMaxCount()
        print("sectorAddr Range : 0x0000 ~ 0x%04X"%(sectorMaxCount-1))
        if sectorAddr < sectorMaxCount:
            bRet = flash.EraseSector(sectorAddr)
            if bRet :
                print("Erase sector(0x%04X) OK"%sectorAddr)
            else :
                print("Erase sector(0x%04X) Fail"%sectorAddr)
        else :
            print("sectorAddr is invalid")

def __ReadService(flash, memAddr, readDataByteSize, isFileDump, workAgent) :
    print("__ReadService is starting..")
    outData=[0 for _ in range(readDataByteSize)]  #읽을 Register 값 개수만큼 리스트 할당 
    workAgent.Start()
    flash.Read(memAddr, readDataByteSize, outData, workAgent)
    if isFileDump :
        filePath = easygui.filesavebox()
        fp = open(filePath, "wb")
        fp.write(bytes(outData))
        fp.close()
    else :
        Util.Print.ListHex(memAddr, outData)
    workAgent.Stop()
    print("__ReadService is finished")
    
def __Read(app, tupleArg, isFileDump) :

    try :
        memAddr = int(tupleArg[0], 16)
    except IndexError :
        print("IndexError, check readAddr(hex)")
        print("   Usage) tflash read [Addr(hex)] [readByteSize(dec)]")
        return 
    except ValueError :
        print("ValueError,  The address of memory is not convertable to Hex-Integer")
        print("   Usage) tflash read [Addr(hex)] [readByteSize(dec)]")
        return 
    
    try :
        readDataByteSize = int(tupleArg[1], 10)
    except IndexError :
        print("IndexError, check readByteSize(dec)")
        print("   Usage) tflash read [Addr(hex)] [readByteSize(dec)]")
        return 
    except ValueError :
        print("ValueError,  The size is not convertable to Dec-Integer")
        print("   Usage) tflash read [Addr(hex)] [readByteSize(dec)]")
        return 

    flash = FlashMemory.CreateInstance(app.GetDevice(), app.GetChipType(), FlashMemory.Type.MipiToSpi)
    if memAddr+readDataByteSize >= flash.GetCapacityByteSize() :
        print("Flash Memroy Range :  0x00000000 ~ 0x%08X" % (flash.GetCapacityByteSize()-1))
        print("Out of Range :  memAddr=0x%08x Size=%d " % memAddr, readDataByteSize)
        return 

    workAgent = Util.WorkAgent()
    workAgent.SetMaxValue(readDataByteSize)
    thread = threading.Thread(target=__ReadService, args=(flash,  memAddr, readDataByteSize, isFileDump, workAgent))
    thread.start()
    while True :
        maxV = workAgent.GetMaxValue()
        curV = workAgent.GetCurValue()
        print("%d"%curV, "/",  "%d"%maxV, end='\r')
        if workAgent.IsStop() :
            print("Read Work is stopped")
            break
        time.sleep(0.3)


def Read(app, tupleArg) :
    __Read(app, tupleArg, False)
    

def Dump(app, tupleArg) :
    __Read(app, tupleArg, True)

def __WriteService(flash, memAddr, writeData, workAgent) :
    print("__WriteService is starting..")
    workAgent.Start()
    flash.Write(memAddr, len(writeData), writeData, workAgent)
    workAgent.Stop()
    print("__WriteService is finished")


def FileWrite(app, tupleArg) :    

    try :
        memAddr = int(tupleArg[0], 16)
    except IndexError :
        print("IndexError, check readAddr(hex)")
        print("   Usage) tflash FileWrite [Addr(hex)] ")
        return 
    except ValueError :
        print("ValueError,  The address of memory is not convertable to Hex-Integer")
        print("   Usage) tflash FileWrite [Addr(hex)] ")
        return 

    filePath = easygui.fileopenbox()
    fp = open(filePath, "rb")
    fileData = fp.read()
    fileSize = len(fileData)
    fp.close()

    flash = FlashMemory.CreateInstance(app.GetDevice(), app.GetChipType(), FlashMemory.Type.MipiToSpi)

    
    print("FileName : " + filePath)
    print("FileSize : ", fileSize)
    print("Flash Memory Addres : ", "0x%08X"%memAddr )

    workAgent = Util.WorkAgent()
    workAgent.SetMaxValue(len(fileData))
    thread = threading.Thread(target=__WriteService, args=(flash,  memAddr, fileData, workAgent))
    thread.start()
    while True :
        maxV = workAgent.GetMaxValue()
        curV = workAgent.GetCurValue()
        print("%d"%curV, "/",  "%d"%maxV, end='\r')
        if workAgent.IsStop() :
            print("Write Work is stopped")
            break
        time.sleep(0.3)
    
    #flash.Write(memAddr, len(fileData), fileData)
    #fp1 = open("d:\\work\\test.jpg", "wb")
    #fp1.write(bytes(fileData))
    #fp1.close()



shellCmd = AppClass.ShellCommand()
shellCmd.Add("ReadStatus", ReadStatus, "ReadStatus")
shellCmd.Add("ReadStatus1", ReadStatus1, "ReadStatus1")
shellCmd.Add("ReadStatus2", ReadStatus2, "ReadStatus2")
shellCmd.Add("WriteStatus1", WriteStatus1, "WriteStatus1")
shellCmd.Add("WriteStatus2", WriteStatus2, "WriteStatus2")
shellCmd.Add("Lock", Lock, "Lock")
shellCmd.Add("Unlock", Unlock, "Unlock")
shellCmd.Add("IsLock", IsLock, "IsLock")
shellCmd.Add("EraseSector", EraseSector, "EraseSector")
shellCmd.Add("Read", Read, "Read")
shellCmd.Add("Dump", Dump, "Dump")
shellCmd.Add("FileWrite", FileWrite, "FileWrite")

def Main(app, tupleArg) :
    if len(tupleArg)==0 or tupleArg[0] == "help" : 
        shellCmd.PrintHelp()
    else :
        isRunCmd = False
        cmd = tupleArg[0]
        tupleArg = tupleArg[1:]
        for shellItem in shellCmd :
                if shellItem.Run(app, cmd, tupleArg) == True :
                    isRunCmd = True
                    break
        if isRunCmd == False :
            print("[TFlash] Can't find sub command")
    