
import enum
import struct

class Vlin1 :

    class Type(enum.IntEnum) :
        VLIN1=0
        VBAT=1
        ELVDD=2

    def __init__(this) : 
        this.ChannelCount=3
        this.Voltage=[-1 for _ in range(this.ChannelCount)]
        this.Current=[-1 for _ in range(this.ChannelCount)]

class Vci :
    class Type(enum.IntEnum) :
        VCI=0
        VDDR=1
        VDDI=2
    def __init__(this) : 
        this.ChannelCount=3
        this.Voltage=[-1 for _ in range(this.ChannelCount)]
        this.Current=[-1 for _ in range(this.ChannelCount)]

class Sdout :
    def __init__(this, channelCount) : 
        this.Voltage=[-1 for _ in range(channelCount)]

class Ldo :
    def __init__(this, channelCount) : 
        this.Voltage=[-1 for _ in range(channelCount)]

class Reg :
    def __init__(this, channelCount) : 
        this.Voltage=[-1 for _ in range(channelCount)]

class Measure :
    def __init__(this, soutChannelCount, ldoChannelCount, regChannelCount): 
        
        if soutChannelCount < 0 :  soutChannelCount = 0
        if ldoChannelCount < 0 :  ldoChannelCount = 0
        if regChannelCount < 0 :  regChannelCount = 0

        this.__SoutChannelCount = soutChannelCount
        this.__LdoChannelCount = ldoChannelCount
        this.__RegChannelCount = regChannelCount
        
        this.vlin1 = Vlin1()
        this.vci = Vci()
        this.sdout = Sdout(this.__SoutChannelCount)
        this.ldo = Ldo(this.__LdoChannelCount)
        this.reg = Reg(this.__RegChannelCount)
        
    
    def GetStructData(this) :
        this.__StructFmt = 'iiiiiiii'    #   Vlin1Adc voltage/current
        this.__StructFmt += 'iiiiiiii'    #   VciAdc voltage/current
        for i in range(16) :   this.__StructFmt += 'i'    # Sdout
        for i in range(16) :   this.__StructFmt += 'i'    # Ldo
        for i in range(16) :   this.__StructFmt += 'i'    # Reg
        this.__StructMeasureData = struct.pack(this.__StructFmt, 
                           0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           )

        return this.__StructMeasureData

    def ParseStructData(this) :
 
        resMea= struct.unpack(this.__StructFmt, this.__StructMeasureData)

        resIdx = 0
        
        #Vlin1Adc
        for i in range(3) :  this.vlin1.Voltage[i] = resMea[resIdx+i]  #Vlin1 Voltage
        resIdx+=4
        for i in range(3) :  this.vlin1.Current[i] = resMea[resIdx+i]  #Vlin1 Current
        resIdx+=4
        
        #VciADC
        for i in range(3) :  this.vci.Voltage[i] = resMea[resIdx+i]  #Vlin1 Voltage
        resIdx+=4
        for i in range(3) :  this.vci.Current[i] = resMea[resIdx+i]  #Vlin1 Current
        resIdx+=4
        
        #Sdout
        for i in range(this.__SoutChannelCount) :  this.sdout.Voltage[i] = resMea[resIdx+i]  
        resIdx+=16

        #Ldo
        for i in range(this.__LdoChannelCount) :  this.ldo.Voltage[i] = resMea[resIdx+i]  
        resIdx+=16

        #Reg
        for i in range(this.__RegChannelCount) :  this.reg.Voltage[i] = resMea[resIdx+i]  
        resIdx+=16

    def ParseListData(this, resList) :
 
        resIdx = 0


        
        #Vlin1Adc
        for i in range(3) :  this.vlin1.Voltage[i] = resList[resIdx+i]  #Vlin1 Voltage
        resIdx+=4
        for i in range(3) :  this.vlin1.Current[i] = resList[resIdx+i]  #Vlin1 Current
        resIdx+=4
        
        #VciADC
        for i in range(3) :  this.vci.Voltage[i] = resList[resIdx+i]  #Vlin1 Voltage
        resIdx+=4
        for i in range(3) :  this.vci.Current[i] = resList[resIdx+i]  #Vlin1 Current
        resIdx+=4
        
        #Sdout
        for i in range(this.__SoutChannelCount) :  this.sdout.Voltage[i] = resList[resIdx+i]  
        resIdx+=16

        #Ldo
        for i in range(this.__LdoChannelCount) :  this.ldo.Voltage[i] = resList[resIdx+i]  
        resIdx+=16

        #Reg
        for i in range(this.__RegChannelCount) :  this.reg.Voltage[i] = resList[resIdx+i]  
        resIdx+=16


    def Print(this) :        
        print("Vlin1Adc Voltage : ")
        print("\tVLINT1 : %d" % this.vlin1.Voltage[Vlin1.Type.VLIN1])
        print("\tVBAT   : %d" % this.vlin1.Voltage[Vlin1.Type.VBAT])
        print("\tELVDD  : %d" % this.vlin1.Voltage[Vlin1.Type.ELVDD])

        print("Vlin1Adc Current : ")
        print("\tVLINT1 : %d" % this.vlin1.Current[Vlin1.Type.VLIN1])
        print("\tVBAT   : %d" % this.vlin1.Current[Vlin1.Type.VBAT])
        print("\tELVDD  : %d" % this.vlin1.Current[Vlin1.Type.ELVDD])

        print("VciAdc Voltage : ")
        print("\tVCI  : %d" % this.vci.Voltage[Vci.Type.VCI])
        print("\tVDDR : %d" % this.vci.Voltage[Vci.Type.VDDR])
        print("\tVDDI : %d" % this.vci.Voltage[Vci.Type.VDDI])

        print("VciAdc Current : ")
        print("\tVCI  : %d" % this.vci.Current[Vci.Type.VCI])
        print("\tVDDR : %d" % this.vci.Current[Vci.Type.VDDR])
        print("\tVDDI : %d" % this.vci.Current[Vci.Type.VDDI])

        print("SdoutAdc Voltage : ", this.sdout.Voltage)
        print("ldoAdc Voltage : ", this.ldo.Voltage)
        print("RegAdc Voltage : ", this.reg.Voltage)
