import sys
import platform
from ctypes import *
from ctypes.wintypes import *

class Api :

    def __init__(this) :
        #print(platform.architecture())
        is64bit = sys.maxsize > 2**32
        if is64bit :
            dllName="AnapassTModule.dll"
        else :
            dllName="AnapassTModule32.dll"

        try:
            #print("Load DLL from CurrentFolder " + "(./" + dllName + ")")
            Load_DLL = WinDLL('../TEDPython/' + dllName)
        except OSError as err:
            #print("OS error: {0}".format(err))
            #print("Load DLL from PackageFolder " + "(" + dllName + ")")
            Load_DLL = WinDLL(dllName)
    
        #TDEVICE_API TED_RESULT TSys_WinInit();
        this.TSys_WinInit = Load_DLL['TSys_WinInit']
        this.TSys_WinInit.restype=c_int;

        #TDEVICE_API TDEVICE_HDL TDeviceCreate(const TED_CHAR* fileName);
        this.TDeviceCreate=Load_DLL['TDeviceCreate']
        this.TDeviceCreate.restype=c_void_p
        this.TDeviceCreate.argtypes=[c_int]

        #TDEVICE_API TED_RESULT TDeviceDestroy(TDEVICE_HDL hdl);
        this.TDeviceDestroy=Load_DLL['TDeviceDestroy']
        this.TDeviceDestroy.restype=c_int;
        this.TDeviceDestroy.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TDeviceSetServerIPAddr(TDEVICE_HDL hdl, const char* serverIPAddr); 
        this.TDeviceSysSetServerIPAddr = Load_DLL['TDeviceSysSetServerIPAddr']
        this.TDeviceSysSetServerIPAddr.restype=c_int;
        this.TDeviceSysSetServerIPAddr.argtypes=[c_void_p, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceSetBoardID(TDEVICE_HDL hdl, int boardID); 
        this.TDeviceSysSetBoardID = Load_DLL['TDeviceSysSetBoardID']
        this.TDeviceSysSetBoardID.restype=c_int;
        this.TDeviceSysSetBoardID.argtypes=[c_void_p, c_int]

        #TDEVICE_API TED_BOOL TDeviceSysSetTcLocalSave(void* hdl, int boardID, int bFlag);
        this.TDeviceSysSetTcLocalSave = Load_DLL['TDeviceSysSetTcLocalSave']
        this.TDeviceSysSetTcLocalSave.restype=c_int;
        this.TDeviceSysSetTcLocalSave.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceSysDelay(TDEVICE_HDL hdl, int delay /*unit : milesec*/);
        this.TDeviceSysDelay = Load_DLL['TDeviceSysDelay']
        this.TDeviceSysDelay.restype=c_int;
        this.TDeviceSysDelay.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceSysGetDutCount(void* hdl);
        this.TDeviceSysGetDutCount = Load_DLL['TDeviceSysGetDutCount']
        this.TDeviceSysGetDutCount.restype=c_int;
        this.TDeviceSysGetDutCount.argtypes=[c_void_p]

        #TDEVICE_API int TDeviceSysGetDutIndexAllDeviceValue(void* hdl);
        this.TDeviceSysGetDutIndexAllDeviceValue = Load_DLL['TDeviceSysGetDutIndexAllDeviceValue']
        this.TDeviceSysGetDutIndexAllDeviceValue.restype=c_int;
        this.TDeviceSysGetDutIndexAllDeviceValue.argtypes=[c_void_p]

        #TDEVICE_API long long TDeviceSysGetCurUtcTime(void* hdl);
        this.TDeviceSysGetCurUtcTime = Load_DLL['TDeviceSysGetCurUtcTime']
        this.TDeviceSysGetCurUtcTime.restype=c_int;
        this.TDeviceSysGetCurUtcTime.argtypes=[c_void_p]

        #TDEVICE_API long long TDeviceSysGetTickCount64(void* hdl);
        this.TDeviceSysGetTickCount64 = Load_DLL['TDeviceSysGetTickCount64']
        this.TDeviceSysGetTickCount64.restype=c_int;
        this.TDeviceSysGetTickCount64.argtypes=[c_void_p]

        #TDEVICE_API long long TDeviceSysGetUtcTimeKST(void* hdl, int year, int month, int day, int hour, int min, int sec);
        this.TDeviceSysGetUtcTimeKST = Load_DLL['TDeviceSysGetUtcTimeKST']
        this.TDeviceSysGetUtcTimeKST.restype=c_int;
        this.TDeviceSysGetUtcTimeKST.argtypes=[c_void_p, c_int, c_int, c_int, c_int, c_int, c_int]

        #TDEVICE_API long long TDeviceSysGetErrFlag(void* hdl);
        this.TDeviceSysGetErrFlag = Load_DLL['TDeviceSysGetErrFlag']
        this.TDeviceSysGetErrFlag.restype=c_int;
        this.TDeviceSysGetErrFlag.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TDeviceSysMipiLock(void* hdl);
        this.TDeviceSysMipiLock = Load_DLL['TDeviceSysMipiLock']
        this.TDeviceSysMipiLock.restype=c_int;
        this.TDeviceSysMipiLock.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TDeviceSysMipiUnlock(void* hdl);
        this.TDeviceSysMipiUnlock = Load_DLL['TDeviceSysMipiUnlock']
        this.TDeviceSysMipiUnlock.restype=c_int;
        this.TDeviceSysMipiUnlock.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TDeviceSysMipiIsLock(void* hdl);
        this.TDeviceSysMipiIsLock = Load_DLL['TDeviceSysMipiIsLock']
        this.TDeviceSysMipiIsLock.restype=c_int;
        this.TDeviceSysMipiIsLock.argtypes=[c_void_p]

                
        #TDEVICE_API TED_RESULT TDeviceConnect(TDEVICE_HDL hdl); 
        this.TDeviceConnect = Load_DLL['TDeviceConnect']
        this.TDeviceConnect.restype=c_int;
        this.TDeviceConnect.argtypes=[c_void_p]

        #TDEVICE_API TED_RESULT TDeviceDisconnect(TDEVICE_HDL hdl);
        this.TDeviceDisconnect = Load_DLL['TDeviceDisconnect']
        this.TDeviceDisconnect.restype=c_int;
        this.TDeviceDisconnect.argtypes=[c_void_p]

        #TDEVICE_API TED_RESULT TDeviceIsConnect(TDEVICE_HDL hdl);
        this.TDeviceIsConnect = Load_DLL['TDeviceIsConnect']
        this.TDeviceIsConnect.restype=c_int;
        this.TDeviceIsConnect.argtypes=[c_void_p]

        #TDEVICE_API TED_RESULT TDeviceSendTxtCmd(TDEVICE_HDL hdl, const TED_CHAR* cmd,  /*OUT*/ TED_CHAR* resp, TED_INT respMaxSize, TED_INT respDurMileSecond);
        this.TDeviceSendTxtCmd = Load_DLL['TDeviceSendTxtCmd']
        this.TDeviceSendTxtCmd.restype=c_int;
        this.TDeviceSendTxtCmd.argtypes=[c_void_p, c_char_p, c_char_p, c_int, c_int]

        #TDEVICE_API TED_RESULT TDeviceSendCtrlCmd(TDEVICE_HDL hdl, const TED_CHAR* cmd,  /*OUT*/ TED_CHAR* resp, TED_INT respMaxSize, TED_INT respDurMileSecond);
        this.TDeviceSendCtrlCmd = Load_DLL['TDeviceSendCtrlCmd']
        this.TDeviceSendCtrlCmd.restype=c_int;
        this.TDeviceSendCtrlCmd.argtypes=[c_void_p, c_char_p, c_char_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_MipiReadReg(void* hdl, int dutIdx, int addr, int byteOffset, int readCount, unsigned char* buf, int bufMaxByteSize);
        this.TDeviceDD_DSIM_MipiReadReg = Load_DLL['TDeviceDD_DSIM_MipiReadReg']
        this.TDeviceDD_DSIM_MipiReadReg.restype=c_int;
        this.TDeviceDD_DSIM_MipiReadReg.argtypes=[c_void_p, c_int, c_int, c_int, c_int, c_char_p, c_int]

        #TDEVICE_API unsigned char TDeviceDD_DSIM_MipiReadReg1Byte(void* hdl, int dutIdx, int addr, int byteOffset);
        this.TDeviceDD_DSIM_MipiReadReg1Byte = Load_DLL['TDeviceDD_DSIM_MipiReadReg1Byte']
        this.TDeviceDD_DSIM_MipiReadReg1Byte.restype=c_int;
        this.TDeviceDD_DSIM_MipiReadReg1Byte.argtypes=[c_void_p, c_int, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_MipiWriteReg(void* hdl, int dutIdx, int addr, int byteOffset, int writeCount, const unsigned char* buf);
        this.TDeviceDD_DSIM_MipiWriteReg = Load_DLL['TDeviceDD_DSIM_MipiWriteReg']
        this.TDeviceDD_DSIM_MipiWriteReg.restype=c_int;
        this.TDeviceDD_DSIM_MipiWriteReg.argtypes=[c_void_p, c_int, c_int, c_int, c_int, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_MipiWriteReg1Byte(void* hdl, int dutIdx, int addr, int byteOffset, unsigned char data);
        this.TDeviceDD_DSIM_MipiWriteReg1Byte = Load_DLL['TDeviceDD_DSIM_MipiWriteReg1Byte']
        this.TDeviceDD_DSIM_MipiWriteReg1Byte.restype=c_int;
        this.TDeviceDD_DSIM_MipiWriteReg1Byte.argtypes=[c_void_p, c_int, c_int, c_int, c_char]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_MipiWriteReg39(void* hdl, int dutIdx, int addr, int writeCount, const unsigned char* buf);
        this.TDeviceDD_DSIM_MipiWriteReg39 = Load_DLL['TDeviceDD_DSIM_MipiWriteReg39']
        this.TDeviceDD_DSIM_MipiWriteReg39.restype=c_int;
        this.TDeviceDD_DSIM_MipiWriteReg39.argtypes=[c_void_p, c_int, c_int, c_int, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_MipiWriteReg15(void* hdl, int dutIdx, int addr, unsigned char value);
        this.TDeviceDD_DSIM_MipiWriteReg15 = Load_DLL['TDeviceDD_DSIM_MipiWriteReg15']
        this.TDeviceDD_DSIM_MipiWriteReg15.restype=c_int;
        this.TDeviceDD_DSIM_MipiWriteReg15.argtypes=[c_void_p, c_int, c_int, c_char]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_MipiWriteReg05(void* hdl, int dutIdx, int addr);
        this.TDeviceDD_DSIM_MipiWriteReg05 = Load_DLL['TDeviceDD_DSIM_MipiWriteReg05']
        this.TDeviceDD_DSIM_MipiWriteReg05.restype=c_int;
        this.TDeviceDD_DSIM_MipiWriteReg05.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_MipiWriteReg07(void* hdl, int dutIdx, int addr);
        this.TDeviceDD_DSIM_MipiWriteReg07 = Load_DLL['TDeviceDD_DSIM_MipiWriteReg07']
        this.TDeviceDD_DSIM_MipiWriteReg07.restype=c_int;
        this.TDeviceDD_DSIM_MipiWriteReg07.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_RESULT TDeviceCatchPowerInfo(TDEVICE_HDL hdl, /*OUT*/struct TED_POWER_INFO* p_pwrinfo, TED_INT timeOut /*milisec */)
        this.TDeviceCatchPowerInfo = Load_DLL['TDeviceCatchPowerInfo']
        this.TDeviceCatchPowerInfo.restype=c_int;
        this.TDeviceCatchPowerInfo.argtypes=[c_void_p, c_char_p, c_int]

        #TDEVICE_API TED_BOOL TDeviceDebugMessage(TDEVICE_HDL hdl, const char* msg);
        this.TDeviceDebugMessage = Load_DLL['TDeviceDebugMessage']
        this.TDeviceDebugMessage.restype=c_int;
        this.TDeviceDebugMessage.argtypes=[c_void_p, c_char_p]

        
        #TDEVICE_API TED_BOOL TDevicePatternConnect(void* hdl);
        this.TDevicePatternConnect = Load_DLL['TDevicePatternConnect']
        this.TDevicePatternConnect.restype=c_int;
        this.TDevicePatternConnect.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TDevicePatternIsConnect(void* hdl);
        this.TDevicePatternIsConnect = Load_DLL['TDevicePatternIsConnect']
        this.TDevicePatternIsConnect.restype=c_int;
        this.TDevicePatternIsConnect.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TDevicePatternDisconnect(void* hdl);
        this.TDevicePatternDisconnect = Load_DLL['TDevicePatternDisconnect']
        this.TDevicePatternDisconnect.restype=c_int;
        this.TDevicePatternDisconnect.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TDevicePatternPaint(void* hdl, unsigned char r, unsigned char g, unsigned char b, unsigned char a);
        this.TDevicePatternPaint = Load_DLL['TDevicePatternPaint']
        this.TDevicePatternPaint.restype=c_int;
        this.TDevicePatternPaint.argtypes=[c_void_p, c_int, c_int, c_int, c_int]
                
        #TDEVICE_API TED_BOOL TDevicePatternUpdateScreen(void* hdl);
        this.TDevicePatternUpdateScreen = Load_DLL['TDevicePatternUpdateScreen']
        this.TDevicePatternUpdateScreen.restype=c_int;
        this.TDevicePatternUpdateScreen.argtypes=[c_void_p]
        
        #TDEVICE_API TED_BOOL TDevicePatternSetCommand(void* hdl, const char* cmd);
        this.TDevicePatternSetCommand = Load_DLL['TDevicePatternSetCommand']
        this.TDevicePatternSetCommand.restype=c_int;
        this.TDevicePatternSetCommand.argtypes=[c_void_p, c_char_p]

        #TDEVICE_API TED_BOOL TDevicePatternDrawImage(void* hdl, const char* imgFileName);
        this.TDevicePatternDrawImage = Load_DLL['TDevicePatternDrawImage']
        this.TDevicePatternDrawImage.restype=c_int;
        this.TDevicePatternDrawImage.argtypes=[c_void_p, c_char_p]

        #TDEVICE_API TED_BOOL TDevicePatternScreenVerify(void* hdl, unsigned char r, unsigned char g, unsigned char b);
        this.TDevicePatternScreenVerify = Load_DLL['TDevicePatternScreenVerify']
        this.TDevicePatternScreenVerify.restype=c_int;
        this.TDevicePatternScreenVerify.argtypes=[c_void_p, c_int, c_int, c_int]


        #TDEVICE_API TED_BOOL TDeviceDebugFuncEnter(TDEVICE_HDL hdl, const char* funcName);
        this.TDeviceDebugFuncEnter = Load_DLL['TDeviceDebugFuncEnter']
        this.TDeviceDebugFuncEnter.restype=c_int;
        this.TDeviceDebugFuncEnter.argtypes=[c_void_p, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceDebugFuncLeave(TDEVICE_HDL hdl, const char* funcName);
        this.TDeviceDebugFuncLeave = Load_DLL['TDeviceDebugFuncLeave']
        this.TDeviceDebugFuncLeave.restype=c_int;
        this.TDeviceDebugFuncLeave.argtypes=[c_void_p, c_char_p]


        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_manual_ctrl(void* hdl, int dutIdx, int value);
        this.TDeviceDD_DSIM_manual_ctrl = Load_DLL['TDeviceDD_DSIM_manual_ctrl']
        this.TDeviceDD_DSIM_manual_ctrl.restype=c_int;
        this.TDeviceDD_DSIM_manual_ctrl.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_power_ctrl(void* hdl, int dutIdx, int value);
        this.TDeviceDD_DSIM_power_ctrl = Load_DLL['TDeviceDD_DSIM_power_ctrl']
        this.TDeviceDD_DSIM_power_ctrl.restype=c_int;
        this.TDeviceDD_DSIM_power_ctrl.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_source_cal(void* hdl, int dutIdx, int value);
        this.TDeviceDD_DSIM_source_cal = Load_DLL['TDeviceDD_DSIM_source_cal']
        this.TDeviceDD_DSIM_source_cal.restype=c_int;
        this.TDeviceDD_DSIM_source_cal.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_sleepin(void* hdl, int dutIdx, int value);
        this.TDeviceDD_DSIM_sleepin = Load_DLL['TDeviceDD_DSIM_sleepin']
        this.TDeviceDD_DSIM_sleepin.restype=c_int;
        this.TDeviceDD_DSIM_sleepin.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_sleepout(void* hdl, int dutIdx, int value);
        this.TDeviceDD_DSIM_sleepout = Load_DLL['TDeviceDD_DSIM_sleepout']
        this.TDeviceDD_DSIM_sleepout.restype=c_int;
        this.TDeviceDD_DSIM_sleepout.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_deep_standby(void* hdl, int dutIdx, int value);
        this.TDeviceDD_DSIM_deep_standby = Load_DLL['TDeviceDD_DSIM_deep_standby']
        this.TDeviceDD_DSIM_deep_standby.restype=c_int;
        this.TDeviceDD_DSIM_deep_standby.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_displayon(void* hdl, int dutIdx, int value);
        this.TDeviceDD_DSIM_displayon = Load_DLL['TDeviceDD_DSIM_displayon']
        this.TDeviceDD_DSIM_displayon.restype=c_int;
        this.TDeviceDD_DSIM_displayon.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceDD_DSIM_reset_ctrl(void* hdl, int dutIdx, int value);
        this.TDeviceDD_DSIM_reset_ctrl = Load_DLL['TDeviceDD_DSIM_reset_ctrl']
        this.TDeviceDD_DSIM_reset_ctrl.restype=c_int;
        this.TDeviceDD_DSIM_reset_ctrl.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceDD_FB_blank(void* hdl, int dutIdx, int value);
        this.TDeviceDD_FB_blank = Load_DLL['TDeviceDD_FB_blank']
        this.TDeviceDD_FB_blank.restype=c_int;
        this.TDeviceDD_FB_blank.argtypes=[c_void_p, c_int, c_int]


        #TDEVICE_API int TDeviceAdcGetInvalidValue(void* hdl);
        this.TDeviceAdcGetInvalidValue = Load_DLL['TDeviceAdcGetInvalidValue']
        this.TDeviceAdcGetInvalidValue.restype=c_int;
        this.TDeviceAdcGetInvalidValue.argtypes=[c_void_p]

        this.TDeviceAdcGetInvalidFloat = Load_DLL['TDeviceAdcGetInvalidFloat']
        this.TDeviceAdcGetInvalidFloat.restype=c_float;
        this.TDeviceAdcGetInvalidFloat.argtypes=[c_void_p]

        #TDEVICE_API int TDeviceAdcGetGroupCount(void* hdl, int dutIdx);
        this.TDeviceAdcGetGroupCount = Load_DLL['TDeviceAdcGetGroupCount']
        this.TDeviceAdcGetGroupCount.restype=c_int;
        this.TDeviceAdcGetGroupCount.argtypes=[c_void_p, c_int]

        #TDEVICE_API TED_BOOL TDeviceAdcGetGroupName(void* hdl, int dutIdx, int groupIdx, char* szGroupName);
        this.TDeviceAdcGetGroupName = Load_DLL['TDeviceAdcGetGroupName']
        this.TDeviceAdcGetGroupName.restype=c_int;
        this.TDeviceAdcGetGroupName.argtypes=[c_void_p, c_int, c_int, c_char_p]

        #TDEVICE_API int TDeviceAdcGetGroupIndexByName(void* hdl, int dutIdx, const char* groupName);
        this.TDeviceAdcGetGroupIndexByName = Load_DLL['TDeviceAdcGetGroupIndexByName']
        this.TDeviceAdcGetGroupIndexByName.restype=c_int;
        this.TDeviceAdcGetGroupIndexByName.argtypes=[c_void_p, c_int, c_char_p]

        #TDEVICE_API int TDeviceAdcGetChannelCount(void* hdl, int dutIdx, int groupIdx);
        this.TDeviceAdcGetChannelCount = Load_DLL['TDeviceAdcGetChannelCount']
        this.TDeviceAdcGetChannelCount.restype=c_int;
        this.TDeviceAdcGetChannelCount.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceAdcGetChannelName(void* hdl, int dutIdx, int groupIdx, int chIdx, /*OUT*/ char* szChName);
        this.TDeviceAdcGetChannelName = Load_DLL['TDeviceAdcGetChannelName']
        this.TDeviceAdcGetChannelName.restype=c_int;
        this.TDeviceAdcGetChannelName.argtypes=[c_void_p, c_int, c_int, c_int, c_char_p]

        #TDEVICE_API int TDeviceAdcGetGroupIndexByPsID(void* hdl, int dutIdx, int psID);
        this.TDeviceAdcGetGroupIndexByPsID = Load_DLL['TDeviceAdcGetGroupIndexByPsID']
        this.TDeviceAdcGetGroupIndexByPsID.restype=c_int;
        this.TDeviceAdcGetGroupIndexByPsID.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API int TDeviceAdcGetChannelIndexByPsID(void* hdl, int dutIdx, int psID);
        this.TDeviceAdcGetChannelIndexByPsID = Load_DLL['TDeviceAdcGetChannelIndexByPsID']
        this.TDeviceAdcGetChannelIndexByPsID.restype=c_int;
        this.TDeviceAdcGetChannelIndexByPsID.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceAdcSetDevConfig(void* hdl, int dutIdx, int groupIdx, int value);
        this.TDeviceAdcSetDevConfig = Load_DLL['TDeviceAdcSetDevConfig']
        this.TDeviceAdcSetDevConfig.restype=c_int;
        this.TDeviceAdcSetDevConfig.argtypes=[c_void_p, c_int, c_int, c_int]

        #TDEVICE_API int TDeviceAdcGetDevConfig(void* hdl, int dutIdx, int groupIdx);
        this.TDeviceAdcGetDevConfig = Load_DLL['TDeviceAdcGetDevConfig']
        this.TDeviceAdcGetDevConfig.restype=c_int;
        this.TDeviceAdcGetDevConfig.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceAdcSetInConfig(void* hdl, int dutIdx, int groupIdx, int chIdx, int value);
        this.TDeviceAdcSetInConfig = Load_DLL['TDeviceAdcSetInConfig']
        this.TDeviceAdcSetInConfig.restype=c_int;
        this.TDeviceAdcSetInConfig.argtypes=[c_void_p, c_int, c_int, c_int, c_int]

        #TDEVICE_API int TDeviceAdcGetInConfig(void* hdl, int dutIdx, int groupIdx, int chIdx);
        this.TDeviceAdcGetInConfig = Load_DLL['TDeviceAdcGetInConfig']
        this.TDeviceAdcGetInConfig.restype=c_int;
        this.TDeviceAdcGetInConfig.argtypes=[c_void_p, c_int, c_int, c_int]

        #TDEVICE_API int TDeviceAdcGetVoltage(void* hdl, int dutIdx, int groupIdx, int chIdx);
        this.TDeviceAdcGetVoltage = Load_DLL['TDeviceAdcGetVoltage']
        this.TDeviceAdcGetVoltage.restype=c_int;
        this.TDeviceAdcGetVoltage.argtypes=[c_void_p, c_int, c_int, c_int]

        #TDEVICE_API float TDeviceAdcGetVoltFloat(void* hdl, int dutIdx, int groupIdx, int chIdx);
        this.TDeviceAdcGetVoltFloat = Load_DLL['TDeviceAdcGetVoltFloat']
        this.TDeviceAdcGetVoltFloat.restype=c_float
        this.TDeviceAdcGetVoltFloat.argtypes=[c_void_p, c_int, c_int, c_int]


        #TDEVICE_API int TDeviceAdcGetVoltageByPsID(void* hdl, int dutIdx, int psID);
        this.TDeviceAdcGetVoltageByPsID = Load_DLL['TDeviceAdcGetVoltageByPsID']
        this.TDeviceAdcGetVoltageByPsID.restype=c_int;
        this.TDeviceAdcGetVoltageByPsID.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API float TDeviceAdcGetVoltFloatByPsID(void* hdl, int dutIdx, int psID);
        this.TDeviceAdcGetVoltFloatByPsID = Load_DLL['TDeviceAdcGetVoltFloatByPsID']
        this.TDeviceAdcGetVoltFloatByPsID.restype=c_float;
        this.TDeviceAdcGetVoltFloatByPsID.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceAdcGetAllVoltage(void* hdl, int dutIdx, int groupIdx, int* valueArray);
        this.TDeviceAdcGetAllVoltage = Load_DLL['TDeviceAdcGetAllVoltage']
        this.TDeviceAdcGetAllVoltage.restype=c_int;
        this.TDeviceAdcGetAllVoltage.argtypes=[c_void_p, c_int, c_int, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceAdcGetAllVoltFloat(void* hdl, int dutIdx, int groupIdx, float* fvalueArray);
        this.TDeviceAdcGetAllVoltFloat = Load_DLL['TDeviceAdcGetAllVoltFloat']
        this.TDeviceAdcGetAllVoltFloat.restype=c_int;
        this.TDeviceAdcGetAllVoltFloat.argtypes=[c_void_p, c_int, c_int, c_char_p]


        #TDEVICE_API int TDeviceAdcGetCurrFloat(void* hdl, int dutIdx, int groupIdx, int chIdx);
        this.TDeviceAdcGetCurrFloat = Load_DLL['TDeviceAdcGetCurrFloat']
        this.TDeviceAdcGetCurrFloat.restype=c_float;
        this.TDeviceAdcGetCurrFloat.argtypes=[c_void_p, c_int, c_int, c_int]
        
        #TDEVICE_API int TDeviceAdcGetCurrent(void* hdl, int dutIdx, int groupIdx, int chIdx);
        this.TDeviceAdcGetCurrent = Load_DLL['TDeviceAdcGetCurrent']
        this.TDeviceAdcGetCurrent.restype=c_int;
        this.TDeviceAdcGetCurrent.argtypes=[c_void_p, c_int, c_int, c_int]

        #TDEVICE_API int TDeviceAdcGetCurrentByPsID(void* hdl, int dutIdx, int psID);
        this.TDeviceAdcGetCurrentByPsID = Load_DLL['TDeviceAdcGetCurrentByPsID']
        this.TDeviceAdcGetCurrentByPsID.restype=c_int;
        this.TDeviceAdcGetCurrentByPsID.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API float TDeviceAdcGetCurrFloatByPsID(void* hdl, int dutIdx, int psID);
        this.TDeviceAdcGetCurrFloatByPsID = Load_DLL['TDeviceAdcGetCurrFloatByPsID']
        this.TDeviceAdcGetCurrFloatByPsID.restype=c_float;
        this.TDeviceAdcGetCurrFloatByPsID.argtypes=[c_void_p, c_int, c_int]
    
        #TDEVICE_API TED_BOOL TDeviceAdcGetAllCurrent(void* hdl, int dutIdx, int groupIdx, int* valueArray);
        this.TDeviceAdcGetAllCurrent = Load_DLL['TDeviceAdcGetAllCurrent']
        this.TDeviceAdcGetAllCurrent.restype=c_int;
        this.TDeviceAdcGetAllCurrent.argtypes=[c_void_p, c_int, c_int, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceAdcGetAllCurrFloat(void* hdl, int dutIdx, int groupIdx, float* fvalueArray);
        this.TDeviceAdcGetAllCurrFloat = Load_DLL['TDeviceAdcGetAllCurrFloat']
        this.TDeviceAdcGetAllCurrFloat.restype=c_int;
        this.TDeviceAdcGetAllCurrFloat.argtypes=[c_void_p, c_int, c_int, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceAdcGetAllFloat(void* hdl, int dutIdx, int groupIdx, float* fVoltArray, float* fCurrArray)
        this.TDeviceAdcGetAllFloat = Load_DLL['TDeviceAdcGetAllFloat']
        this.TDeviceAdcGetAllFloat.restype=c_int;
        this.TDeviceAdcGetAllFloat.argtypes=[c_void_p, c_int, c_int, c_char_p, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceAdcSoutSetRBSel(void* hdl, int dutIdx, int value);
        this.TDeviceAdcSoutSetRBSel = Load_DLL['TDeviceAdcSoutSetRBSel']
        this.TDeviceAdcSoutSetRBSel.restype=c_int;
        this.TDeviceAdcSoutSetRBSel.argtypes=[c_void_p, c_int, c_int]
    
        #TDEVICE_API int TDeviceAdcSoutGetRBSel(void* hdl, int dutIdx);
        this.TDeviceAdcSoutGetRBSel = Load_DLL['TDeviceAdcSoutGetRBSel']
        this.TDeviceAdcSoutGetRBSel.restype=c_int;
        this.TDeviceAdcSoutGetRBSel.argtypes=[c_void_p, c_int]
    

        #//VLIN1_ADC
        #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetSamples(TDEVICE_HDL hdl, int dutIdx, int value);  
        this.TDeviceVlin1AdcSetSamples = Load_DLL['TDeviceVlin1AdcSetSamples']
        this.TDeviceVlin1AdcSetSamples.restype=c_int;
        this.TDeviceVlin1AdcSetSamples.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetInterval(TDEVICE_HDL hdl,  int dutIdx,  int value); 
        this.TDeviceVlin1AdcSetInterval = Load_DLL['TDeviceVlin1AdcSetInterval']
        this.TDeviceVlin1AdcSetInterval.restype=c_int;
        this.TDeviceVlin1AdcSetInterval.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetChannelOn(TDEVICE_HDL hdl, int dutIdx, int chIdx);
        this.TDeviceVlin1AdcSetChannelOn = Load_DLL['TDeviceVlin1AdcSetChannelOn']
        this.TDeviceVlin1AdcSetChannelOn.restype=c_int;
        this.TDeviceVlin1AdcSetChannelOn.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetChannelOff(TDEVICE_HDL hdl,  int dutIdx, int chIdx); 
        this.TDeviceVlin1AdcSetChannelOff = Load_DLL['TDeviceVlin1AdcSetChannelOff']
        this.TDeviceVlin1AdcSetChannelOff.restype=c_int;
        this.TDeviceVlin1AdcSetChannelOff.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceVlin1AdcSetMode(TDEVICE_HDL hdl,  int dutIdx, int value);  
        this.TDeviceVlin1AdcSetMode = Load_DLL['TDeviceVlin1AdcSetMode']
        this.TDeviceVlin1AdcSetMode.restype=c_int;
        this.TDeviceVlin1AdcSetMode.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API int TDeviceVlin1AdcGetVoltage(TDEVICE_HDL hdl,  int dutIdx, int chIdx);  
        this.TDeviceVlin1AdcGetVoltage = Load_DLL['TDeviceVlin1AdcGetVoltage']
        this.TDeviceVlin1AdcGetVoltage.restype=c_int;
        this.TDeviceVlin1AdcGetVoltage.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API int TDeviceVlin1AdcGetVoltageVLIN1(TDEVICE_HDL hdl, int dutIdx, );  
        this.TDeviceVlin1AdcGetVoltageVLIN1 = Load_DLL['TDeviceVlin1AdcGetVoltageVLIN1']
        this.TDeviceVlin1AdcGetVoltageVLIN1.restype=c_int;
        this.TDeviceVlin1AdcGetVoltageVLIN1.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceVlin1AdcGetVoltageVBAT(TDEVICE_HDL hdl,  int dutIdx, );  
        this.TDeviceVlin1AdcGetVoltageVBAT = Load_DLL['TDeviceVlin1AdcGetVoltageVBAT']
        this.TDeviceVlin1AdcGetVoltageVBAT.restype=c_int;
        this.TDeviceVlin1AdcGetVoltageVBAT.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceVlin1AdcGetVoltageELVDD(TDEVICE_HDL hdl,  int dutIdx, );  
        this.TDeviceVlin1AdcGetVoltageELVDD = Load_DLL['TDeviceVlin1AdcGetVoltageELVDD']
        this.TDeviceVlin1AdcGetVoltageELVDD.restype=c_int;
        this.TDeviceVlin1AdcGetVoltageELVDD.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceVlin1AdcGetCurrent(TDEVICE_HDL hdl,  int dutIdx, int chIdx);  
        this.TDeviceVlin1AdcGetCurrent = Load_DLL['TDeviceVlin1AdcGetCurrent']
        this.TDeviceVlin1AdcGetCurrent.restype=c_int;
        this.TDeviceVlin1AdcGetCurrent.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API int TDeviceVlin1AdcGetCurrentVLIN1(TDEVICE_HDL hdl,  int dutIdx, ); 
        this.TDeviceVlin1AdcGetCurrentVLIN1 = Load_DLL['TDeviceVlin1AdcGetCurrentVLIN1']
        this.TDeviceVlin1AdcGetCurrentVLIN1.restype=c_int;
        this.TDeviceVlin1AdcGetCurrentVLIN1.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceVlin1AdcGetCurrentVBAT(TDEVICE_HDL hdl,  int dutIdx, ); 
        this.TDeviceVlin1AdcGetCurrentVBAT = Load_DLL['TDeviceVlin1AdcGetCurrentVBAT']
        this.TDeviceVlin1AdcGetCurrentVBAT.restype=c_int;
        this.TDeviceVlin1AdcGetCurrentVBAT.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceVlin1AdcGetCurrentELVDD(TDEVICE_HDL hdl,  int dutIdx, ); 
        this.TDeviceVlin1AdcGetCurrentELVDD = Load_DLL['TDeviceVlin1AdcGetCurrentELVDD']
        this.TDeviceVlin1AdcGetCurrentELVDD.restype=c_int;
        this.TDeviceVlin1AdcGetCurrentELVDD.argtypes=[c_void_p, c_int]

        #//VCI_ADC
        #TDEVICE_API TED_BOOL TDeviceVciAdcSetSamples(TDEVICE_HDL hdl,  int dutIdx, int value); 
        this.TDeviceVciAdcSetSamples = Load_DLL['TDeviceVciAdcSetSamples']
        this.TDeviceVciAdcSetSamples.restype=c_int;
        this.TDeviceVciAdcSetSamples.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceVciAdcSetInterval(TDEVICE_HDL hdl,  int dutIdx, int value);
        this.TDeviceVciAdcSetInterval = Load_DLL['TDeviceVciAdcSetInterval']
        this.TDeviceVciAdcSetInterval.restype=c_int;
        this.TDeviceVciAdcSetInterval.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceVciAdcSetChannelOn(TDEVICE_HDL hdl,  int dutIdx, int chIdx);
        this.TDeviceVciAdcSetChannelOn = Load_DLL['TDeviceVciAdcSetChannelOn']
        this.TDeviceVciAdcSetChannelOn.restype=c_int;
        this.TDeviceVciAdcSetChannelOn.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceVciAdcSetChannelOff(TDEVICE_HDL hdl,  int dutIdx, int chIdx);
        this.TDeviceVciAdcSetChannelOff = Load_DLL['TDeviceVciAdcSetChannelOff']
        this.TDeviceVciAdcSetChannelOff.restype=c_int;
        this.TDeviceVciAdcSetChannelOff.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceVciAdcSetMode(TDEVICE_HDL hdl,  int dutIdx, int value);
        this.TDeviceVciAdcSetMode = Load_DLL['TDeviceVciAdcSetMode']
        this.TDeviceVciAdcSetMode.restype=c_int;
        this.TDeviceVciAdcSetMode.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API int TDeviceVciAdcGetVoltage(TDEVICE_HDL hdl,  int dutIdx, int chIdx);
        this.TDeviceVciAdcGetVoltage = Load_DLL['TDeviceVciAdcGetVoltage']
        this.TDeviceVciAdcGetVoltage.restype=c_int;
        this.TDeviceVciAdcGetVoltage.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API int TDeviceVciAdcGetVoltageVCI(TDEVICE_HDL hdl,  int dutIdx, );
        this.TDeviceVciAdcGetVoltageVCI = Load_DLL['TDeviceVciAdcGetVoltageVCI']
        this.TDeviceVciAdcGetVoltageVCI.restype=c_int;
        this.TDeviceVciAdcGetVoltageVCI.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceVciAdcGetVoltageVDDR(TDEVICE_HDL hdl,  int dutIdx, );
        this.TDeviceVciAdcGetVoltageVDDR = Load_DLL['TDeviceVciAdcGetVoltageVDDR']
        this.TDeviceVciAdcGetVoltageVDDR.restype=c_int;
        this.TDeviceVciAdcGetVoltageVDDR.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceVciAdcGetVoltageVDDI(TDEVICE_HDL hdl,  int dutIdx, );
        this.TDeviceVciAdcGetVoltageVDDI = Load_DLL['TDeviceVciAdcGetVoltageVDDI']
        this.TDeviceVciAdcGetVoltageVDDI.restype=c_int;
        this.TDeviceVciAdcGetVoltageVDDI.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceVciAdcGetCurrent(TDEVICE_HDL hdl,  int dutIdx, int chIdx);
        this.TDeviceVciAdcGetCurrent = Load_DLL['TDeviceVciAdcGetCurrent']
        this.TDeviceVciAdcGetCurrent.restype=c_int;
        this.TDeviceVciAdcGetCurrent.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API int TDeviceVciAdcGetCurrentVCI(TDEVICE_HDL hdl,  int dutIdx, );
        this.TDeviceVciAdcGetCurrentVCI = Load_DLL['TDeviceVciAdcGetCurrentVCI']
        this.TDeviceVciAdcGetCurrentVCI.restype=c_int;
        this.TDeviceVciAdcGetCurrentVCI.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceVciAdcGetCurrentVDDR(TDEVICE_HDL hdl,  int dutIdx, );
        this.TDeviceVciAdcGetCurrentVDDR = Load_DLL['TDeviceVciAdcGetCurrentVDDR']
        this.TDeviceVciAdcGetCurrentVDDR.restype=c_int;
        this.TDeviceVciAdcGetCurrentVDDR.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceVciAdcGetCurrentVDDI(TDEVICE_HDL hdl,  int dutIdx, );
        this.TDeviceVciAdcGetCurrentVDDI = Load_DLL['TDeviceVciAdcGetCurrentVDDI']
        this.TDeviceVciAdcGetCurrentVDDI.restype=c_int;
        this.TDeviceVciAdcGetCurrentVDDI.argtypes=[c_void_p, c_int]

        #//SDOUT ADC
        #define TED_SDOUTADC_MAX_CH_COUNT 16
        #TDEVICE_API int TDeviceSoutAdcSetDevConfig(TDEVICE_HDL hdl,  int dutIdx, int value);
        this.TDeviceSoutAdcSetDevConfig = Load_DLL['TDeviceSoutAdcSetDevConfig']
        this.TDeviceSoutAdcSetDevConfig.restype=c_int;
        this.TDeviceSoutAdcSetDevConfig.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API int TDeviceSoutAdcSetInConfig(TDEVICE_HDL hdl,  int dutIdx, int chIdx, int value); 
        this.TDeviceSoutAdcSetInConfig = Load_DLL['TDeviceSoutAdcSetInConfig']
        this.TDeviceSoutAdcSetInConfig.restype=c_int;
        this.TDeviceSoutAdcSetInConfig.argtypes=[c_void_p, c_int, c_int, c_int]

        #TDEVICE_API int TDeviceSoutAdcSetRBSel(TDEVICE_HDL hdl,  int dutIdx, int value);    
        this.TDeviceSoutAdcSetRBSel = Load_DLL['TDeviceSoutAdcSetRBSel']
        this.TDeviceSoutAdcSetRBSel.restype=c_int;
        this.TDeviceSoutAdcSetRBSel.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API int TDeviceSoutAdcGetChannelCount(TDEVICE_HDL hdl,  int dutIdx, );
        this.TDeviceSoutAdcGetChannelCount = Load_DLL['TDeviceSoutAdcGetChannelCount']
        this.TDeviceSoutAdcGetChannelCount.restype=c_int;
        this.TDeviceSoutAdcGetChannelCount.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceSoutAdcGetVoltage(TDEVICE_HDL hdl,  int dutIdx, int chIdx);  
        this.TDeviceSoutAdcGetVoltage = Load_DLL['TDeviceSoutAdcGetVoltage']
        this.TDeviceSoutAdcGetVoltage.restype=c_int;
        this.TDeviceSoutAdcGetVoltage.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceSoutAdcGetAllVoltage(TDEVICE_HDL hdl,  int dutIdx, int* voltageArray);
        this.TDeviceSoutAdcGetAllVoltage = Load_DLL['TDeviceSoutAdcGetAllVoltage']
        this.TDeviceSoutAdcGetAllVoltage.restype=c_int;
        this.TDeviceSoutAdcGetAllVoltage.argtypes=[c_void_p, c_int, c_char_p]
                
        #TDEVICE_API int TDeviceLdoAdcSetInConfig(TDEVICE_HDL hdl,  int dutIdx, int chIdx, int value); 
        this.TDeviceLdoAdcSetInConfig = Load_DLL['TDeviceLdoAdcSetInConfig']
        this.TDeviceLdoAdcSetInConfig.restype=c_int;
        this.TDeviceLdoAdcSetInConfig.argtypes=[c_void_p, c_int, c_int, c_int]

        #TDEVICE_API int TDeviceLdoAdcGetChannelCount(TDEVICE_HDL hdl,  int dutIdx, );
        this.TDeviceLdoAdcGetChannelCount = Load_DLL['TDeviceLdoAdcGetChannelCount']
        this.TDeviceLdoAdcGetChannelCount.restype=c_int;
        this.TDeviceLdoAdcGetChannelCount.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceLdoAdcGetVoltage(TDEVICE_HDL hdl,  int dutIdx, int chIdx);  
        this.TDeviceLdoAdcGetVoltage = Load_DLL['TDeviceLdoAdcGetVoltage']
        this.TDeviceLdoAdcGetVoltage.restype=c_int;
        this.TDeviceLdoAdcGetVoltage.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceLdoAdcGetAllVoltage(TDEVICE_HDL hdl,  int dutIdx, int* voltageArray);
        this.TDeviceLdoAdcGetAllVoltage = Load_DLL['TDeviceLdoAdcGetAllVoltage']
        this.TDeviceLdoAdcGetAllVoltage.restype=c_int;
        this.TDeviceLdoAdcGetAllVoltage.argtypes=[c_void_p, c_int, c_char_p]


        #TDEVICE_API int TDeviceRegAdcSetInConfig(TDEVICE_HDL hdl,  int dutIdx, int chIdx, int value); 
        this.TDeviceRegAdcSetInConfig = Load_DLL['TDeviceRegAdcSetInConfig']
        this.TDeviceRegAdcSetInConfig.restype=c_int;
        this.TDeviceRegAdcSetInConfig.argtypes=[c_void_p, c_int, c_int, c_int]

        #TDEVICE_API int TDeviceRegAdcGetChannelCount(TDEVICE_HDL hdl, int dutIdx);
        this.TDeviceRegAdcGetChannelCount = Load_DLL['TDeviceRegAdcGetChannelCount']
        this.TDeviceRegAdcGetChannelCount.restype=c_int;
        this.TDeviceRegAdcGetChannelCount.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceRegAdcGetVoltage(TDEVICE_HDL hdl,  int dutIdx, int chIdx);  
        this.TDeviceRegAdcGetVoltage = Load_DLL['TDeviceRegAdcGetVoltage']
        this.TDeviceRegAdcGetVoltage.restype=c_int;
        this.TDeviceRegAdcGetVoltage.argtypes=[c_void_p, c_int, c_int]

        #TDEVICE_API TED_BOOL TDeviceRegAdcGetAllVoltage(TDEVICE_HDL hdl,  int dutIdx, int* voltageArray);
        this.TDeviceRegAdcGetAllVoltage = Load_DLL['TDeviceRegAdcGetAllVoltage']
        this.TDeviceRegAdcGetAllVoltage.restype=c_int;
        this.TDeviceRegAdcGetAllVoltage.argtypes=[c_void_p, c_int, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceAgingNotifyPyStart(TDEVICE_HDL hdl); 
        this.TDeviceAgingNotifyPyStart = Load_DLL['TDeviceAgingNotifyPyStart']
        this.TDeviceAgingNotifyPyStart.restype=c_int;
        this.TDeviceAgingNotifyPyStart.argtypes=[c_void_p, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceAgingNotifyPyStop(TDEVICE_HDL hdl); 
        this.TDeviceAgingNotifyPyStop = Load_DLL['TDeviceAgingNotifyPyStop']
        this.TDeviceAgingNotifyPyStop.restype=c_int;
        this.TDeviceAgingNotifyPyStop.argtypes=[c_void_p, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceAgingSetCurJobInfo(void* hdl, int dutIdx, int jobID, int status, int scIdx, int scCount, const char* desc);
        this.TDeviceAgingSetCurJobInfo = Load_DLL['TDeviceAgingSetCurJobInfo']
        this.TDeviceAgingSetCurJobInfo.restype=c_int;
        this.TDeviceAgingSetCurJobInfo.argtypes=[c_void_p, c_int, c_int, c_int, c_int, c_int, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceAgingSetCurScInfo(void* hdl, int dutIdx, int scID, int status, int tcIdx, int tcCount, const char* desc);
        this.TDeviceAgingSetCurScInfo = Load_DLL['TDeviceAgingSetCurScInfo']
        this.TDeviceAgingSetCurScInfo.restype=c_int;
        this.TDeviceAgingSetCurScInfo.argtypes=[c_void_p, c_int, c_int, c_int, c_int, c_int, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceAgingSetCurTcInfo(void* hdl, int dutIdx, int tcID, int status, int tcStepIdx, int tcStepCount, const char* desc);
        this.TDeviceAgingSetCurTcInfo = Load_DLL['TDeviceAgingSetCurTcInfo']
        this.TDeviceAgingSetCurTcInfo.restype=c_int;
        this.TDeviceAgingSetCurTcInfo.argtypes=[c_void_p, c_int, c_int, c_int, c_int, c_int, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceAgingSetCurTcStepInfo(void* hdl, int dutIdx, int tcStepID, int status, const char* desc);
        this.TDeviceAgingSetCurTcStepInfo = Load_DLL['TDeviceAgingSetCurTcStepInfo']
        this.TDeviceAgingSetCurTcStepInfo.restype=c_int;
        this.TDeviceAgingSetCurTcStepInfo.argtypes=[c_void_p, c_int, c_int, c_int, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceAgingMeasureADC(void* hdl, int dutIdx, /*OUT*/ void* res);
        this.TDeviceAgingMeasureADC = Load_DLL['TDeviceAgingMeasureADC']
        this.TDeviceAgingMeasureADC.restype=c_int;
        this.TDeviceAgingMeasureADC.argtypes=[c_void_p, c_int, c_char_p]

        #TDEVICE_API int TDeviceAgingMeasureADCResultStructureByteSize(void* hdl);
        this.TDeviceAgingMeasureADCResultStructureByteSize = Load_DLL['TDeviceAgingMeasureADCResultStructureByteSize']
        this.TDeviceAgingMeasureADCResultStructureByteSize.restype=c_int;
        this.TDeviceAgingMeasureADCResultStructureByteSize.argtypes=[c_void_p]

        #TDEVICE_API int TDeviceANA670X_GetChipIDCount(void* hdl);
        this.TDeviceANA670X_GetChipIDCount = Load_DLL['TDeviceANA670X_GetChipIDCount']
        this.TDeviceANA670X_GetChipIDCount.restype=c_int;
        this.TDeviceANA670X_GetChipIDCount.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TDeviceANA670X_GetChipID(void* hdl, int dutIdx, /*OUT*/unsigned char* chipIDArr);
        this.TDeviceANA670X_GetChipID = Load_DLL['TDeviceANA670X_GetChipID']
        this.TDeviceANA670X_GetChipID.restype=c_int;
        this.TDeviceANA670X_GetChipID.argtypes=[c_void_p, c_int, c_char_p]

        #TDEVICE_API TED_BOOL TDeviceANA670X_SetFrameRate(void* hdl, int dutIdx, int fr);
        this.TDeviceANA670X_SetFrameRate = Load_DLL['TDeviceANA670X_SetFrameRate']
        this.TDeviceANA670X_SetFrameRate.restype=c_int;
        this.TDeviceANA670X_SetFrameRate.argtypes=[c_void_p, c_int , c_int]

        #TDEVICE_API int TDeviceANA670X_GetFrameRate(void* hdl, int dutIdx);
        this.TDeviceANA670X_GetFrameRate = Load_DLL['TDeviceANA670X_GetFrameRate']
        this.TDeviceANA670X_GetFrameRate.restype=c_int;
        this.TDeviceANA670X_GetFrameRate.argtypes=[c_void_p, c_int]

        #TDEVICE_API int TDeviceANA670X_GetProductRevisionBytesCount(void* hdl);
        this.TDeviceANA670X_GetProductRevisionBytesCount = Load_DLL['TDeviceANA670X_GetProductRevisionBytesCount']
        this.TDeviceANA670X_GetProductRevisionBytesCount.restype=c_int;
        this.TDeviceANA670X_GetProductRevisionBytesCount.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TDeviceANA670X_GetProductRevisionBytes(void* hdl, int dutIdx, /*OUT*/unsigned char* revArr);
        this.TDeviceANA670X_GetProductRevisionBytes = Load_DLL['TDeviceANA670X_GetProductRevisionBytes']
        this.TDeviceANA670X_GetProductRevisionBytes.restype=c_int;
        this.TDeviceANA670X_GetProductRevisionBytes.argtypes=[c_void_p, c_int, c_char_p]

        # enum TFileTransferType {
        #    TFileTransferTypeT5 = 0,
        #    TFileTransferTypeMaxCount
        #};

        # enum TFileTransferError {
        #    TFileTransferErrorSuccess = 0,
        #    TFileTransferErrorSendPacket,
        #    TFileTransferErrorNoResp,
        #    TFileTransferErrorFileOpen,
        #    TFileTransferErrorStorageSize,
        #    TFileTransferErrorCRC
        #};

        #TDEVICE_API TFILETRANSFER_HDL TFileTransferCreate(enum TFileTransferType type, TDEVICE_HDL deviceHandle);
        #TDEVICE_API TED_BOOL TFileTransferDestroy(TFILETRANSFER_HDL fileTransferHandle);
        #TDEVICE_API TED_BOOL TFileTransferStart(TFILETRANSFER_HDL fileTransferHandle, const char* fileName);
        #TDEVICE_API TED_BOOL TFileTransferStop(TFILETRANSFER_HDL fileTransferHandle);
        #TDEVICE_API int TFileTransferGetFileByteSize(TFILETRANSFER_HDL fileTransferHandle);
        #TDEVICE_API int TFileTransferGetTransferByteSize(TFILETRANSFER_HDL fileTransferHandle);
        #TDEVICE_API TED_BOOL TFileTransferIsStart(TFILETRANSFER_HDL fileTransferHandle);
        #TDEVICE_API TED_BOOL TFileTransferIsDone(TFILETRANSFER_HDL fileTransferHandle);
        #TDEVICE_API TED_BOOL TFileTransferIsError(TFILETRANSFER_HDL fileTransferHandle);
        #TDEVICE_API enum TFileTransferError TFileTransferGetLastError(TFILETRANSFER_HDL fileTransferHandle);

        #TDEVICE_API TFILETRANSFER_HDL TFileTransferCreate(enum TFileTransferType type, TDEVICE_HDL deviceHandle);
        this.TFileTransferCreate = Load_DLL['TFileTransferCreate']
        this.TFileTransferCreate.restype=c_void_p;
        this.TFileTransferCreate.argtypes=[c_int, c_void_p]

        #TDEVICE_API TED_BOOL TFileTransferDestroy(TFILETRANSFER_HDL fileTransferHandle);
        this.TFileTransferDestroy=Load_DLL['TFileTransferDestroy']
        this.TFileTransferDestroy.restype=c_int;
        this.TFileTransferDestroy.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TFileTransferStart(TFILETRANSFER_HDL fileTransferHandle, const char* fileName);
        this.TFileTransferStart=Load_DLL['TFileTransferStart']
        this.TFileTransferStart.restype=c_int;
        this.TFileTransferStart.argtypes=[c_void_p, c_void_p]

        #TDEVICE_API TED_BOOL TFileTransferStop(TFILETRANSFER_HDL fileTransferHandle);
        this.TFileTransferStop=Load_DLL['TFileTransferStop']
        this.TFileTransferStop.restype=c_int;
        this.TFileTransferStop.argtypes=[c_void_p]

        #TDEVICE_API int TFileTransferGetFileByteSize(TFILETRANSFER_HDL fileTransferHandle);
        this.TFileTransferGetFileByteSize=Load_DLL['TFileTransferGetFileByteSize']
        this.TFileTransferGetFileByteSize.restype=c_int;
        this.TFileTransferGetFileByteSize.argtypes=[c_void_p]

        #TDEVICE_API int TFileTransferGetTransferByteSize(TFILETRANSFER_HDL fileTransferHandle);
        this.TFileTransferGetTransferByteSize=Load_DLL['TFileTransferGetTransferByteSize']
        this.TFileTransferGetTransferByteSize.restype=c_int;
        this.TFileTransferGetTransferByteSize.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TFileTransferIsStart(TFILETRANSFER_HDL fileTransferHandle);
        this.TFileTransferIsStart=Load_DLL['TFileTransferIsStart']
        this.TFileTransferIsStart.restype=c_int;
        this.TFileTransferIsStart.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TFileTransferIsDone(TFILETRANSFER_HDL fileTransferHandle);
        this.TFileTransferIsDone=Load_DLL['TFileTransferIsDone']
        this.TFileTransferIsDone.restype=c_int;
        this.TFileTransferIsDone.argtypes=[c_void_p]

        #TDEVICE_API TED_BOOL TFileTransferIsError(TFILETRANSFER_HDL fileTransferHandle);
        this.TFileTransferIsError=Load_DLL['TFileTransferIsError']
        this.TFileTransferIsError.restype=c_int;
        this.TFileTransferIsError.argtypes=[c_void_p]

        #TDEVICE_API enum TFileTransferError TFileTransferGetLastError(TFILETRANSFER_HDL fileTransferHandle);
        this.TFileTransferGetLastError=Load_DLL['TFileTransferGetLastError']
        this.TFileTransferGetLastError.restype=c_int;
        this.TFileTransferGetLastError.argtypes=[c_void_p]

