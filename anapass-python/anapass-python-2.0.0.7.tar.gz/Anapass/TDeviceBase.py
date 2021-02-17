from enum import Enum
import time
import platform
import sys
import enum
from abc import ABCMeta, abstractmethod
from Anapass import Util
from Anapass import Adc
import inspect

class TString :
    def __init__(this, str):
        this.__String = str

    def ToCTypeString(this) :
        return this.__String.encode('utf-8')

    #static method
    def ConvertToCTypeStrng(x) :
        return x.encode('utf-8')

    def ConvertCTypeStringToUnicode(x) :
        return x.decode('utf-8')

    def CStrToPyStr(byteData) :

        strLen = 0
        for idx, value in enumerate(byteData) :
            if value == 0 :
                strLen = idx
                break

        newByteData = bytearray(strLen) 
        for idx, value in enumerate(byteData) :
            if value != 0 :
                newByteData[idx] = value
            else :
                break;

        return newByteData.decode('utf-8')


class TPower :

    class Type(enum.IntEnum) :
        VBAT1=0
        ELVSS=1
        VDD1=2
        VCI1=3
        VBAT2=4
        VDD2=5
        VCI2=6

    def __init__(this):
        this.No = 0
        this.Avail=[0 for _ in range(10)]
        this.Value1=[0 for _ in range(10)]
        this.Voltage=[0.0 for _ in range(10)]
        this.Current=[0.0 for _ in range(10)]
        this.Range1=[0.0 for _ in range(10)]
        this.Range2=[0.0 for _ in range(10)]


class TChip :
    class Type(enum.IntEnum) : 
        Common=0
        ANA6705=1
        ANA6706=2

class TBoard :
    class Type(enum.IntEnum) : 
        Common=0

