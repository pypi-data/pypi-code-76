

from Anapass.TModule import *
from Anapass import Aging
import inspect

def TEDMode_HLPM_30Hz_ON(device, dutIdx, isDelay=True) :
    
    print()
    print("[TEDMode_HLPM_30Hz_ON] Enter ")

    HZ = 30
    frameRate = device.ANA670X_GetFrameRate(dutIdx)
    if frameRate != HZ :

        #VEH, VAINT 측정을 위하여 PWR_MODE 설정을 1로 변경 필요,  6A72h → 0x48로 설정 변경
        device.WREG0_15(dutIdx, 0xB0, 0x72) 
        device.WREG0_15(dutIdx, 0x6A, 0x48)  
    
        while True :
            device.ANA670X_SetFrameRate(dutIdx, HZ) #device.WREG0_15(dutIdx, 0x53, 0x24)  #HLPM ON
            frameRate = device.ANA670X_GetFrameRate(dutIdx)
            print("[TEDMode_HLPM_30Hz_ON] CurHz=%d" % frameRate)
            if frameRate == HZ :
                break

        print("[TEDMode_HLPM_30Hz_ON] Leave Hz=%d" % frameRate)
    else :
        print("[TEDMode_HLPM_30Hz_ON] Skip Hz=%d" % frameRate)

    print()
    

def TEDMode_HS1_120Hz(device, dutIdx) :
    
    print()
    print("[TEDMode_HS1_120Hz] Enter ")

    HZ = 120
    frameRate = device.ANA670X_GetFrameRate(dutIdx)
    if frameRate != HZ :

        #Normal모드에서 VBOT값 흔들림 방지를 위해 6A72h → 0x40로 설정 변경
        device.WREG0_15(dutIdx, 0xB0, 0x72) 
        device.WREG0_15(dutIdx, 0x6A, 0x40)  

        while True : 
            #TEDMode_HLPM_30Hz_OFF(device, dutIdx, False)
            device.ANA670X_SetFrameRate(dutIdx, HZ) 
            #device.WREG0_15(dutIdx, 0xB0, 0x01)  #echo "0x15 0xB0 0x01" > /sys/devices/platform/12870000.dsim/mipi2_rw
            #device.WREG0_15(dutIdx, 0x60, 0x00)  #echo "0x39 0x60 0x00" > /sys/devices/platform/12870000.dsim/mipi2_rw
            #device.WREG0_15(dutIdx, 0xF7, 0x07)  #Update
                                             #echo "0x15 0xB0 0x00" > /sys/devices/platform/12870000.dsim/mipi2_rw
                                             #echo "0x39 0xF7 0x07" > /sys/devices/platform/12870000.dsim/mipi2_rw
                                             # Check Mode
                                             # cat /sys/devices/platform/12860000.decon_f/tetime
                                             #    TE_TIME: 8278895
            
            frameRate = device.ANA670X_GetFrameRate(dutIdx)
            print("[TEDMode_HS1_120Hz] Cur Hz=%d" % frameRate)
            if frameRate == HZ :
                break;

        print("[TEDMode_HS1_120Hz] Setting Leave Hz=%d" % frameRate)

    else :
        print("[TEDMode_HS1_120Hz] Setting Skip Hz=%d" % frameRate)

    print()


def TEDMode_Normal_60Hz(device, dutIdx) :
    
    print()
    #print("[TEDMode_Normal_60Hz] Enter TEDMode_Delay=%d" % TEDMode_Delay)
    print("[TEDMode_Normal_60Hz] Enter ")

    HZ = 50
    frameRate = device.ANA670X_GetFrameRate(dutIdx)
    if frameRate != 60 :
        #Normal모드에서 VBOT값 흔들림 방지를 위해 6A72h → 0x40로 설정 변경
        device.WREG0_15(dutIdx, 0xB0, 0x72) 
        device.WREG0_15(dutIdx, 0x6A, 0x40)  

        while True : 
            device.ANA670X_SetFrameRate(dutIdx, 60) 
            frameRate = device.ANA670X_GetFrameRate(dutIdx)
            print("[TEDMode_Normal_60Hz] Cur Hz=%d" % frameRate)
            if frameRate == 60 :
                break
        print("[TEDMode_Normal_60Hz] Leave Hz=%d" % frameRate)
    else :
        print("[TEDMode_Normal_60Hz] Skip Hz=%d" % frameRate)
    print()


def TCBegin(device, dutIdx) :

    if platform.system()=="Windows" : 
        delayTick=0
    else :
        delayTick=2000

    #Blank On/Off
    device.DD_FB_blank(dutIdx, 1)         #echo 1 > /sys/class/graphics/fb0/blank;
    device.SysDelay(delayTick)
    device.DD_FB_blank(dutIdx, 0)         #echo 0 > /sys/class/graphics/fb0/blank;
    device.SysDelay(delayTick)
        
    # Blank Off 시 , 120Hz, source cal 하므로 설정할 필요없다. 
    #120Hz
    #TEDMode_HS1_120Hz(device, dutIdx)

    #Source Cal
    #device.DD_DSIM_source_cal(dutIdx, 1) #echo 1 > /sys/devices/platform/12870000.dsim/source_cal

    #Write Black
    device.PatternConnect()
    device.PatternPaint(0, 0, 0, 0);
    device.PatternUpdateScreen()
    device.SysDelay(500)

    # Screen Verify
    device.PatternScreenVerify(0, 0, 0)


def TCEnd(device, dutIdx) :

    if platform.system()=="Windows" : 
        delayTick=0
    else :
        delayTick=2000

    #Write Black
    device.PatternDisconnect()
    
    #120Hz  # Blank Off 시 , 120Hz, source cal 하므로 설정할 필요없다. 
    #TEDMode_HS1_120Hz(device, dutIdx)

    #Blank On/Off
    device.DD_FB_blank(dutIdx, 1)         #echo 1 > /sys/class/graphics/fb0/blank;
    device.SysDelay(delayTick)
    device.DD_FB_blank(dutIdx, 0)         #echo 0 > /sys/class/graphics/fb0/blank;
    device.SysDelay(delayTick)
        
    
def VEH_BML_Setting(device, dutIdx) :
    #VEH, BML 측정을 위하여 PWR_MODE 설정을 1로 변경 필요,  6A72h → 0x48로 설정 변경
    device.WREG0_15(dutIdx, 0xB0, 0x72) 
    device.WREG0_15(dutIdx, 0x6A, 0x48)  
    
    #VGLL, VGHH, VAINT, VEH, BML 측정을 위한 LDO Enable, F43Dh, F43Eh → 0x00으로 설정 변경
    device.WREG0_15(dutIdx, 0xB0, 0x3D) 
    device.WREG0_15(dutIdx, 0xF4, 0x00)  

    device.WREG0_15(dutIdx, 0xB0, 0x3E) 
    device.WREG0_15(dutIdx, 0xF4, 0x00)  
