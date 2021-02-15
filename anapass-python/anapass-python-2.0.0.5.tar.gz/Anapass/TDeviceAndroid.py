
from enum import Enum
import time
import platform
import sys
import enum
import ted
from abc import ABCMeta, abstractmethod
from Anapass.TDeviceBase  import *

#
# class TDevice
#
class TDeviceAndroid(TDeviceBase) :

    def __init__(this, deviceTypeValue):
        TDeviceBase.__init__(this, deviceTypeValue)

    def __del__(this): pass
        #print("TDevice::~TDevice")
        #TDeviceDestroy(this.__DeviceHandle)
            
    def SysSetServerIPAddr(this, serverIPAddr) :
        return True

    def Connect(this) :
        return True

    def Disonnect(this) :
        return True
    
    def SysSetBoardID(this, boardID) : 
        return ted.SysSetBoardID(boardID)

    def SetTcLocalSave(this, boardID, bFlag) : 
        return ted.SysSetTcLocalSave(boardID, bFlag)

    def NotifyPyStart(this, pyFileName) : 
        return ted.SysNotifyPyStart(pyFileName)

    def NotifyPyStop(this, pyFileName) : 
        return ted.SysNotifyPyStop(pyFileName)

    def SysGetDutIndexAllDeviceValue(this) : 
        return ted.SysGetDutIndexAllDeviceValue()

    def SysGetDutCount(this) : 
        return ted.SysGetDutCount()

    def SysDelay(this, delay) :
        return ted.SysDelayMS(delay)

    def SysGetTickCount64(this) : 
        return ted.SysGetTickCount64()

    def SysGetCurUtcTime(this) : 
        return ted.SysGetCurUtcTime()

    def SysGetUtcTimeKST(this, year, month, day, hour, min, sec) : 
        return ted.SysGetUtcTimeKST(year, month, day, hour, min, sec)

    def SysGetErrFlag(this) : 
        return ted.SysGetErrFlag()

    def SysMipiLock(this) : 
        return ted.SysMipiLock()

    def SysMipiUnlock(this) : 
        return ted.SysMipiUnlock()

    def SysMipiIsLock(this) : 
        return ted.SysMipiIsLock()


    def SendTxtCmd(this, cmd) :
        return False

    def SendTxtCmdReadResp(this, cmd, maxRespByteSize) :
        return False

    #private methond
    def SendCtrlCmd(this, cmd) :  
        return False
    
    def ReadReg(this, regAddr, byteOffset, readCount, regValueList, regValueListStartIdx=0) :
        regValueListTemp = ted.DD_DSIM_MipiReadReg(regAddr, byteOffset, readCount)
        for idx, regValueInt in enumerate(regValueListTemp) :
            regValueList[idx + regValueListStartIdx] = regValueInt
        return True

    def ReadReg1Byte(this, regAddr, byteOffset) :
        return ted.DD_DSIM_MipiReadReg1Byte(dutIdx, regAddr, byteOffset)

    def WriteReg(this, regAddr, byteOffset, writeCount, regValueList, writeDataStartIdx=0) :

        dutIdx = 0

        regValueListTmp=[0 for _ in range(writeCount)]  #���� Register �� ������ŭ ����Ʈ �Ҵ� 
        for i in range(writeCount) :
            regValueListTmp[i] = regValueList[i+wrietDataStartIdx]
         
        ted.DD_DSIM_MipiWriteReg(dutIdx, regAddr, byteOffset, regValueListTmp)

        return True

    def WriteReg1Byte(this, regAddr, byteOffset, regValue) :
        return ted.DD_DSIM_MipiWriteReg1Byte(dutIdx, regAddr, byteOffset, regValue)

    def WriteCtrlReg(this, regAddr) :
        return this.WriteReg1Byte(regAddr, 0, 1)

    #COMM_API Bool TedDD_DSIM_MipiReadReg(int dutIdx, int addr, int byteOffset, int readCount, unsigned char* buf, int bufMaxByteSize);
    def DD_DSIM_MipiReadReg(this, dutIdx, regAddr, byteOffset, readCount) : 
        return ted.DD_DSIM_MipiReadReg(dutIdx, regAddr, byteOffset, readCount)

    #COMM_API unsigned char TedDD_DSIM_MipiReadReg1Byte(int dutIdx, int addr, int byteOffset);
    def DD_DSIM_MipiReadReg1Byte(this, dutIdx, regAddr, byteOffset) : 
        return ted.DD_DSIM_MipiReadReg1Byte(dutIdx, regAddr, byteOffset)

    #COMM_API Bool TedDD_DSIM_MipiReadReg(int dutIdx, int addr, int byteOffset, int readCount, unsigned char* buf, int bufMaxByteSize);
    def DD_DSIM_MipiWriteReg(this, dutIdx, regAddr, byteOffset, regValueList) : 
        return ted.DD_DSIM_MipiWriteReg(dutIdx, regAddr, byteOffset, regValueList)

    #COMM_API Bool TedDD_DSIM_MipiWriteReg1Byte(int dutIdx, int addr, int byteOffset, unsigned char data);
    def DD_DSIM_MipiWriteReg1Byte(this, dutIdx, regAddr, byteOffset, regValue) : 
        return ted.DD_DSIM_MipiWriteReg1Byte(dutIdx, regAddr, byteOffset, regValue)

    #WREG0=0x39, [Addr], [regVal0], [regVal1].....
    #COMM_API Bool TedDD_DSIM_MipiWriteReg39(int dutIdx, int addr, int writeCount, unsigned char* buf);
    def DD_DSIM_MipiWriteReg39(this, dutIdx, regAddr, regValueList) :
        return ted.DD_DSIM_MipiWriteReg39(dutIdx, regAddr, regValueList)

    #WREG0=0x15, [Addr], [regVal]
    #COMM_API Bool TedDD_DSIM_MipiWriteReg15(int dutIdx, int addr, unsigned char value);
    def DD_DSIM_MipiWriteReg15(this, dutIdx, regAddr, regValue) :
        return ted.DD_DSIM_MipiWriteReg15(dutIdx, regAddr, regValue)

    #WREG0=0x05, [Addr]
    #COMM_API Bool TedDD_DSIM_MipiWriteReg05(int dutIdx, int addr);
    def DD_DSIM_MipiWriteReg05(this, dutIdx, regAddr) :
        return ted.DD_DSIM_MipiWriteReg05(dutIdx, regAddr)

    #WREG0=0x07, [value]   :   Compressd Mode Command
    #COMM_API Bool TedDD_DSIM_MipiWriteReg07(int dutIdx, int addr);
    def DD_DSIM_MipiWriteReg07(this, dutIdx, value) :
        return ted.DD_DSIM_MipiWriteReg07(dutIdx, value)

    def CatchPower(this, powerInfo) :

        ret = TDeviceCatchPowerInfo(this.__DeviceHandle,  this.__PowerStructData, 1000)

        result= struct.unpack(this.__PowerStructFmt, this.__PowerStructData)

        resIdx=0
        
        powerInfo.No = result[resIdx] 
        resIdx += 1

        for i in range(10) :
            powerInfo.Avail[i] = result[i+resIdx]
        resIdx += 10

        for i in range(10) :
            powerInfo.Value1[i] = result[i+resIdx]
        resIdx += 10

        for i in range(10) :
            powerInfo.Voltage[i] = result[i+resIdx]
        resIdx += 10

        for i in range(10) :
            powerInfo.Current[i] = result[i+resIdx]
        resIdx += 10

        for i in range(10) :
            powerInfo.Range1[i] = result[i+resIdx]
        resIdx += 10

        for i in range(10) :
            powerInfo.Range2[i] = result[i+resIdx]
        resIdx += 10

        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag
    

    def PatternConnect(this) : 
        return ted.PatternConnect()

    def PatternDisconnect(this) : 
        return ted.PatternDisconnect()

    def PatternSetCommand(this, ptrnCmd) :
        return ted.PatternSetCommand(ptrnCmd)
    
    def PatternPaint(this, r, g, b, a) : 
        return ted.PatternPaint(r, g, b, a)

    def PatternUpdateScreen(this) : 
        return ted.PatternUpdateScreen()

    def PatternDrawImage(this, imgFileName) : 
        return ted.PatternDrawImage(imgFileName)

    def PatternScreenVerify(this, r, g, b) : 
        return ted.PatternScreenVerify(r, g, b)

    def ANA670X_GetChipIDCount(this) : 
        return ted.ANA670X_GetChipIDCount()

    def ANA670X_GetChipID(this, dutIdx) : 
        return ted.ANA670X_GetChipID(dutIdx)

    def ANA670X_GetProductRevisionBytesCount(this) : 
        return ted.ANA670X_GetProductRevisionBytesCount()

    def ANA670X_GetProductRevisionBytes(this, dutIdx) : 
        return ted.ANA670X_GetProductRevisionBytes(dutIdx)

    def ANA670X_SetFrameRate(this, dutIdx, fr) :
        return ted.ANA670X_SetFrameRate(dutIdx, fr)

    def ANA670X_GetFrameRate(this, dutIdx) : 
        return ted.ANA670X_GetFrameRate(dutIdx)

    def DebugMessage(this, msg) :
        #print(msg)
        ret = TDeviceDebugMessage(this.__DeviceHandle, TString.ConvertToCTypeStrng(msg))
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def DebugFuncEnter(this, funcName) :
        ret = TDeviceDebugFuncEnter(this.__DeviceHandle, TString.ConvertToCTypeStrng(funcName))
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def DebugFuncLeave(this, funcName) :
        ret = TDeviceDebugFuncLeave(this.__DeviceHandle, TString.ConvertToCTypeStrng(funcName))
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def DD_FB_blank(this, dutIdx, value) :
        return ted.DD_FB_blank(dutIdx, value)

    #COMM_API Bool TedDD_DSIM_manual_ctrl(int dutIdx, int value);
    def DD_DSIM_manual_ctrl(this, dutIdx, value) :
        return ted.DD_DSIM_manual_ctrl(dutIdx, value)

    #COMM_API Bool TedDD_DSIM_power_ctrl(int dutIdx, int value);
    def DD_DSIM_power_ctrl(this, dutIdx, value) :
        return ted.DD_DSIM_power_ctrl(dutIdx, value)

    #COMM_API Bool TedDD_DSIM_source_cal(int dutIdx, int value);
    def DD_DSIM_source_cal(this, dutIdx, value) :
        return ted.DD_DSIM_source_cal(dutIdx, value)

    def DD_DSIM_sleepin(this, dutIdx, value) : 
        return ted.DD_DSIM_sleepin(dutIdx, value)
    
    def DD_DSIM_sleepout(this, dutIdx, value) : 
        return ted.DD_DSIM_sleepout(dutIdx, value)
    
    def DD_DSIM_deep_standby(this, dutIdx, value) : 
        return ted.DD_DSIM_deep_standby(dutIdx, value)
    
    def DD_DSIM_displayon(this, dutIdx, value) : 
        return ted.DD_DSIM_displayon(dutIdx, value)
    
    def DD_DSIM_reset_ctrl(this, dutIdx, value) : 
        return ted.DD_DSIM_reset_ctrl(dutIdx, value)


    #//VLIN1_ADC
    #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetSamples(TDEVICE_HDL hdl, int value);  
    def Vlin1AdcSetSamples(this, dutIdx, value) :
        return ted.vlin1_adc_set_samples(dutIdx, value)

    #DEVICE_API TED_BOOL TDeviceVlin1AdcSetInterval(TDEVICE_HDL hdl, int value); 
    def Vlin1AdcSetInterval(this, dutIdx, value) :
        return ted.vlin1_adc_set_interval(dutIdx, value)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetChannelOn(TDEVICE_HDL hdl, int chIdx);
    def Vlin1AdcSetChannelOn(this, dutIdx, value) :
        return ted.vlin1_adc_set_channel_on(dutIdx, value)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetChannelOff(TDEVICE_HDL hdl, int chIdx); 
    def Vlin1AdcSetChannelOff(this, dutIdx, value) :
        return ted.vlin1_adc_set_channel_off(dutIdx, value)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetMode(TDEVICE_HDL hdl, int value);  
    def Vlin1AdcSetMode(this, dutIdx, value) :
        return ted.vlin1_adc_set_mode(dutIdx, value)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetVoltage(TDEVICE_HDL hdl, int chIdx);  
    def Vlin1AdcGetVoltage(this, dutIdx, chIdx) :
        return ted.vlin1_adc_get_voltage(dutIdx, chIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetVoltageVLIN1(TDEVICE_HDL hdl);  
    def Vlin1AdcGetVoltageVLIN1(this, dutIdx) :
        return ted.vlin1_adc_get_voltage_VLIN1(dutIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetVoltageVBAT(TDEVICE_HDL hdl);  
    def Vlin1AdcGetVoltageVBAT(this, dutIdx) :
        return ted.vlin1_adc_get_voltage_VBAT(dutIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetVoltageELVDD(TDEVICE_HDL hdl);  
    def Vlin1AdcGetVoltageELVDD(this, dutIdx) :
        return ted.vlin1_adc_get_voltage_ELVDD(dutIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetCurrent(TDEVICE_HDL hdl, int chIdx);  
    def Vlin1AdcGetCurrent(this, dutIdx, chIdx) :
        return ted.vlin1_adc_get_current(dutIdx, chIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetCurrentVLIN1(TDEVICE_HDL hdl); 
    def Vlin1AdcGetCurrentVLIN1(this, dutIdx) :
        return ted.vlin1_adc_get_current_VLIN1(dutIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetCurrentVBAT(TDEVICE_HDL hdl); 
    def Vlin1AdcGetCurrentVBAT(this, dutIdx) :
        return ted.vlin1_adc_get_current_VBAT(dutIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetCurrentELVDD(TDEVICE_HDL hdl); 
    def Vlin1AdcGetCurrentELVDD(this, dutIdx) :
        return ted.vlin1_adc_get_current_ELVDD(dutIdx)

    #//VCI_ADC
    #TDEVICE_API TED_BOOL TDeviceVciAdcSetSamples(TDEVICE_HDL hdl, int value); 
    def VciAdcSetSamples(this, dutIdx, value) :
        return ted.vci_adc_set_samples(dutIdx, value)

    #TDEVICE_API TED_BOOL TDeviceVciAdcSetInterval(TDEVICE_HDL hdl, int value);
    def VciAdcSetInterval(this, dutIdx, value) :
        return ted.vci_adc_set_interval(dutIdx, value)

    #TDEVICE_API TED_BOOL TDeviceVciAdcSetChannelOn(TDEVICE_HDL hdl, int chIdx);
    def VciAdcSetChannelOn(this, dutIdx, value) :
        return ted.vci_adc_set_channel_on(dutIdx, value)

    #TDEVICE_API TED_BOOL TDeviceVciAdcSetChannelOff(TDEVICE_HDL hdl, int chIdx);
    def VciAdcSetChannelOff(this, dutIdx, value) :
        return ted.vci_adc_set_channel_off(dutIdx, value)

    #TDEVICE_API TED_BOOL TDeviceVciAdcSetMode(TDEVICE_HDL hdl, int value);
    def VciAdcSetMode(this, dutIdx, value) :
        return ted.vci_adc_set_mode(dutIdx, value)

    #TDEVICE_API int TDeviceVciAdcGetVoltage(TDEVICE_HDL hdl, int chIdx);
    def VciAdcGetVoltage(this, dutIdx, chIdx) :
        return ted.vci_adc_get_voltage(dutIdx, chIdx)

    #TDEVICE_API int TDeviceVciAdcGetVoltageVCI(TDEVICE_HDL hdl);
    def VciAdcGetVoltageVCI(this, dutIdx) :
        return ted.vci_adc_get_voltage_VCI(dutIdx)

    #TDEVICE_API int TDeviceVciAdcGetVoltageVDDR(TDEVICE_HDL hdl);
    def VciAdcGetVoltageVDDR(this, dutIdx) :
        return ted.vci_adc_get_voltage_VDDR(dutIdx)

    #TDEVICE_API int TDeviceVciAdcGetVoltageVDDI(TDEVICE_HDL hdl);
    def VciAdcGetVoltageVDDI(this, dutIdx) :
        return ted.vci_adc_get_voltage_VDDI(dutIdx)

    #TDEVICE_API int TDeviceVciAdcGetCurrent(TDEVICE_HDL hdl, int chIdx);
    def VciAdcGetCurrent(this, dutIdx, chIdx) :
        return ted.vci_adc_get_current(dutIdx, chIdx)

    #DEVICE_API int TDeviceVciAdcGetCurrentVCI(TDEVICE_HDL hdl);
    def VciAdcGetCurrentVCI(this, dutIdx) :
        return ted.vci_adc_get_current_VCI(dutIdx)

    #TDEVICE_API int TDeviceVciAdcGetCurrentVDDR(TDEVICE_HDL hdl);
    def VciAdcGetCurrentVDDR(this, dutIdx) :
        return ted.vci_adc_get_current_VDDR(dutIdx)

    #TDEVICE_API int TDeviceVciAdcGetCurrentVDDI(TDEVICE_HDL hdl);
    def VciAdcGetCurrentVDDI(this, dutIdx) :
        return ted.vci_adc_get_current_VDDI(dutIdx)

    #//SDOUT ADC
    #define TED_SDOUTADC_MAX_CH_COUNT 16
    #TDEVICE_API int TDeviceSoutAdcSetDevConfig(TDEVICE_HDL hdl, int value);
    def SoutAdcSetDevConfig(this, dutIdx, value) :
        return ted.sout_adc_set_devconfig(dutIdx, value)

    #TDEVICE_API int TDeviceSoutAdcSetInConfig(TDEVICE_HDL hdl, int chIdx,  int value); 
    def SoutAdcSetInConfig(this, dutIdx, chIdx, value) :
        return ted.sout_adc_set_inconfig(dutIdx, chIdx, value)

    #COMM_API Bool TedAdcSoutSetRBSel(int dutIdx, int value)
    def AdcSoutSetRBSel(this, dutIdx, value) :
        return ted.AdcSoutSetRBSel(dutIdx, value)

    #COMM_API int TedAdcSoutGetRBSel(int dutIdx)
    def AdcSoutGetRBSel(this, dutIdx) :
        return ted.AdcSoutGetRBSel(dutIdx)

    def SoutAdcGetChannelCount(this, dutIdx) :
        return ted.sout_adc_get_channel_count(dutIdx)

    #TDEVICE_API int TDeviceSoutAdcGetVoltage(TDEVICE_HDL hdl, int chIdx);  
    def SoutAdcGetVoltage(this, dutIdx, chIdx) :
        return ted.sout_adc_get_voltage(dutIdx, chIdx)

    #TDEVICE_API TED_BOOL TDeviceSoutAdcGetAllVoltage(TDEVICE_HDL hdl, int* voltageArray);
    def SoutAdcGetAllVoltage(this, dutIdx) :
        return ted.sout_adc_get_all_voltage(dutIdx)

    #TDEVICE_API TED_BOOL TDeviceLdoAdcSetInConfig(TDEVICE_HDL hdl, int chIdx, int value);
    def LdoAdcSetInConfig(this, dutIdx, chIdx, value) :
        return  ted.ldo_adc_set_inconfig(dutIdx, chIdx, value)

    def LdoAdcGetChannelCount(this, dutIdx) :
        return ted.ldo_adc_get_channel_count(dutIdx)

    #TDEVICE_API int TDeviceLdoAdcGetVoltage(TDEVICE_HDL hdl, int chIdx);
    def LdoAdcGetVoltage(this, dutIdx, chIdx) :
        return  ted.ldo_adc_get_voltage(dutIdx, chIdx)

    #TDEVICE_API TED_BOOL TDeviceLdoAdcGetAllVoltage(TDEVICE_HDL hdl, int* voltageArray);
    def LdoAdcGetAllVoltage(this, dutIdx) :
        return ted.ldo_adc_get_all_voltage(dutIdx)

    #TDEVICE_API TED_BOOL TDeviceRegAdcSetInConfig(TDEVICE_HDL hdl, int chIdx, int value);
    def RegAdcSetInConfig(this, dutIdx, chIdx, value) :
        return ted.reg_adc_set_inconfig(dutIdx, chIdx, value)

    def RegAdcGetChannelCount(this, dutIdx) :
        return ted.reg_adc_get_channel_count(dutIdx)

    #TDEVICE_API int TDeviceRegAdcGetVoltage(TDEVICE_HDL hdl, int chIdx);
    def RegAdcGetVoltage(this, dutIdx, chIdx) :
        return ted.reg_adc_get_voltage(dutIdx, chIdx)

    #TDEVICE_API TED_BOOL TDeviceLdoAdcGetAllVoltage(TDEVICE_HDL hdl, int* voltageArray);
    def RegAdcGetAllVoltage(this, dutIdx) :
        return ted.reg_adc_get_all_voltage(dutIdx)

    #COMM_API Bool TedAgingSetCurJobInfo(int dutIdx, int jobID, int status, int scIdx, int scCount, const char* desc);
    def AgingSetCurJobInfo(this, dutIdx, jobID, status, scIdx, scCount, desc) :
        return ted.AgingSetCurJobInfo(dutIdx, jobID, status, scIdx, scCount, desc)

    #TDEVICE_API TED_BOOL TDeviceAgingSetCurScInfo(TDEVICE_HDL hdl, int scID, int status, int tcIdx, int tcCount);
    def AgingSetCurScInfo(this, dutIdx, scID, status, tcIdx, tcCount, desc) :
        return ted.AgingSetCurScInfo(dutIdx, scID, status, tcIdx, tcCount, desc)

    #TDEVICE_API TED_BOOL TDeviceAgingSetCurTcInfo(TDEVICE_HDL hdl, int tcID, int status, int tcStepIdx, int tcStepCount);
    def AgingSetCurTcInfo(this, dutIdx, tcID, status, tcStepIdx, tcStepCount, desc) :
        return ted.AgingSetCurTcInfo(dutIdx, tcID, status, tcStepIdx, tcStepCount, desc)

    #TDEVICE_API TED_BOOL TDeviceAgingSetCurTcStepInfo(TDEVICE_HDL hdl, int tcStepID, int status);
    def AgingSetCurTcStepInfo(this, dutIdx, tcStepID, status, desc) :
        return ted.AgingSetCurTcStepInfo(dutIdx, tcStepID, status, desc)

    #COMM_API Bool TedAgingMeasureADC(int dutIdx, /*OUT*/void* res);
    def AgingMeasureADC(this, dutIdx) :
        return ted.AgingMeasureADC(dutIdx)

    #COMM_API int TedAgingMeasureADCResultStructureByteSize();
    def AgingMeasureADCResultStructureByteSize(this) : 
        return ted.AgingMeasureADCResultStructureByteSize()


#
# class TFileTransfer
#
class TFileTransfer :

    class Type(enum.IntEnum) : 
        T5 = 0
        
    class ErrorType(enum.IntEnum) : 
        Success = 0,
        SendPacket=1,
        NoResp=2,
        FileOpen=3,
        StorageSize=4,
        CRC=5
    
    #TDEVICE_API TFILETRANSFER_HDL TFileTransferCreate(enum TFileTransferType type, TDEVICE_HDL deviceHandle);
    def __init__(this, type, device) :
        this.__TFileTransferHandle = TFileTransferCreate(type, device.Handle)
        this.__FileName = ""

    def __getattr__(this, attrName) :
        if attrName == 'LastErrorString' : 
            return this.GetLastErrorString()
        if attrName == 'FileName' : 
            return this.__FileName
        else :
            raise AttributeError(attrName)


    #TDEVICE_API TED_BOOL TFileTransferDestroy(TFILETRANSFER_HDL fileTransferHandle);

    #TDEVICE_API TED_BOOL TFileTransferStart(TFILETRANSFER_HDL fileTransferHandle, const char* fileName);
    def Start(this, fileName) : 
        this.__FileName = fileName
        bytesString = fileName.encode('euc-kr')
        #bytesString = fileName.encode('ascii')
        #bytesString = fileName.encode('utf-8')
        ret = TFileTransferStart(this.__TFileTransferHandle, bytesString)
        return ret

    #TDEVICE_API TED_BOOL TFileTransferStop(TFILETRANSFER_HDL fileTransferHandle);
    def Stop(this) : 
        ret = TFileTransferStop(this.__TFileTransferHandle)
        return ret

    #TDEVICE_API int TFileTransferGetFileByteSize(TFILETRANSFER_HDL fileTransferHandle);
    def GetFileByteSize(this) : 
        ret = TFileTransferGetFileByteSize(this.__TFileTransferHandle)
        return ret

    #TDEVICE_API int TFileTransferGetTransferByteSize(TFILETRANSFER_HDL fileTransferHandle);
    def GetTransferByteSize(this) : 
        ret = TFileTransferGetTransferByteSize(this.__TFileTransferHandle)
        return ret

    #TDEVICE_API TED_BOOL TFileTransferIsStart(TFILETRANSFER_HDL fileTransferHandle);
    def IsStart(this) : 
        ret = TFileTransferIsStart(this.__TFileTransferHandle)
        return ret

    #TDEVICE_API TED_BOOL TFileTransferIsDone(TFILETRANSFER_HDL fileTransferHandle);
    def IsDone(this) : 
        ret = TFileTransferIsDone(this.__TFileTransferHandle)
        return ret

    #TDEVICE_API TED_BOOL TFileTransferIsError(TFILETRANSFER_HDL fileTransferHandle);
    def IsError(this) : 
        ret = TFileTransferIsError(this.__TFileTransferHandle)
        return ret

    #TDEVICE_API enum TFileTransferError TFileTransferGetLastError(TFILETRANSFER_HDL fileTransferHandle);
    def GetLastError(this) : 
        ret = TFileTransferGetLastError(this.__TFileTransferHandle)
        return ret

    def GetLastErrorString(this) :
        err = this.GetLastError()
        if err == TFileTransfer.ErrorType.Success :
            return "Success"
        elif err == TFileTransfer.ErrorType.SendPacket :
            return "SendPacket Error"
        elif err == TFileTransfer.ErrorType.NoResp :
            return "NoResp Error"
        elif err == TFileTransfer.ErrorType.FileOpen :
            return "FileOpen Error"
        elif err == TFileTransfer.ErrorType.StorageSize :
            return "StorageSize Error"
        elif err == TFileTransfer.ErrorType.CRC :
            return "CRC Error"
        else :
            return "Unknown Error"
    
    