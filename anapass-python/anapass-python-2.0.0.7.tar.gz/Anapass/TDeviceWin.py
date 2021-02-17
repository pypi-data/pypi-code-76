
from ctypes import *
from ctypes.wintypes import *
from enum import Enum
import time
import platform
import sys
import os
import pkg_resources  # part of setuptools
import enum
import struct
from abc import ABCMeta, abstractmethod
from Anapass  import TDeviceWinDLL
from Anapass.TDeviceBase  import *

#
# class TDevice
#
class TDeviceWin(TDeviceBase) :

    class ErrorString(enum.Enum) :
        GetResp="ErrorGetResp"
    
    def __init__(this, deviceTypeValue):

        TDeviceBase.__init__(this, deviceTypeValue)
        this.__Api = TDeviceWinDLL.Api()
        this.__Api.TSys_WinInit();

        #print(DisplayName +"TRY: create " + deviceType.name )
        this.__DeviceHandle = this.__Api.TDeviceCreate(deviceTypeValue)
        
        #struct TED_POWER_INFO {
        #    TED_S32 no;
        #    TED_S32 available[10];
        #    TED_S32 value1[10];
        #    TED_FLOAT fV[10];
        #    TED_FLOAT fA[10];
        #    TED_FLOAT fRange1[10];
        #    TED_FLOAT fRange2[10];dir

        #};

        this.__PowerStructFmt = 'i'    #    TED_S32 no;    
        this.__PowerStructFmt+='10i'   # TED_S32 available[10];
        this.__PowerStructFmt+='10i'   # TED_S32 value[10];
        this.__PowerStructFmt+='10f'   # TED_FLOAT fV[10];
        this.__PowerStructFmt+='10f'   # TED_FLOAT fV[10];
        this.__PowerStructFmt+='10f'   # TED_FLOAT fRange1[10];
        this.__PowerStructFmt+='10f'   # TED_FLOAT fRange2[10];
        
        # arg=list(range(61))

        this.__PowerStructData = struct.pack(this.__PowerStructFmt, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                           0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                           )

    def __del__(this):
        #print("TDevice::~TDevice")
        this.__Api.TDeviceDestroy(this.__DeviceHandle)

            
    def SysSetServerIPAddr(this, serverIPAddr) :
        ret = this.__Api.TDeviceSysSetServerIPAddr(this.__DeviceHandle, TString.ConvertToCTypeStrng(serverIPAddr))
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def SysSetBoardID(this, boardID) : 
        ret = this.__Api.TDeviceSysSetBoardID(this.__DeviceHandle, boardID)
        if ret==1 :
            bflag = True
        else :
            bflag = False
        return bflag

    def SysSetTcLocalSave(this, boardID, bFlag) : 
        ret = this.__Api.TDeviceSysSetTcLocalSave(this.__DeviceHandle, boardID, bFlag)
        if ret==1 :
            bflag = True
        else :
            bflag = False
        return bflag
        
    def Connect(this) :
        ret = this.__Api.TDeviceConnect(this.__DeviceHandle)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def Disonnect(this) :
        ret = this.__Api.TDeviceDisconnect(this.__DeviceHandle)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag
    
    def SendTxtCmd(this, cmd) :
        #print("[this.__Api.TDevice.SendTxtCmd] " + cmd)
        ret = this.__Api.TDeviceSendTxtCmd(this.__DeviceHandle, TString.ConvertToCTypeStrng(cmd), c_char_p(0), 0, 10)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def SendTxtCmdReadResp(this, cmd, maxRespByteSize) :
        respBytesArray=bytes(maxRespByteSize)
        ret = this.__Api.TDeviceSendTxtCmd(this.__DeviceHandle, TString.ConvertToCTypeStrng(cmd), respBytesArray, maxRespByteSize, 1000)
        if ret==1 :
            bflag = True
            resp = TString.ConvertCTypeStringToUnicode(respBytesArray)
        else :
            bflag = False;
            resp = this.__Api.TDevice.ErrorString.GetResp
        return resp

    #private methond
    def SendCtrlCmd(this, cmd) :  
        ret = this.__Api.TDeviceSendCtrlCmd(this.__DeviceHandle, TString.ConvertToCTypeStrng(cmd), c_char_p(0), 0, 0)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def Reset(this) :
        return this.__SendCtrlCmd('RESET')

    def Next(this) :
        return this.__SendCtrlCmd('NEXT')

    def Back(this) :
        return this.__SendCtrlCmd('BACK')

    def ReadReg(this, regAddr, byteOffset, readCount, regValueList, regValueListStartIdx=0) :
        dutIdx = 0
        regValueInt = 0
        regValueByteArray=bytes(readCount)
        ret = this.__Api.TDeviceDD_DSIM_MipiReadReg(this.__DeviceHandle, dutIdx, regAddr, byteOffset, readCount, regValueByteArray, readCount)
        if ret==1 :
            for idx, regValueByte in enumerate(regValueByteArray) :
                regValueInt = regValueByte
                regValueInt &= 0xFF
                regValueList[idx + regValueListStartIdx] = regValueInt
            bflag = True
        else :
            bflag = False;
        return bflag

    def ReadReg1Byte(this, regAddr, byteOffset) :
        dutIdx = 0
        return this.__Api.TDeviceDD_DSIM_MipiReadReg1Byte(this.__DeviceHandle, dutIdx, regAddr, byteOffset)

    def WriteReg(this, regAddr, byteOffset, writeCount, regValueList, writeDataStartIdx=0) :

        if writeDataStartIdx == 0 :
            regValueByteArray=bytes(regValueList)
        else :
            listTmp = regValueList[writeDataStartIdx:(writeDataStartIdx+writeCount)]
            regValueByteArray=bytes(listTmp)

        ret = this.__Api.TDeviceDD_DSIM_MipiWriteReg(this.__DeviceHandle, regAddr, byteOffset, writeCount, regValueByteArray)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def WriteReg1Byte(this, regAddr, byteOffset, regValue) :
        ret = this.__Api.TDeviceDD_DSIM_MipiWriteReg1Byte(this.__DeviceHandle, regAddr, byteOffset, c_char(regValue))
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def WriteCtrlReg(this, regAddr) :
        return this.WriteReg1Byte(regAddr, 0, 1)
    
    def CatchPower(this, powerInfo) :

        ret = this.__Api.TDeviceCatchPowerInfo(this.__DeviceHandle,  this.__PowerStructData, 1000)

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

    
    
    def DebugMessage(this, msg) :
        #print(msg)
        ret = this.__Api.TDeviceDebugMessage(this.__DeviceHandle, TString.ConvertToCTypeStrng(msg))
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def DebugFuncEnter(this, funcName) :
        ret = this.__Api.TDeviceDebugFuncEnter(this.__DeviceHandle, TString.ConvertToCTypeStrng(funcName))
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def DebugFuncLeave(this, funcName) :
        ret = this.__Api.TDeviceDebugFuncLeave(this.__DeviceHandle, TString.ConvertToCTypeStrng(funcName))
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag
            
    #//VLIN1_ADC
    #TDEVICE_API TED_BOOL this.__Api.TDeviceVlin1AdcSetSamples(TDEVICE_HDL hdl, int value);  
    def Vlin1AdcSetSamples(this, dutIdx, value) :
        ret = this.__Api.TDeviceVlin1AdcSetSamples(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #DEVICE_API TED_BOOL TDeviceVlin1AdcSetInterval(TDEVICE_HDL hdl, int value); 
    def Vlin1AdcSetInterval(this, dutIdx, value) :
        ret = this.__Api.TDeviceVlin1AdcSetInterval(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetChannelOn(TDEVICE_HDL hdl, int chIdx);
    def Vlin1AdcSetChannelOn(this, dutIdx, value) :
        ret = this.__Api.TDeviceVlin1AdcSetChannelOn(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetChannelOff(TDEVICE_HDL hdl, int chIdx); 
    def Vlin1AdcSetChannelOff(this, dutIdx, value) :
        ret = this.__Api.TDeviceVlin1AdcSetChannelOff(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetMode(TDEVICE_HDL hdl, int value);  
    def Vlin1AdcSetMode(this, dutIdx, value) :
        ret = this.__Api.TDeviceVlin1AdcSetMode(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetVoltage(TDEVICE_HDL hdl, int chIdx);  
    def Vlin1AdcGetVoltage(this, dutIdx, chIdx) :
        return this.__Api.TDeviceVlin1AdcGetVoltage(this.__DeviceHandle, dutIdx, chIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetVoltageVLIN1(TDEVICE_HDL hdl);  
    def Vlin1AdcGetVoltageVLIN1(this, dutIdx) :
        return this.__Api.TDeviceVlin1AdcGetVoltageVLIN1(this.__DeviceHandle, dutIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetVoltageVBAT(TDEVICE_HDL hdl);  
    def Vlin1AdcGetVoltageVBAT(this, dutIdx) :
        return this.__Api.TDeviceVlin1AdcGetVoltageVBAT(this.__DeviceHandle, dutIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetVoltageELVDD(TDEVICE_HDL hdl);  
    def Vlin1AdcGetVoltageELVDD(this, dutIdx) :
        return this.__Api.TDeviceVlin1AdcGetVoltageELVDD(this.__DeviceHandle, dutIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetCurrent(TDEVICE_HDL hdl, int chIdx);  
    def Vlin1AdcGetCurrent(this, dutIdx, chIdx) :
        return this.__Api.TDeviceVlin1AdcGetCurrent(this.__DeviceHandle, dutIdx, chIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetCurrentVLIN1(TDEVICE_HDL hdl); 
    def Vlin1AdcGetCurrentVLIN1(this, dutIdx) :
        return this.__Api.TDeviceVlin1AdcGetCurrentVLIN1(this.__DeviceHandle, dutIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetCurrentVBAT(TDEVICE_HDL hdl); 
    def Vlin1AdcGetCurrentVBAT(this, dutIdx) :
        return this.__Api.TDeviceVlin1AdcGetCurrentVBAT(this.__DeviceHandle, dutIdx)

    #TDEVICE_API TED_BOOL TDeviceVlin1AdcGetCurrentELVDD(TDEVICE_HDL hdl); 
    def Vlin1AdcGetCurrentELVDD(this, dutIdx) :
        return this.__Api.TDeviceVlin1AdcGetCurrentELVDD(this.__DeviceHandle, dutIdx)

    #//VCI_ADC
    #TDEVICE_API TED_BOOL TDeviceVciAdcSetSamples(TDEVICE_HDL hdl, int value); 
    def VciAdcSetSamples(this, dutIdx, value) :
        ret = this.__Api.TDeviceVciAdcSetSamples(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API TED_BOOL TDeviceVciAdcSetInterval(TDEVICE_HDL hdl, int value);
    def VciAdcSetInterval(this, dutIdx, value) :
        ret = this.__Api.TDeviceVciAdcSetInterval(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API TED_BOOL TDeviceVciAdcSetChannelOn(TDEVICE_HDL hdl, int chIdx);
    def VciAdcSetChannelOn(this, dutIdx, value) :
        ret = this.__Api.TDeviceVciAdcSetChannelOn(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API TED_BOOL TDeviceVciAdcSetChannelOff(TDEVICE_HDL hdl, int chIdx);
    def VciAdcSetChannelOff(this, dutIdx, value) :
        ret = this.__Api.TDeviceVciAdcSetChannelOff(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API TED_BOOL TDeviceVciAdcSetMode(TDEVICE_HDL hdl, int value);
    def VciAdcSetMode(this, dutIdx, value) :
        ret = this.__Api.TDeviceVciAdcSetMode(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API int TDeviceVciAdcGetVoltage(TDEVICE_HDL hdl, int chIdx);
    def VciAdcGetVoltage(this, dutIdx, chIdx) :
        return this.__Api.TDeviceVciAdcGetVoltage(this.__DeviceHandle, dutIdx, chIdx)

    #TDEVICE_API int TDeviceVciAdcGetVoltageVCI(TDEVICE_HDL hdl);
    def VciAdcGetVoltageVCI(this, dutIdx) :
        return this.__Api.TDeviceVciAdcGetVoltageVCI(this.__DeviceHandle, dutIdx)

    #TDEVICE_API int TDeviceVciAdcGetVoltageVDDR(TDEVICE_HDL hdl);
    def VciAdcGetVoltageVDDR(this, dutIdx) :
        return this.__Api.TDeviceVciAdcGetVoltageVDDR(this.__DeviceHandle, dutIdx)

    #TDEVICE_API int TDeviceVciAdcGetVoltageVDDI(TDEVICE_HDL hdl);
    def VciAdcGetVoltageVDDI(this, dutIdx) :
        return this.__Api.TDeviceVciAdcGetVoltageVDDI(this.__DeviceHandle, dutIdx)

    #TDEVICE_API int TDeviceVciAdcGetCurrent(TDEVICE_HDL hdl, int chIdx);
    def VciAdcGetCurrent(this, dutIdx, chIdx) :
        return this.__Api.TDeviceVciAdcGetCurrent(this.__DeviceHandle, dutIdx, chIdx)

    #DEVICE_API int TDeviceVciAdcGetCurrentVCI(TDEVICE_HDL hdl);
    def VciAdcGetCurrentVCI(this, dutIdx) :
        return this.__Api.TDeviceVciAdcGetCurrentVCI(this.__DeviceHandle, dutIdx)

    #TDEVICE_API int TDeviceVciAdcGetCurrentVDDR(TDEVICE_HDL hdl);
    def VciAdcGetCurrentVDDR(this, dutIdx) :
        return this.__Api.TDeviceVciAdcGetCurrentVDDR(this.__DeviceHandle, dutIdx)

    #TDEVICE_API int TDeviceVciAdcGetCurrentVDDI(TDEVICE_HDL hdl);
    def VciAdcGetCurrentVDDI(this, dutIdx) :
        return this.__Api.TDeviceVciAdcGetCurrentVDDI(this.__DeviceHandle, dutIdx)

    #//SDOUT ADC
    #define TED_SDOUTADC_MAX_CH_COUNT 16
    #TDEVICE_API int TDeviceSoutAdcSetDevConfig(TDEVICE_HDL hdl, int value);
    def SoutAdcSetDevConfig(this, dutIdx, value) :
        ret = this.__Api.TDeviceSoutAdcSetDevConfig(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API int TDeviceSoutAdcSetInConfig(TDEVICE_HDL hdl, int chIdx,  int value); 
    def SoutAdcSetInConfig(this, chIdx, dutIdx, value) :
        ret = this.__Api.TDeviceSoutAdcSetInConfig(this.__DeviceHandle, dutIdx, chIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #DEVICE_API int TDeviceSoutAdcSetRBSel(TDEVICE_HDL hdl, int value);    
    def SoutAdcSetRBSel(this, dutIdx, value) :
        ret = this.__Api.TDeviceSoutAdcSetRBSel(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API int TDeviceSoutAdcGetChannelCount(TDEVICE_HDL hdl);
    def SoutAdcGetChannelCount(this, dutIdx) :
        return this.__Api.TDeviceSoutAdcGetChannelCount(this.__DeviceHandle, dutIdx)

    #TDEVICE_API int TDeviceSoutAdcGetVoltage(TDEVICE_HDL hdl, int chIdx);  
    def SoutAdcGetVoltage(this, dutIdx, chIdx) :
        return this.__Api.TDeviceSoutAdcGetVoltage(this.__DeviceHandle, dutIdx, chIdx)

    #TDEVICE_API TED_BOOL TDeviceSoutAdcGetAllVoltage(TDEVICE_HDL hdl, int* voltageArray);
    def SoutAdcGetAllVoltage(this, dutIdx) :

        structFmt = 'i'    #    TED_S32 no;    
        for i in range(15) :
            structFmt += 'i'    #    TED_S32 no;    
        structData = struct.pack(structFmt, 
                           0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0,
                           )
        voltageList=[-1 for _ in range(16)]
        ret = this.__Api.TDeviceSoutAdcGetAllVoltage(this.__DeviceHandle, dutIdx, structData)
        if ret==1 :
            result= struct.unpack(structFmt, structData)
            for i in range(16) :
                voltageList[i] = result[i]
        return voltageList


    #TDEVICE_API TED_BOOL TDeviceLdoAdcSetInConfig(TDEVICE_HDL hdl, int chIdx, int value);
    def LdoAdcSetInConfig(this, dutIdx, chIdx, value) :
        ret = this.__Api.TDeviceLdoAdcSetInConfig(this.__DeviceHandle, dutIdx, chIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API int TDeviceLdoAdcGetChannelCount(TDEVICE_HDL hdl);
    def LdoAdcGetChannelCount(this, dutIdx) :
        return this.__Api.TDeviceLdoAdcGetChannelCount(this.__DeviceHandle, dutIdx)

    #TDEVICE_API int TDeviceLdoAdcGetVoltage(TDEVICE_HDL hdl, int chIdx);
    def LdoAdcGetVoltage(this, dutIdx, chIdx) :
        return this.__Api.TDeviceLdoAdcGetVoltage(this.__DeviceHandle, dutIdx, chIdx)

    #TDEVICE_API TED_BOOL TDeviceLdoAdcGetAllVoltage(TDEVICE_HDL hdl, int* voltageArray);
    def LdoAdcGetAllVoltage(this, dutIdx) :

        structFmt = 'i'    #    TED_S32 no;    
        for i in range(15) :
            structFmt += 'i'    #    TED_S32 no;    
        structData = struct.pack(structFmt, 
                           0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0,
                           )
        voltageList=[-1 for _ in range(16)]
        ret = this.__Api.TDeviceLdoAdcGetAllVoltage(this.__DeviceHandle, dutIdx, structData)
        if ret==1 :
            result= struct.unpack(structFmt, structData)
            for i in range(16) :
                voltageList[i] = result[i]
        return voltageList


    #TDEVICE_API TED_BOOL TDeviceRegAdcSetInConfig(TDEVICE_HDL hdl, int chIdx, int value);
    def RegAdcSetInConfig(this, dutIdx, chIdx, value) :
        ret = this.__Api.TDeviceRegAdcSetInConfig(this.__DeviceHandle, dutIdx, chIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API int TDeviceRegAdcGetChannelCount(TDEVICE_HDL hdl);
    def RegAdcGetChannelCount(this, dutIdx) :
        return this.__Api.TDeviceRegAdcGetChannelCount(this.__DeviceHandle, dutIdx)

    #TDEVICE_API int TDeviceRegAdcGetVoltage(TDEVICE_HDL hdl, int chIdx);
    def RegAdcGetVoltage(this, dutIdx, chIdx) :
        return this.__Api.TDeviceRegAdcGetVoltage(this.__DeviceHandle, dutIdx, chIdx)

    #TDEVICE_API TED_BOOL TDeviceLdoAdcGetAllVoltage(TDEVICE_HDL hdl, int* voltageArray);
    def RegAdcGetAllVoltage(this, dutIdx) :

        structFmt = 'i'    #    TED_S32 no;    
        for i in range(15) :
            structFmt += 'i'    #    TED_S32 no;    
        structData = struct.pack(structFmt, 
                           0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0,
                           )
        voltageList=[-1 for _ in range(16)]
        ret = this.__Api.TDeviceRegAdcGetAllVoltage(this.__DeviceHandle, dutIdx, structData)
        if ret==1 :
            result= struct.unpack(structFmt, structData)
            for i in range(16) :
                voltageList[i] = result[i]
        return voltageList

    def AgingNotifyPyStart(this, pyFileName) : 
        ret = this.__Api.TDeviceAgingNotifyPyStart(this.__DeviceHandle, TString.ConvertToCTypeStrng(pyFileName))
        if ret==1 :
            bflag = True
        else :
            bflag = False
        return bflag

    def AgingNotifyPyStop(this, pyFileName) : 
        ret = this.__Api.TDeviceAgingNotifyPyStop(this.__DeviceHandle, TString.ConvertToCTypeStrng(pyFileName))
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #TDEVICE_API TED_BOOL TDeviceAgingSetCurJobInfo(TDEVICE_HDL hdl, int jobID, int status, int scIdx, int scCount, const char* desc);
    def AgingSetCurJobInfo(this, dutIdx, jobID, status, scIdx, scCount, desc) :
        return this.__Api.TDeviceAgingSetCurJobInfo(this.__DeviceHandle, dutIdx, jobID, status,scIdx, scCount, TString.ConvertToCTypeStrng(desc))

    #TDEVICE_API TED_BOOL TDeviceAgingSetCurScInfo(TDEVICE_HDL hdl, int scID, int status, int tcIdx, int tcCount, const char* desc);
    def AgingSetCurScInfo(this, dutIdx, scID, status,tcIdx, tcCount, desc) :
        return this.__Api.TDeviceAgingSetCurScInfo(this.__DeviceHandle, dutIdx, scID, status,tcIdx, tcCount, TString.ConvertToCTypeStrng(desc))

    #TDEVICE_API TED_BOOL TDeviceAgingSetCurTcInfo(void* hdl, int dutIdx, int tcID, int status, int tcStepIdx, int tcStepCount, const char* desc);
    def AgingSetCurTcInfo(this, dutIdx, tcID, status, tcStepIdx, tcStepCount, desc) :
        return this.__Api.TDeviceAgingSetCurTcInfo(this.__DeviceHandle, dutIdx, tcID, status, tcStepIdx, tcStepCount, TString.ConvertToCTypeStrng(desc))

    #TDEVICE_API TED_BOOL TDeviceAgingSetCurTcStepInfo(TDEVICE_HDL hdl, int tcStepID, int status, const char* desc);
    def AgingSetCurTcStepInfo(this, dutIdx, tcStepID, status, desc) :
        return this.__Api.TDeviceAgingSetCurTcStepInfo(this.__DeviceHandle, dutIdx, tcStepID, status, TString.ConvertToCTypeStrng(desc))

    #TDEVICE_API  TED_BOOL TDeviceAgingMeasureADC(TDEVICE_HDL hdl, int jobID, int scID, int tcID, int tcStep,  const char* desc, /*OUT*/unsigned char* res);
    def AgingMeasureADC(this, dutIdx) : 
        #soutChannelCount = this.SoutAdcGetChannelCount()
        #ldoChannelCount = this.LdoAdcGetChannelCount()
        #regChannelCount = this.RegAdcGetChannelCount()
        #meaRes = Adc.Measure(soutChannelCount, ldoChannelCount, regChannelCount)
        ##this.__Api.TDeviceAgingMeasureADC(this.__DeviceHandle, dutIdx, meaRes.GetStructData())
        #meaRes.ParseStructData()
        #return meaRes
        this.__Api.TDeviceAgingMeasureADC(this.__DeviceHandle, dutIdx, None)
        #return True

    #COMM_API int TedAgingMeasureADCResultStructureByteSize();
    def AgingMeasureADCResultStructureByteSize(this) : 
        return this.__Api.TDeviceAgingMeasureADCResultStructureByteSize()
            
    def ANA670X_GetChipIDCount(this) : 
        return this.__Api.TDeviceANA670X_GetChipIDCount(this.__DeviceHandle)

    def ANA670X_GetChipID(this, dutIdx) : 
        chiIdCount = this.ANA670X_GetChipIDCount()
        chipIdList = [0 for _ in range(chiIdCount)]
        chipIdByteArray = bytes(chiIdCount)
        ret = this.__Api.TDeviceANA670X_GetChipID(this.__DeviceHandle, dutIdx, chipIdByteArray)
        if ret==1 :
            for idx, regValueByte in enumerate(chipIdByteArray) :
                regValueInt = regValueByte
                regValueInt &= 0xFF
                chipIdList[idx] = regValueInt
        
        return chipIdList

    def ANA670X_GetProductRevisionBytesCount(this) : 
        return this.__Api.TDeviceANA670X_GetProductRevisionBytesCount(this.__DeviceHandle)

    def ANA670X_GetProductRevisionBytes(this, dutIdx) : 
        
        revCount = this.ANA670X_GetProductRevisionBytesCount()
        revList = [0 for _ in range(revCount)]
        revByteArray = bytes(revCount)
        ret = this.__Api.TDeviceANA670X_GetProductRevisionBytes(this.__DeviceHandle, dutIdx, revByteArray)
        if ret==1 :
            for idx, regValueByte in enumerate(revByteArray) :
                regValueInt = regValueByte
                regValueInt &= 0xFF
                revList[idx] = regValueInt
        
        return revList


    def ANA670X_SetFrameRate(this, dutIdx, fr) :
        return this.__Api.TDeviceANA670X_SetFrameRate(this.__DeviceHandle, dutIdx, fr)

    def ANA670X_GetFrameRate(this, dutIdx) : 
        return this.__Api.TDeviceANA670X_GetFrameRate(this.__DeviceHandle, dutIdx)

    #COMM_API Bool TedAdcSoutSetRBSel(int dutIdx, int value)
    def AdcSoutSetRBSel(this, dutIdx, value) :
        return True #ted.AdcSoutSetRBSel(dutIdx, value)

    #COMM_API int TedAdcSoutGetRBSel(int dutIdx)
    def AdcSoutGetRBSel(this, dutIdx) :
        return 1 #ted.AdcSoutGetRBSel(dutIdx)


    #TDEVICE_API TED_BOOL TDeviceDD_DSIM_MipiReadReg(void* hdl, int dutIdx, int addr, int byteOffset, int readCount, unsigned char* buf, int bufMaxByteSize);
    def DD_DSIM_MipiReadReg(this, dutIdx, regAddr, byteOffset, readCount) : 

        regValueList=[0 for _ in range(readCount)]
        regValueByteArray=bytes(readCount)
        ret = this.__Api.TDeviceDD_DSIM_MipiReadReg(this.__DeviceHandle,  dutIdx, regAddr, byteOffset, readCount, regValueByteArray, readCount)
        if ret==1 :
            for idx, regValueByte in enumerate(regValueByteArray) :
                regValueInt = regValueByte
                regValueInt &= 0xFF
                regValueList[idx] = regValueInt
        
        return regValueList

    #TDEVICE_API unsigned char TDeviceDD_DSIM_MipiReadReg1Byte(void* hdl, int dutIdx, int addr, int byteOffset);
    def DD_DSIM_MipiReadReg1Byte(this, dutIdx, regAddr, byteOffset) : 
        return this.__Api.TDeviceDD_DSIM_MipiReadReg1Byte(this.__DeviceHandle,  dutIdx, regAddr, byteOffset)

    #TDEVICE_API TED_BOOL TDeviceDD_DSIM_MipiWriteReg(void* hdl, int dutIdx, int addr, int byteOffset, int writeCount, const unsigned char* buf);
    def DD_DSIM_MipiWriteReg(this, dutIdx, regAddr, byteOffset, regValueList) : 
        writeCount = len(regValueList)
        regValueByteArray=bytes(regValueList)
        ret = this.__Api.TDeviceDD_DSIM_MipiWriteReg(this.__DeviceHandle, dutIdx, regAddr, byteOffset, writeCount, regValueByteArray)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag


    #TDEVICE_API TED_BOOL TDeviceDD_DSIM_MipiWriteReg1Byte(void* hdl, int dutIdx, int addr, int byteOffset, unsigned char data);
    def DD_DSIM_MipiWriteReg1Byte(this, dutIdx, regAddr, byteOffset, regValue) : 
        return this.__Api.TDeviceDD_DSIM_MipiWriteReg1Byte(this.__DeviceHandle,  dutIdx, regAddr, byteOffset, regValue)
    

    #WREG0=0x39, [Addr], [regVal0], [regVal1].....
    def DD_DSIM_MipiWriteReg39(this, dutIdx, regAddr, regValueList) :
        #print("[this.__Api.TDevice.DD_DSIM_MipiWriteReg39] 0x%02x" % (regAddr))
        regValueByteArray=bytes(regValueList)
        ret = this.__Api.TDeviceDD_DSIM_MipiWriteReg39(this.__DeviceHandle, dutIdx, regAddr, len(regValueList), regValueByteArray)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #WREG0=0x15, [Addr], [regVal]
    def DD_DSIM_MipiWriteReg15(this, dutIdx, regAddr, regValue) :
        ret = this.__Api.TDeviceDD_DSIM_MipiWriteReg15(this.__DeviceHandle, dutIdx, regAddr, regValue)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #WREG0=0x05, [Addr]
    def DD_DSIM_MipiWriteReg05(this, dutIdx, regAddr) :
        ret = this.__Api.TDeviceDD_DSIM_MipiWriteReg05(this.__DeviceHandle, dutIdx, regAddr)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #WREG0=0x07, [value]   :   Compressd Mode Command
    def DD_DSIM_MipiWriteReg07(this, dutIdx, value) :
        ret = this.__Api.TDeviceDD_DSIM_MipiWriteReg07(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    
    
    def DD_DSIM_manual_ctrl(this, dutIdx, value) :
        ret = this.__Api.TDeviceDD_DSIM_manual_ctrl(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag
        

    #COMM_API Bool TedDD_DSIM_power_ctrl(int dutIdx, int value);
    def DD_DSIM_power_ctrl(this, dutIdx, value) :
        ret = this.__Api.TDeviceDD_DSIM_power_ctrl(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    #COMM_API Bool TedDD_DSIM_source_cal(int dutIdx, int value);
    def DD_DSIM_source_cal(this, dutIdx, value) :
        ret = this.__Api.TDeviceDD_DSIM_source_cal(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def DD_DSIM_sleepin(this, dutIdx, value) : 
        ret = this.__Api.TDeviceDD_DSIM_sleepin(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag
    
    def DD_DSIM_sleepout(this, dutIdx, value) : 
        ret = this.__Api.TDeviceDD_DSIM_sleepout(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag
    
    def DD_DSIM_deep_standby(this, dutIdx, value) : 
        ret = this.__Api.TDeviceDD_DSIM_deep_standby(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag
    
    def DD_DSIM_displayon(this, dutIdx, value) : 
        ret = this.__Api.TDeviceDD_DSIM_displayon(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag
    
    def DD_DSIM_reset_ctrl(this, dutIdx, value) : 
        ret = this.__Api.TDeviceDD_DSIM_reset_ctrl(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag
    
    def DD_FB_blank(this, dutIdx, value) :
        ret = this.__Api.TDeviceDD_FB_blank(this.__DeviceHandle, dutIdx, value)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def PatternConnect(this) : 
        ret = this.__Api.TDevicePatternConnect(this.__DeviceHandle)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def PatternDisconnect(this) : 
        ret = this.__Api.TDevicePatternDisconnect(this.__DeviceHandle)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def PatternIsConnect(this) : 
        ret = this.__Api.TDevicePatternIsConnect(this.__DeviceHandle)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag


    def PatternSetCommand(this, ptrnCmd) :
        ret = this.__Api.TDevicePatternSetCommand(this.__DeviceHandle, TString.ConvertToCTypeStrng(ptrnCmd))
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag
    
    def PatternPaint(this, r, g, b, a) : 
        ret = this.__Api.TDevicePatternPaint(this.__DeviceHandle, r, g, b, a)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def PatternUpdateScreen(this) : 
        ret = this.__Api.TDevicePatternUpdateScreen(this.__DeviceHandle)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def PatternDrawImage(this, imgFileName) : 
        ret = this.__Api.TDevicePatternDrawImage(this.__DeviceHandle, imgFileName)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def PatternScreenVerify(this, r, g, b) : 
        ret = this.__Api.TDevicePatternScreenVerify(this.__DeviceHandle, r, g, b)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    
    def SysGetCurUtcTime(this) : 
        return this.__Api.TDeviceSysGetCurUtcTime(this.__DeviceHandle)

    def SysDelay(this, delay) :
        ret = this.__Api.TDeviceSysDelay(this.__DeviceHandle, delay)
        if ret==1 :
            bflag = True
        else :
            bflag = False;
        return bflag

    def SysGetDutIndexAllDeviceValue(this) : 
        return this.__Api.TDeviceSysGetDutIndexAllDeviceValue(this.__DeviceHandle)

    def SysGetDutCount(this) : 
        return this.__Api.TDeviceSysGetDutCount(this.__DeviceHandle)

    def SysGetTickCount64(this) : 
        return this.__Api.TDeviceSysGetTickCount64(this.__DeviceHandle)
    
    def SysGetUtcTimeKST(this, year, month, day, hour, min, sec) : 
        return this.__Api.TDeviceSysGetUtcTimeKST(this.__DeviceHandle, year, month, day, hour, min, sec)

    def SysGetErrFlag(this) : 
        return this.__Api.TDeviceSysGetErrFlag(this.__DeviceHandle)

    def SysMipiLock(this) : 
        return this.__Api.TDeviceSysMipiLock(this.__DeviceHandle)

    def SysMipiUnlock(this) : 
        return this.__Api.TDeviceSysMipiUnlock(this.__DeviceHandle)

    def SysMipiIsLock(this) : 
        return this.__Api.TDeviceSysMipiIsLock(this.__DeviceHandle)

    #COMM_API int TedAdcGetInvalidValue();
    def AdcGetInvalidValue(this) : 
        return this.__Api.TDeviceAdcGetInvalidValue(this.__DeviceHandle)

    def AdcGetInvalidFloat(this) : 
        return this.__Api.TDeviceAdcGetInvalidFloat(this.__DeviceHandle)

    #COMM_API int TedAdcGetGroupCount(int dutIdx);
    def AdcGetGroupCount(this, dutIdx) : 
        return this.__Api.TDeviceAdcGetGroupCount(this.__DeviceHandle, dutIdx)

    #COMM_API Bool TedAdcGetGroupName(int dutIdx, int groupIdx, char* szGroupName);
    def AdcGetGroupName(this, dutIdx, grpIdx) : 
        grpNameBytes=bytes(256)
        this.__Api.TDeviceAdcGetGroupName(this.__DeviceHandle, dutIdx, grpIdx, grpNameBytes)
        return TString.CStrToPyStr(grpNameBytes)

    #COMM_API int TedAdcGetGroupIndexByName(int dutIdx, const char* groupName);
    def AdcGetGroupIndexByName(this, dutIdx, grpName) : 
        return this.__Api.TDeviceAdcGetGroupIndexByName(this.__DeviceHandle, dutIdx, TString.ConvertToCTypeStrng(grpName))

    #COMM_API int TedAdcGetChannelCount(int dutIdx, int groupIdx);
    def AdcGetChannelCount(this, dutIdx, grpIdx) : 
        return this.__Api.TDeviceAdcGetChannelCount(this.__DeviceHandle, dutIdx, grpIdx)

    #COMM_API Bool TedAdcGetChannelName(int dutIdx, int groupIdx, int chIdx, /*OUT*/ char* szChName);
    def AdcGetChannelName(this, dutIdx, grpIdx, chIdx) : 
        chNameBytes=bytes(256)
        this.__Api.TDeviceAdcGetChannelName(this.__DeviceHandle, dutIdx, grpIdx, chIdx, chNameBytes)
        return TString.CStrToPyStr(chNameBytes)

    #COMM_API int TedAdcGetGroupIndexByPsID(int dutIdx, int psID);
    def AdcGetGroupIndexByPsID(this, dutIdx, psID) : 
        return this.__Api.TDeviceAdcGetGroupIndexByPsID(this.__DeviceHandle, dutIdx, psID)

    #COMM_API int TedAdcGetChannelIndexByPsID(int dutIdx, int psID);
    def AdcGetChannelIndexByPsID(this, dutIdx, psID) : 
        return this.__Api.TDeviceAdcGetChannelIndexByPsID(this.__DeviceHandle, dutIdx, psID)

    #COMM_API Bool TedAdcSetDevConfig(int dutIdx, int groupIdx, int value);
    def AdcSetDevConfig(this, dutIdx, grpIdx, value) :
        return this.__Api.TDeviceAdcSetDevConfig(this.__DeviceHandle, dutIdx, grpIdx, value)

    #COMM_API int TedAdcGetDevConfig(int dutIdx, int groupIdx);
    def AdcGetDevConfig(this, dutIdx, grpIdx) :
        return this.__Api.TDeviceAdcGetDevConfig(this.__DeviceHandle, dutIdx, grpIdx)

    #COMM_API Bool TedAdcSetInConfig(int dutIdx, int groupIdx, int chIdx, int value);
    def AdcSetInConfig(this, dutIdx, grpIdx, value) :
        return this.__Api.TDeviceAdcSetInConfig(this.__DeviceHandle, dutIdx, grpIdx, value)

    #COMM_API int TedAdcGetInConfig(int dutIdx, int groupIdx, int chIdx);
    def AdcGetInConfig(this, dutIdx, grpIdx, chIdx) :
        return this.__Api.TDeviceAdcGetInConfig(this.__DeviceHandle, dutIdx, grpIdx, chIdx)

    #COMM_API int TedAdcGetVoltage(int dutIdx, int groupIdx, int chIdx);
    def AdcGetVoltage(this, dutIdx, grpIdx, chIdx) :
        return this.__Api.TDeviceAdcGetVoltage(this.__DeviceHandle, dutIdx, grpIdx, chIdx)

    def AdcGetVoltFloat(this, dutIdx, grpIdx, chIdx) :
        return this.__Api.TDeviceAdcGetVoltFloat(this.__DeviceHandle, dutIdx, grpIdx, chIdx)

    #COMM_API int TedAdcGetVoltageByPsID(int dutIdx, int psID);
    def AdcGetVoltageByPsID(this, dutIdx, psID) :
        return this.__Api.TDeviceAdcGetVoltageByPsID(this.__DeviceHandle, dutIdx, psID)

    #COMM_API float TedAdcGetVoltFloatByPsID(int dutIdx, int psID);
    def AdcGetVoltFloatByPsID(this, dutIdx, psID) :
        return this.__Api.TDeviceAdcGetVoltFloatByPsID(this.__DeviceHandle, dutIdx, psID)

    #COMM_API Bool TedAdcGetAllVoltage(int dutIdx, int groupIdx, int* valueArray);
    def AdcGetAllVoltage(this, dutIdx, grpIdx) :

        chCnt = this.AdcGetChannelCount(dutIdx, grpIdx)
        adcList = [0 for _ in range(chCnt)]
        
        structFmt = "%di" % chCnt
        #adcValueArrayBytes = struct.pack(structFmt, [0 for _ in range(chCnt)] )
        #adcValueArrayBytes = struct.pack(structFmt, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        adcValueArrayBytes = bytes(chCnt*4)
        
        this.__Api.TDeviceAdcGetAllVoltage(this.__DeviceHandle, dutIdx, grpIdx, adcValueArrayBytes)

        result= struct.unpack(structFmt, adcValueArrayBytes)

        for i in range(chCnt) :
            adcList[i] = result[i]

        #adcList = [0 for _ in range(chCnt)]
        #adcValueArrayBytes = bytes(chCnt*4)
        #this.__Api.TDeviceAdcGetAllVoltage(dutIdx, grpIdx, adcValueArrayBytes)
        
        #adcInt = 0
        #for idx, value in enumerate(adcValueArrayBytes) :
        #    if (idx+1) % 4 == 0 : 
        #        adcList[idx/4] = adcInt
        #    else :
        #        adcInt |= value << (8*idx)

        return adcList

    #TDEVICE_API TED_BOOL TDeviceAdcGetAllVoltFloat(void* hdl, int dutIdx, int groupIdx, float* fvalueArray);
    def AdcGetAllVoltFloat(this, dutIdx, grpIdx) : 

        chCnt = this.AdcGetChannelCount(dutIdx, grpIdx)
        adcList = [0.0 for _ in range(chCnt)]
        
        structFmt = "%df" % chCnt
        #adcValueArrayBytes = struct.pack(structFmt, [0 for _ in range(chCnt)] )
        #adcValueArrayBytes = struct.pack(structFmt, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        adcValueArrayBytes = bytes(chCnt*4)
        this.__Api.TDeviceAdcGetAllVoltFloat(this.__DeviceHandle, dutIdx, grpIdx, adcValueArrayBytes)

        result= struct.unpack(structFmt, adcValueArrayBytes)

        for i in range(chCnt) :
            adcList[i] = result[i]
        
        return adcList

    #COMM_API int TedAdcGetCurrent(int dutIdx, int groupIdx, int chIdx);
    def AdcGetCurrent(this, dutIdx, grpIdx, chIdx) :
        return this.__Api.TDeviceAdcGetCurrent(this.__DeviceHandle, dutIdx, grpIdx, chIdx)

    def AdcGetCurrFloat(this, dutIdx, grpIdx, chIdx) :
        return this.__Api.TDeviceAdcGetCurrFloat(this.__DeviceHandle, dutIdx, grpIdx, chIdx)

    #COMM_API int TedAdcGetCurrentByPsID(int dutIdx, int psID);
    def AdcGetCurrentByPsID(this, dutIdx, psID) :
        return this.__Api.TDeviceAdcGetCurrentByPsID(this.__DeviceHandle, dutIdx, psID)

    #COMM_API float TedAdcGetCurrFloatByPsID(int dutIdx, int psID);
    def AdcGetCurrFloatByPsID(this, dutIdx, psID) :
        return this.__Api.TDeviceAdcGetCurrFloatByPsID(this.__DeviceHandle, dutIdx, psID)

    #COMM_API Bool TedAdcGetAllCurrent(int dutIdx, int groupIdx, int* valueArray);
    def AdcGetAllCurrent(this, dutIdx, grpIdx) :
        
        chCnt = this.AdcGetChannelCount(dutIdx, grpIdx)
        adcValueArrayBytes = bytes(chCnt*4)
        this.__Api.TDeviceAdcGetAllCurrent(this.__DeviceHandle, dutIdx, grpIdx, adcValueArrayBytes)
        
        unPackResult= struct.unpack(("%di" % chCnt), adcValueArrayBytes)
        adcList = [0 for _ in range(chCnt)]
        for i in range(chCnt) :
            adcList[i] = unPackResult[i]

        return adcList

    #TDEVICE_API TED_BOOL TDeviceAdcGetAllCurrFloat(void* hdl, int dutIdx, int groupIdx, float* fvalueArray);
    def AdcGetAllCurrFloat(this, dutIdx, grpIdx) : 

        chCnt = this.AdcGetChannelCount(dutIdx, grpIdx)
        adcList = [0.0 for _ in range(chCnt)]
        structFmt = "%df" % chCnt
        adcValueArrayBytes = bytes(chCnt*4)
        this.__Api.TDeviceAdcGetAllCurrFloat(this.__DeviceHandle, dutIdx, grpIdx, adcValueArrayBytes)

        result= struct.unpack(structFmt, adcValueArrayBytes)

        for i in range(chCnt) :
            adcList[i] = result[i]
        
        return adcList

    #COMM_API Bool TedAdcSoutSetRBSel(int dutIdx, int value);
    def AdcSoutSetRBSel(this, dutIdx, value) :
        return this.__Api.TDeviceAdcSoutSetRBSel(this.__DeviceHandle, dutIdx, value)

    #COMM_API int TedAdcSoutGetRBSel(int dutIdx);
    def AdcSoutGetRBSel(this, dutIdx) :
        return this.__Api.TDeviceAdcSoutGetRBSel(this.__DeviceHandle, dutIdx)

    #TDEVICE_API TED_BOOL TDeviceAdcGetAllFloat(void* hdl, int dutIdx, int groupIdx, float* fVoltArray, float* fCurrArray)
    def AdcGetAllFloat(this, dutIdx, grpIdx) : 

        chCnt = this.AdcGetChannelCount(dutIdx, grpIdx)
        adcList = [0.0 for _ in range(chCnt*2)]

        structFmt = "%df" % chCnt
        adcVoltArrayBytes = bytes(chCnt*4)
        adcCurrArrayBytes = bytes(chCnt*4)
        this.__Api.TDeviceAdcGetAllFloat(this.__DeviceHandle, dutIdx, grpIdx, adcVoltArrayBytes, adcCurrArrayBytes)

        result= struct.unpack(structFmt, adcVoltArrayBytes)
        for i in range(chCnt) :
            adcList[i] = result[i]
        
        result= struct.unpack(structFmt, adcCurrArrayBytes)
        for i in range(chCnt) :
            adcList[i + chCnt] = result[i]

        return adcList

    #TDEVICE_API TFILETRANSFER_HDL TFileTransferCreate(enum TFileTransferType type, TDEVICE_HDL deviceHandle);
    def TFileTransferCreate(this, type) : 
        return this.__Api.TFileTransferCreate(type, this.__DeviceHandle)

    #TDEVICE_API TED_BOOL TFileTransferDestroy(TFILETRANSFER_HDL fileTransferHandle);
    def TFileTransferDestroy(this, fileTransferHandle) : 
        return this.__Api.TFileTransferDestroy(fileTransferHandle)
    
    #TDEVICE_API TED_BOOL TFileTransferStart(TFILETRANSFER_HDL fileTransferHandle, const char* fileName);
    def TFileTransferStart(this, fileTransferHandle, fileName) : 
        return this.__Api.TFileTransferStart(fileTransferHandle, fileName)

    #TDEVICE_API TED_BOOL TFileTransferStop(TFILETRANSFER_HDL fileTransferHandle);
    def TFileTransferStop(this, fileTransferHandle) : 
        return this.__Api.TFileTransferStop(fileTransferHandle)
    
    #TDEVICE_API int TFileTransferGetFileByteSize(TFILETRANSFER_HDL fileTransferHandle);
    def TFileTransferGetFileByteSize(this, fileTransferHandle) : 
        return this.__Api.TFileTransferGetFileByteSize(fileTransferHandle)
        
    #TDEVICE_API int TFileTransferGetTransferByteSize(TFILETRANSFER_HDL fileTransferHandle);
    def TFileTransferGetTransferByteSize(this, fileTransferHandle) : 
        return this.__Api.TFileTransferGetTransferByteSize(fileTransferHandle)

    #TDEVICE_API TED_BOOL TFileTransferIsStart(TFILETRANSFER_HDL fileTransferHandle);
    def TFileTransferIsStart(this, fileTransferHandle) : 
        return this.__Api.TFileTransferIsStart(fileTransferHandle)
    
    #TDEVICE_API TED_BOOL TFileTransferIsDone(TFILETRANSFER_HDL fileTransferHandle);
    def TFileTransferIsDone(this, fileTransferHandle) : 
        return this.__Api.TFileTransferIsDone(fileTransferHandle)

    #TDEVICE_API TED_BOOL TFileTransferIsError(TFILETRANSFER_HDL fileTransferHandle);
    def TFileTransferIsError(this, fileTransferHandle) : 
        return this.__Api.TFileTransferIsError(fileTransferHandle)
        
    #TDEVICE_API enum TFileTransferError TFileTransferGetLastError(TFILETRANSFER_HDL fileTransferHandle);
    def TFileTransferGetLastError(this, fileTransferHandle) : 
        return this.__Api.TFileTransferGetLastError(fileTransferHandle)