#
# class TDevice
#
class TDeviceBase(metaclass=ABCMeta) :

    class Type(enum.IntEnum) : 
        T5 = 0
        T5PacketAnalysis=1
        T4 = 2
        TESys=3

    class ErrorString(enum.Enum) :
        GetResp="ErrorGetResp"
    
    def __init__(this, deviceTypeValue):
        #print(DisplayName +"TRY: create " + deviceType.name )
        this.__DeviceTypeValue = deviceTypeValue
        this.__SoutAdcMaxChCount=16
        this.__LdoAdcMaxChCount=16
        this.__RegAdcMaxChCount=16

    def __del__(this):
        #print("TDevice::~TDevice")
        TDeviceDestroy(this.__DeviceHandle)
    
    
    def TestVlin1Adc(this) :
        this.Vlin1AdcSetSamples(1111)
        this.Vlin1AdcSetInterval(22222)
        this.Vlin1AdcSetChannelOn(33333)
        this.Vlin1AdcSetChannelOff(44444)
        this.Vlin1AdcSetMode(55555)
        print("Volt(0) : %d "%this.Vlin1AdcGetVoltage(0))
        print("Volt-VLIN1 : %d "%this.Vlin1AdcGetVoltageVLIN1())
        print("Volt-VBAT : %d "%this.Vlin1AdcGetVoltageVBAT())
        print("Volt-ELVDD : %d "%this.Vlin1AdcGetVoltageELVDD())
        print("Curr(0) : %d "%this.Vlin1AdcGetCurrent(0))
        print("Curr-VLIN1 : %d "%this.Vlin1AdcGetCurrentVLIN1())
        print("Curr-VBAT : %d "%this.Vlin1AdcGetCurrentVBAT())
        print("Curr-ELVDD : %d "%this.Vlin1AdcGetCurrentELVDD())

    def TestVciAdc(this) :
        this.VciAdcSetSamples(111)
        this.VciAdcSetInterval(222)
        this.VciAdcSetChannelOn(333)
        this.VciAdcSetChannelOff(444)
        this.VciAdcSetMode(555)
        print("Volt(0) : %d "%this.VciAdcGetVoltage(0))
        print("Volt-VCI : %d "%this.VciAdcGetVoltageVCI())
        print("Volt-VDDR : %d "%this.VciAdcGetVoltageVDDR())
        print("Volt-VDDI : %d "%this.VciAdcGetVoltageVDDI())
        print("Curr(0) : %d "%this.VciAdcGetCurrent(0))
        print("Curr-VCI : %d "%this.VciAdcGetCurrentVCI())
        print("Curr-VDDR : %d "%this.VciAdcGetCurrentVDDR())
        print("Curr-VDDI : %d "%this.VciAdcGetCurrentVDDI())

    def TestSoutAdc(this) :
        this.SoutAdcSetDevConfig(77777)
        for chIdx in range(this.__SoutAdcMaxChCount) :
            this.SoutAdcSetInConfig(chIdx, 6600+chIdx)
        this.SoutAdcSetRBSel(1)
        for chIdx in range(this.__SoutAdcMaxChCount) :
            print("SoutAdc-Volt(%d) : %d "%(chIdx, this.SoutAdcGetVoltage(chIdx)))
        voltList=this.SoutAdcGetAllVoltage()
        for chIdx in range(this.__SoutAdcMaxChCount) :
            print("SoutAdc-VoltAll(%d) : %d "%(chIdx, voltList[chIdx]))
    
    def TestLdoAdc(this) :
        for chIdx in range(this.__LdoAdcMaxChCount) :
            this.LdoAdcSetInConfig(chIdx, 4500+chIdx)
        for chIdx in range(this.__LdoAdcMaxChCount) :
            print("LdoAdc-Volt(%d) : %d "%(chIdx, this.LdoAdcGetVoltage(chIdx)))
        voltList=this.LdoAdcGetAllVoltage()
        for chIdx in range(this.__LdoAdcMaxChCount) :
            print("LdoAdc-VoltAll(%d) : %d "%(chIdx, voltList[chIdx]))
    
    def TestRegAdc(this) :
        for chIdx in range(this.__RegAdcMaxChCount) :
            this.RegAdcSetInConfig(chIdx, 3400+chIdx)
        for chIdx in range(this.__RegAdcMaxChCount) :
            print("RegAdc-Volt(%d) : %d "%(chIdx, this.RegAdcGetVoltage(chIdx)))
        voltList=this.RegAdcGetAllVoltage()
        for chIdx in range(this.__RegAdcMaxChCount) :
            print("RegAdc-VoltAll(%d) : %d "%(chIdx, voltList[chIdx]))
        
    @abstractmethod            
    def SysSetServerIPAddr(this, serverIPAddr) : pass

    @abstractmethod            
    def SysSetBoardID(this, boardID) : pass

    #TDEVICE_API TED_BOOL TDeviceSysSetBoardID(void* hdl, int boardID);
    @abstractmethod            
    def SysSetTcLocalSave(this, boardID, bFlag) : pass
        
    @abstractmethod            
    def SysGetDutIndexAllDeviceValue(this) : pass

    @abstractmethod            
    def SysGetDutCount(this) : pass

    @abstractmethod            
    def SysGetTickCount64(this) : pass

    @abstractmethod            
    def SysGetCurUtcTime(this) : pass

    @abstractmethod            
    def SysGetUtcTimeKST(this, year, month, day, hour, min, sec) : pass

    @abstractmethod            
    def SysGetErrFlag(this) : pass

    @abstractmethod            
    def SysMipiLock(this) : pass

    @abstractmethod            
    def SysMipiUnlock(this) : pass

    @abstractmethod            
    def SysMipiIsLock(this) : pass

    @abstractmethod            
    def Connect(this) : pass

    @abstractmethod            
    def Disonnect(this) : pass
        
    @abstractmethod            
    def SendTxtCmd(this, cmd) : pass

    @abstractmethod            
    def SendTxtCmdReadResp(this, cmd, maxRespByteSize) : pass

    @abstractmethod            
    def SendCtrlCmd(this, cmd) :  pass

    def Reset(this) :
        return this.SendCtrlCmd('RESET')

    def Next(this) :
        return this.SendCtrlCmd('NEXT')

    def Back(this) :
        return this.SendCtrlCmd('BACK')

    @abstractmethod            
    def ReadReg(this, regAddr, byteOffset, readCount, regValueList, regValueListStartIdx=0) : pass

    @abstractmethod            
    def ReadReg1Byte(this, regAddr, byteOffset) : pass

    @abstractmethod
    def WriteReg(this, regAddr, byteOffset, writeCount, regValueList, writeDataStartIdx=0) : pass

    @abstractmethod
    def WriteReg1Byte(this, regAddr, byteOffset, regValue) : pass
        
    @abstractmethod
    def WriteCtrlReg(this, regAddr) : pass

    #COMM_API Bool TedDD_DSIM_MipiReadReg(int dutIdx, int addr, int byteOffset, int readCount, unsigned char* buf, int bufMaxByteSize);
    @abstractmethod
    def DD_DSIM_MipiReadReg(this, dutIdx, regAddr, byteOffset, readCount) : pass

    #COMM_API unsigned char TedDD_DSIM_MipiReadReg1Byte(int dutIdx, int addr, int byteOffset);
    @abstractmethod
    def DD_DSIM_MipiReadReg1Byte(this, dutIdx, regAddr, byteOffset) : pass

    #COMM_API Bool TedDD_DSIM_MipiReadReg(int dutIdx, int addr, int byteOffset, int readCount, unsigned char* buf, int bufMaxByteSize);
    @abstractmethod
    def DD_DSIM_MipiWriteReg(this, dutIdx, regAddr, byteOffset, regValueList) : pass

    #COMM_API Bool TedDD_DSIM_MipiWriteReg1Byte(int dutIdx, int addr, int byteOffset, unsigned char data);
    @abstractmethod
    def DD_DSIM_MipiWriteReg1Byte(this, dutIdx, regAddr, byteOffset, regValue) : pass

    #WREG0=0x39, [Addr], [regVal0], [regVal1].....
    #COMM_API Bool TedDD_DSIM_MipiWriteReg39(int dutIdx, int addr, int writeCount, unsigned char* buf);
    @abstractmethod
    def DD_DSIM_MipiWriteReg39(this, dutIdx, regAddr, regValueList) : pass

    #WREG0=0x15, [Addr], [regVal]
    #COMM_API Bool TedDD_DSIM_MipiWriteReg15(int dutIdx, int addr, unsigned char value);
    @abstractmethod
    def DD_DSIM_MipiWriteReg15(this, dutIdx, regAddr, regValue) : pass

    #WREG0=0x05, [Addr]
    #COMM_API Bool TedDD_DSIM_MipiWriteReg05(int dutIdx, int addr);
    @abstractmethod
    def DD_DSIM_MipiWriteReg05(this, dutIdx, regAddr) : pass

    #WREG0=0x07, [value]   :   Compressd Mode Command
    #COMM_API Bool TedDD_DSIM_MipiWriteReg07(int dutIdx, int addr);
    @abstractmethod
    def DD_DSIM_MipiWriteReg07(this, dutIdx, value) : pass
        
    @abstractmethod
    def CatchPower(this, powerInfo) : pass

    @abstractmethod
    def PatternConnect(this) : pass

    @abstractmethod
    def PatternDisconnect(this) : pass

    @abstractmethod
    def PatternIsConnect(this) : pass

    @abstractmethod
    def PatternSetCommand(this, ptrnCmd) : pass

    @abstractmethod
    def PatternPaint(this, r, g, b, a) : pass

    @abstractmethod
    def PatternUpdateScreen(this) : pass

    @abstractmethod
    def PatternDrawImage(this, imgFileName) : pass

    @abstractmethod
    def PatternScreenVerify(this, r, g, b) : pass

    @abstractmethod
    def ANA670X_GetChipIDCount(this) : pass

    @abstractmethod
    def ANA670X_GetChipID(this, dutIdx) : pass

    @abstractmethod
    def ANA670X_GetProductRevisionBytesCount(this) : pass

    @abstractmethod
    def ANA670X_GetProductRevisionBytes(this, dutIdx) : pass

    @abstractmethod
    def ANA670X_SetFrameRate(this, dutIdx, fr) : pass

    @abstractmethod
    def ANA670X_GetFrameRate(this, dutIdx) : pass

    @abstractmethod
    def SysDelay(this, delay) : pass
        
    @abstractmethod
    def DebugMessage(this, msg) : pass
        
    @abstractmethod
    def DebugFuncEnter(this, funcName) : pass
    
    @abstractmethod
    def DebugFuncLeave(this, funcName) : pass
    
    @abstractmethod
    def DD_FB_blank(this, dutIdx, value) : pass
    @abstractmethod
    def DD_DSIM_manual_ctrl(this, dutIdx, value) : pass
    @abstractmethod
    def DD_DSIM_power_ctrl(this, dutIdx, value) : pass
    @abstractmethod
    def DD_DSIM_source_cal(this, dutIdx, value) : pass
    @abstractmethod
    def DD_DSIM_sleepin(this, dutIdx, value) : pass
    @abstractmethod
    def DD_DSIM_sleepout(this, dutIdx, value) : pass
    @abstractmethod
    def DD_DSIM_deep_standby(this, dutIdx, value) : pass
    @abstractmethod
    def DD_DSIM_displayon(this, dutIdx, value) : pass
    @abstractmethod
    def DD_DSIM_reset_ctrl(this, dutIdx, value) : pass

    #//VLIN1_ADC
    #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetSamples(TDEVICE_HDL hdl, int value);  
    @abstractmethod
    def Vlin1AdcSetSamples(this, dutIdx, value) : pass

    #DEVICE_API TED_BOOL TDeviceVlin1AdcSetInterval(TDEVICE_HDL hdl, int value); 
    @abstractmethod
    def Vlin1AdcSetInterval(this, dutIdx, value) : pass

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetChannelOn(TDEVICE_HDL hdl, int chIdx);
    @abstractmethod
    def Vlin1AdcSetChannelOn(this, dutIdx, value) : pass

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetChannelOff(TDEVICE_HDL hdl, int chIdx); 
    @abstractmethod
    def Vlin1AdcSetChannelOff(this, dutIdx, value) : pass

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetMode(TDEVICE_HDL hdl, int value);  
    @abstractmethod
    def Vlin1AdcSetMode(this, dutIdx, value) : pass

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetVoltage(TDEVICE_HDL hdl, int chIdx);  
    @abstractmethod
    def Vlin1AdcGetVoltage(this, dutIdx, chIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetVoltageVLIN1(TDEVICE_HDL hdl);  
    @abstractmethod
    def Vlin1AdcGetVoltageVLIN1(this, dutIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetVoltageVBAT(TDEVICE_HDL hdl);  
    @abstractmethod
    def Vlin1AdcGetVoltageVBAT(this, dutIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetVoltageELVDD(TDEVICE_HDL hdl);  
    @abstractmethod
    def Vlin1AdcGetVoltageELVDD(this, dutIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetCurrent(TDEVICE_HDL hdl, int chIdx);  
    @abstractmethod
    def Vlin1AdcGetCurrent(this, dutIdx, chIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetCurrentVLIN1(TDEVICE_HDL hdl); 
    @abstractmethod
    def Vlin1AdcGetCurrentVLIN1(this, dutIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetCurrentVBAT(TDEVICE_HDL hdl); 
    @abstractmethod
    def Vlin1AdcGetCurrentVBAT(this, dutIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetCurrentELVDD(TDEVICE_HDL hdl); 
    @abstractmethod
    def Vlin1AdcGetCurrentELVDD(this, dutIdx) : pass

    #//VCI_ADC
    #TDEVICE_API TED_BOOL TDeviceVciAdcSetSamples(TDEVICE_HDL hdl, int value); 
    @abstractmethod
    def VciAdcSetSamples(this, dutIdx, value) : pass

    #TDEVICE_API TED_BOOL TDeviceVciAdcSetInterval(TDEVICE_HDL hdl, int value);
    @abstractmethod
    def VciAdcSetInterval(this, dutIdx, value) : pass

    #TDEVICE_API TED_BOOL TDeviceVciAdcSetChannelOn(TDEVICE_HDL hdl, int chIdx);
    @abstractmethod
    def VciAdcSetChannelOn(this, dutIdx, value) : pass

    #TDEVICE_API TED_BOOL TDeviceVciAdcSetChannelOff(TDEVICE_HDL hdl, int chIdx);
    @abstractmethod
    def VciAdcSetChannelOff(this, dutIdx, value) : pass

    #TDEVICE_API TED_BOOL TDeviceVciAdcSetMode(TDEVICE_HDL hdl, int value);
    @abstractmethod
    def VciAdcSetMode(this, dutIdx, value) : pass
        
    #TDEVICE_API int TDeviceVciAdcGetVoltage(TDEVICE_HDL hdl, int chIdx);
    @abstractmethod
    def VciAdcGetVoltage(this, dutIdx, chIdx) : pass

    #TDEVICE_API int TDeviceVciAdcGetVoltageVCI(TDEVICE_HDL hdl);
    @abstractmethod
    def VciAdcGetVoltageVCI(this, dutIdx) : pass

    #TDEVICE_API int TDeviceVciAdcGetVoltageVDDR(TDEVICE_HDL hdl);
    @abstractmethod
    def VciAdcGetVoltageVDDR(this, dutIdx) : pass

    #TDEVICE_API int TDeviceVciAdcGetVoltageVDDI(TDEVICE_HDL hdl);
    @abstractmethod
    def VciAdcGetVoltageVDDI(this, dutIdx) : pass

    #TDEVICE_API int TDeviceVciAdcGetCurrent(TDEVICE_HDL hdl, int chIdx);
    @abstractmethod
    def VciAdcGetCurrent(this, dutIdx, chIdx) : pass

    #DEVICE_API int TDeviceVciAdcGetCurrentVCI(TDEVICE_HDL hdl);
    @abstractmethod
    def VciAdcGetCurrentVCI(this, dutIdx) : pass

    #TDEVICE_API int TDeviceVciAdcGetCurrentVDDR(TDEVICE_HDL hdl);
    @abstractmethod
    def VciAdcGetCurrentVDDR(this, dutIdx) : pass

    #TDEVICE_API int TDeviceVciAdcGetCurrentVDDI(TDEVICE_HDL hdl);
    @abstractmethod
    def VciAdcGetCurrentVDDI(this, dutIdx) : pass

    #//SDOUT ADC
    #define TED_SDOUTADC_MAX_CH_COUNT 16
    #TDEVICE_API int TDeviceSoutAdcSetDevConfig(TDEVICE_HDL hdl, int value);
    @abstractmethod
    def SoutAdcSetDevConfig(this, dutIdx, value) : pass

    #TDEVICE_API int TDeviceSoutAdcSetInConfig(TDEVICE_HDL hdl, int chIdx,  int value); 
    @abstractmethod
    def SoutAdcSetInConfig(this, dutIdx, chIdx, value) : pass

    #COMM_API Bool TedAdcSoutSetRBSel(int dutIdx, int value)
    @abstractmethod
    def AdcSoutSetRBSel(this, dutIdx, value) : pass

    #COMM_API int TedAdcSoutGetRBSel(int dutIdx)
    @abstractmethod
    def AdcSoutGetRBSel(this, dutIdx) : pass

    #TDEVICE_API int TDeviceSoutAdcGetChannelCount(TDEVICE_HDL hdl);
    @abstractmethod
    def SoutAdcGetChannelCount(this, dutIdx) : pass

    #TDEVICE_API int TDeviceSoutAdcGetVoltage(TDEVICE_HDL hdl, int chIdx);  
    @abstractmethod
    def SoutAdcGetVoltage(this, dutIdx, chIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceSoutAdcGetAllVoltage(TDEVICE_HDL hdl, int* voltageArray);
    @abstractmethod
    def SoutAdcGetAllVoltage(this, dutIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceLdoAdcSetInConfig(TDEVICE_HDL hdl, int chIdx, int value);
    @abstractmethod
    def LdoAdcSetInConfig(this, dutIdx, chIdx, value) : pass

    #TDEVICE_API int TDeviceLdoAdcGetChannelCount(TDEVICE_HDL hdl);
    @abstractmethod
    def LdoAdcGetChannelCount(this, dutIdx) : pass

    #TDEVICE_API int TDeviceLdoAdcGetVoltage(TDEVICE_HDL hdl, int chIdx);
    @abstractmethod
    def LdoAdcGetVoltage(this, dutIdx, chIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceLdoAdcGetAllVoltage(TDEVICE_HDL hdl, int* voltageArray);
    @abstractmethod
    def LdoAdcGetAllVoltage(this, dutIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceRegAdcSetInConfig(TDEVICE_HDL hdl, int chIdx, int value);
    @abstractmethod
    def RegAdcSetInConfig(this, dutIdx, chIdx, value) : pass

    #TDEVICE_API int TDeviceRegAdcGetChannelCount(TDEVICE_HDL hdl);
    @abstractmethod
    def RegAdcGetChannelCount(this, dutIdx) : pass

    #TDEVICE_API int TDeviceRegAdcGetVoltage(TDEVICE_HDL hdl, int chIdx);
    @abstractmethod
    def RegAdcGetVoltage(this, dutIdx, chIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceLdoAdcGetAllVoltage(TDEVICE_HDL hdl, int* voltageArray);
    @abstractmethod
    def RegAdcGetAllVoltage(this, dutIdx) : pass

    @abstractmethod            
    def AgingNotifyPyStart(this, pyFileName) : pass

    @abstractmethod            
    def AgingNotifyPyStop(this, pyFileName) : pass

    #COMM_API Bool TedAgingSetCurJobInfo(int dutIdx, int jobID, int status, int scIdx, int scCount, const char* desc);
    @abstractmethod
    def AgingSetCurJobInfo(this, dutIdx, jobID, status, scIdx, scCount, desc) : pass

    #COMM_API Bool TedAgingSetCurScInfo(int dutIdx, int scID, int status, int tcIdx, int tcCount, const char* desc);
    @abstractmethod
    def AgingSetCurScInfo(this, dutIdx, scID, status,tcIdx, tcCount, desc) : pass

    #COMM_API Bool TedAgingSetCurTcInfo(int dutIdx, int tcID, int status, int tcStepIdx, int tcStepCount, const char* desc);
    @abstractmethod
    def AgingSetCurTcInfo(this, dutIdx, tcID, status,tcStepIdx, tcStepCount, desc) : pass

    #COMM_API Bool TedAgingSetCurTcStepInfo(int dutIdx, int tcStepID, int status, const char* desc);
    @abstractmethod
    def AgingSetCurTcStepInfo(this, dutIdx, tcStepID, status, desc) : pass

    #TCOMM_API Bool TedAgingMeasureADC(int dutIdx, /*OUT*/void* res);
    @abstractmethod
    def AgingMeasureADC(this, dutIdx) : pass

    #COMM_API int TedAgingMeasureADCResultStructureByteSize();
    @abstractmethod
    def AgingMeasureADCResultStructureByteSize(this) : pass

    #COMM_API int TedAdcGetInvalidValue();
    @abstractmethod
    def AdcGetInvalidValue(this) : pass

    @abstractmethod
    def AdcGetInvalidFloat(this) : pass

    #COMM_API int TedAdcGetGroupCount(int dutIdx);
    @abstractmethod
    def AdcGetGroupCount(this, dutIdx) : pass

    #COMM_API Bool TedAdcGetGroupName(int dutIdx, int groupIdx, char* szGroupName);
    @abstractmethod
    def AdcGetGroupName(this, dutIdx, grpIdx) : pass

    #COMM_API int TedAdcGetGroupIndexByName(int dutIdx, const char* groupName);
    @abstractmethod
    def AdcGetGroupIndexByName(this, dutIdx, grpName) : pass

    #COMM_API int TedAdcGetChannelCount(int dutIdx, int groupIdx);
    @abstractmethod
    def AdcGetChannelCount(this, dutIdx, grpIdx) : pass

    #COMM_API Bool TedAdcGetChannelName(int dutIdx, int groupIdx, int chIdx, /*OUT*/ char* szChName);
    @abstractmethod
    def AdcGetChannelName(this, dutIdx, grpIdx, chIdx) : pass

    #COMM_API int TedAdcGetGroupIndexByPsID(int dutIdx, int psID);
    @abstractmethod
    def AdcGetGroupIndexByPsID(this, dutIdx, psID) : pass

    #COMM_API int TedAdcGetChannelIndexByPsID(int dutIdx, int psID);
    @abstractmethod
    def AdcGetChannelIndexByPsID(this, dutIdx, psID) : pass

    #COMM_API Bool TedAdcSetDevConfig(int dutIdx, int groupIdx, int value);
    @abstractmethod
    def AdcSetDevConfig(this, dutIdx, grpIdx, value) : pass

    #COMM_API int TedAdcGetDevConfig(int dutIdx, int groupIdx);
    @abstractmethod
    def AdcGetDevConfig(this, dutIdx, grpIdx) : pass

    #COMM_API Bool TedAdcSetInConfig(int dutIdx, int groupIdx, int chIdx, int value);
    @abstractmethod
    def AdcSetInConfig(this, dutIdx, grpIdx, value) : pass

    #COMM_API int TedAdcGetInConfig(int dutIdx, int groupIdx, int chIdx);
    @abstractmethod
    def AdcGetInConfig(this, dutIdx, grpIdx, chIdx) : pass

    #COMM_API int TedAdcGetVoltage(int dutIdx, int groupIdx, int chIdx);
    @abstractmethod
    def AdcGetVoltage(this, dutIdx, grpIdx, chIdx) : pass

    #TDEVICE_API float TDeviceAdcGetVoltFloat(void* hdl, int dutIdx, int groupIdx, int chIdx)
    @abstractmethod
    def AdcGetVoltFloat(this, dutIdx, grpIdx, chIdx) : pass

    #COMM_API int TedAdcGetVoltageByPsID(int dutIdx, int psID);
    @abstractmethod
    def AdcGetVoltageByPsID(this, dutIdx, psID) : pass

    #COMM_API float TedAdcGetVoltFloatByPsID(int dutIdx, int psID);
    @abstractmethod
    def AdcGetVoltFloatByPsID(this, dutIdx, psID) : pass

    #COMM_API Bool TedAdcGetAllVoltage(int dutIdx, int groupIdx, int* valueArray);
    @abstractmethod
    def AdcGetAllVoltage(this, dutIdx, grpIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceAdcGetAllVoltFloat(void* hdl, int dutIdx, int groupIdx, float* fvalueArray);
    @abstractmethod
    def AdcGetAllVoltFloat(this, dutIdx, grpIdx) : pass

    #COMM_API int TedAdcGetCurrent(int dutIdx, int groupIdx, int chIdx);
    @abstractmethod
    def AdcGetCurrent(this, dutIdx, grpIdx, chIdx) : pass

    #TDEVICE_API float TDeviceAdcGetCurrFloat(void* hdl, int dutIdx, int groupIdx, int chIdx)
    @abstractmethod
    def AdcGetCurrFloat(this, dutIdx, grpIdx, chIdx) : pass

    #COMM_API int TedAdcGetCurrentByPsID(int dutIdx, int psID);
    @abstractmethod
    def AdcGetCurrentByPsID(this, dutIdx, psID) : pass

    #COMM_API float TedAdcGetCurrFloatByPsID(int dutIdx, int psID);
    @abstractmethod
    def AdcGetCurrFloatByPsID(this, dutIdx, psID) : pass

    #COMM_API Bool TedAdcGetAllCurrent(int dutIdx, int groupIdx, int* valueArray);
    @abstractmethod
    def AdcGetAllCurrent(this, dutIdx, grpIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceAdcGetAllCurrFloat(void* hdl, int dutIdx, int groupIdx, float* fvalueArray);
    @abstractmethod
    def AdcGetAllCurrFloat(this, dutIdx, grpIdx) : pass

    #COMM_API Bool TedAdcSoutSetRBSel(int dutIdx, int value);
    @abstractmethod
    def AdcSoutSetRBSel(this, dutIdx, value) : pass

    #COMM_API int TedAdcSoutGetRBSel(int dutIdx);
    @abstractmethod
    def AdcSoutGetRBSel(this, dutIdx) : pass

    #TDEVICE_API TED_BOOL TDeviceAdcGetAllFloat(void* hdl, int dutIdx, int groupIdx, float* fVoltArray, float* fCurrArray)
    @abstractmethod
    def AdcGetAllFloat(this, dutIdx, groupIdx) : pass

    #TDEVICE_API TFILETRANSFER_HDL TFileTransferCreate(enum TFileTransferType type, TDEVICE_HDL deviceHandle);
    @abstractmethod
    def TFileTransferCreate(this, type) : pass
    
    #TDEVICE_API TED_BOOL TFileTransferDestroy(TFILETRANSFER_HDL fileTransferHandle);
    @abstractmethod
    def TFileTransferDestroy(this, fileTransferHandle) : pass
    
    #TDEVICE_API TED_BOOL TFileTransferStart(TFILETRANSFER_HDL fileTransferHandle, const char* fileName);
    @abstractmethod
    def TFileTransferStart(this, fileTransferHandle, fileName) : pass

    #TDEVICE_API TED_BOOL TFileTransferStop(TFILETRANSFER_HDL fileTransferHandle);
    @abstractmethod
    def TFileTransferStop(this, fileTransferHandle) : pass
    
    #TDEVICE_API int TFileTransferGetFileByteSize(TFILETRANSFER_HDL fileTransferHandle);
    @abstractmethod
    def TFileTransferGetFileByteSize(this, fileTransferHandle) : pass
        
    #TDEVICE_API int TFileTransferGetTransferByteSize(TFILETRANSFER_HDL fileTransferHandle);
    @abstractmethod
    def TFileTransferGetTransferByteSize(this, fileTransferHandle) : pass

    #TDEVICE_API TED_BOOL TFileTransferIsStart(TFILETRANSFER_HDL fileTransferHandle);
    @abstractmethod
    def TFileTransferIsStart(this, fileTransferHandle) : pass
    
    #TDEVICE_API TED_BOOL TFileTransferIsDone(TFILETRANSFER_HDL fileTransferHandle);
    @abstractmethod
    def TFileTransferIsDone(this, fileTransferHandle) : pass

    #TDEVICE_API TED_BOOL TFileTransferIsError(TFILETRANSFER_HDL fileTransferHandle);
    @abstractmethod
    def TFileTransferIsError(this, fileTransferHandle) : pass
        
    #TDEVICE_API enum TFileTransferError TFileTransferGetLastError(TFILETRANSFER_HDL fileTransferHandle);
    @abstractmethod
    def TFileTransferGetLastError(this, fileTransferHandle) : pass


