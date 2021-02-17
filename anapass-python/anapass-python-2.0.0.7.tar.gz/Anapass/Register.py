import xml.etree.ElementTree as ET
import enum

########################################################################################################################
#
#  class ANA6705Reg, ANA6706Reg
#  class TRegister
#
########################################################################################################################

class ANA6705 :
    NOP=0x00
    SWRESET=0x01
    RDCMODE=0x03
    RDDIDIF=0x04
    RDNUMPE=0x05
    RDRED=0x06
    RDGREEN=0x07
    RDBLUE=0x08
    RDDPM=0x0A
    RDDMADCTL=0x0B
    RDDIM=0x0D
    RDDSM=0x0E
    RDDSDR=0x0F
    SLPIN=0x10
    SLPOUT=0x11
    NORON=0x13
    INVOFF=0x20
    INVON=0x21
    ALLPOFF=0x22
    ALLPON=0x23
    DISPOFF=0x28
    DISPON=0x29
    CASET=0x2A
    PASET=0x2B
    RAMWR=0x2C
    RAMRD=0x2E
    TEOFF=0x34
    TEON=0x35
    MADCTL=0x36
    IDMOFF=0x38
    IDMON=0x39
    RAMWRC=0x3C
    RAMRDC=0x3E
    TESCL=0x44
    RDSCL=0x45
    WRDISBV=0x51
    RDDISBV=0x52
    WRCTRLD=0x53
    RDCTRLD=0x54
    WRCABC=0x55
    RDCABC=0x56
    WRVRRCTRL=0x60
    RDVRRCTRL=0x61
    WRIP00=0x81
    RDIP00=0x82
    WRIP01=0x83
    RDIP01=0x84
    WRIP02=0x85
    RDIP02=0x86
    WRIP03=0x87
    RDIP03=0x88
    WRIP04=0x89
    RDIP04=0x8A
    WRIP07=0x8B
    RDIP07=0x8C
    WRIP08=0x8E
    RDIP08=0x8F
    WRIP17=0x90
    RDIP17=0x91
    WRCMOD=0x9D
    WRPPS=0x9E
    PASSWD0=0x9F
    RDDDBS=0xA1
    RDPPSS=0xA2
    RDDDBC=0xA8
    RDPPSC=0xA9
    RDFCS=0xAA
    RDCCS=0xAF
    RDID1=0xDA
    RDID2=0xDB
    RDID3=0xDC
    G_PARA=0xB0
    IP00CTL=0xB1
    IP01CTL=0xB2
    IP02CTL=0xB3
    IP03CTL=0xB4
    IP04CTL=0xB5
    IP05CTL=0xB6
    IP06CTL_0=0xB7
    IP06CTL_1=0xB8
    IP06CTL_2=0xB9
    IP06CTL_3=0xBA
    IP06CTL_4=0xBB
    IP06CTL_5=0xBC
    IP07CTL=0xBD
    IP08CTL_0=0xBE
    IP08CTL_1=0xBF
    IP08CTL_2=0xC0
    IP08CTL_3=0xC1
    IP08CTL_4=0xC2
    IP09CTL=0xC3
    IP10CTL=0xC4
    IP11CTL_0=0xC5
    IP11CTL_1=0xC6
    IP11CTL_2=0xC7
    IP12CTL=0xC8
    IP13CTL=0xC9
    IP14CTL=0xCA
    IP15CTL=0xCB
    IP16CTL=0xCC
    IP17CTL=0xCD
    IP18CTL_0=0xCE
    IP18CTL_1=0xCF
    IP19CTL=0xD0
    IPTOPCTL=0xD1
    GPOCTL=0xD2
    OTPCTRL=0xD3
    OTPCHECK=0xD4
    MCDCTL=0xD5
    CHIP_ID=0xD6
    TECTRL=0xD7
    NVMRD=0xD8
    DSTB=0xD9
    MPSCTL=0xDD
    SPICTL=0xDE
    SPIDATA=0xDF
    PCDCTL=0xE0
    RPCDCTL=0xE1
    SCALER=0xE2
    MIPI_LANE_SEL=0xE3
    LFDCTL=0xE4
    MIPI0=0xE5
    IP22CTL=0xE6
    CCDCTL=0xE7
    IP26CTL=0xE8
    IP27CTL=0xE9
    MIPI5=0xEA
    IP28CTL=0xEB
    LABA=0xEC
    ESDFG=0xED
    ESDERR=0xEE
    DBIST=0xEF
    PASSWD1=0xF0
    PASSWD2=0xF1
    DISPCTL=0xF2
    MANPWRSEQ=0xF3
    PWRCTL=0xF4
    T2MCTL=0xF5
    SRCCTL=0xF6
    PANELUPDATE=0xF7
    ANAIPCTL=0xF8
    MIPICTL=0xF9
    RDOPTREV=0xFA
    MISCCTL=0xFB
    PASSWD3=0xFC
    IP29CTL=0xFD
    IP33CTL=0xFE

class ANA6706 :
    NOP=0x00
    SWRESET=0x01
    RDCMODE=0x03
    RDDIDIF=0x04
    RDNUMPE=0x05
    RDRED_DSC=0x06
    RDGREEN_DSC=0x07
    RDBLUE_DSC=0x08
    RDDPM=0x0A
    RDDMADCTL=0x0B
    RDDIM=0x0D
    RDDSM=0x0E
    RDDSDR=0x0F
    SLPIN=0x10
    SLPOUT=0x11
    PTLON=0x12
    NORON=0x13
    INVOFF=0x20
    INVON=0x21
    ALLPOFF=0x22
    ALLPON=0x23
    DISPOFF=0x28
    DISPON=0x29
    CASET=0x2A
    PASET=0x2B
    RAMWR=0x2C
    RAMRD=0x2E
    PTLAR=0x30
    TEOFF=0x34
    TEON=0x35
    MADCTL=0x36
    IDMOFF=0x38
    IDMON=0x39
    RAMWRC=0x3C
    RAMRDC=0x3E
    TESCL=0x44
    RDSCL=0x45
    WRDISBV=0x51
    RDDISBV=0x52
    WRCTRLD=0x53
    RDCTRLD=0x54
    WRCABC=0x55
    RDCABC=0x56
    WRVRRCTRL=0x60
    RDVRRCTRL=0x61
    WRIP00=0x82
    RDIP00=0x83
    WRIP01=0x84
    RDIP01=0x85
    WRIP02=0x86
    RDIP02=0x87
    WRIP03=0x88
    RDIP03=0x89
    WRIP04=0x8A
    RDIP04=0x8B
    WRIP07=0x8C
    RDIP07=0x8D
    WRIP08=0x8E
    RDIP08=0x8F
    WRCMOD=0x9D
    WRPPS=0x9E
    PASSWD0=0x9F
    RDDDBS=0xA1
    RDPPSS=0xA2
    WRIP37=0xA4
    RDIP37=0xA5
    HAP_W=0xA6
    HAP_R=0xA7
    RDDDBC=0xA8
    RDPPSC=0xA9
    RDFCS=0xAA
    RDCCS=0xAF
    RDID1=0xDA
    RDID2=0xDB
    RDID3=0xDC
    G_PARA=0xB0
    IP00=0xB8
    IP01=0xBC
    IP02=0xBE
    IP03_IP04=0xC2
    R=0x90
    BCCTL=0xB1
    OLEDREAD=0xB2
    HBMCTL=0xB3
    ACLCTL=0xB4
    MPSCTL=0xB5
    RMPSCTL=0xB6
    HLPMCTL=0xBB
    GAMCTL1=0xC7
    GAMCTL2=0xC8
    GAMCTL3=0xC9
    GAMCTL4=0xCA
    GAMMODE1=0xCA
    IP07_IP09=0x91
    IP08A=0xC3
    IP08B=0xC4
    IP08C=0xC5
    IP08D=0xC6
    IP08E=0xCE
    IP08F=0xCF
    IP10_IP12=0x92
    IP11A=0x93
    IP11B=0x94
    IP11C=0x95
    IP11D=0xA0
    IP11E=0xA3
    IP11F=0xAB
    IP11G=0xAC
    IP11F=0xAB
    IP11H=0xAD
    IP13A=0x6D
    IP13B=0x6F
    IP14=0x96
    IP15A=0x97
    IP15B=0x98
    IP15C=0x9C
    IP16=0x99
    IP18A=0x9A
    IP18B=0x9B
    IP19=0x63
    IP20_IP29=0xD2
    IP22=0xD3
    IP23=0xD4
    IP25=0x64
    IP27=0x65
    IP33_37=0xD5
    IP36A=0xD7
    IP36B=0xE0
    IP36C=0xE2
    IP36D=0xE4
    IP36E=0xE7
    IP36F=0xE8
    IP36G=0xEA
    IPTOP=0x6A
    GPO_A=0xCB
    GPO_B=0xB7
    TECTRL=0xB9
    LFDCTL=0xBD
    DBIST=0xBF
    SPICTL=0xC0
    SPIDATA=0xC1
    PCD_CCDCTL=0xCC
    MCDCTL=0xCD
    OTPCTRL=0xD0
    OTPCHECK=0xD1
    CHIP_ID=0xD6
    NVMRD=0xD8
    DSTB=0xD9
    MIPI0=0xE5
    MIPICTL=0xE6
    MIPI5=0xE9
    ESDFG=0xED
    ESDERR=0xEE
    PWRSEQ=0xEF
    PASSWD1=0xF0
    PASSWD2=0xF1
    DISPCTL=0xF2
    PWRCTL=0xF4
    T2MCTL=0xF5
    SRCCTL=0xF6
    PANELUPDATE=0xF7
    ANAIPCTL=0xF8
    FAILSAFE=0xF9
    RDOPTREV=0xFA
    MISCCTL=0xFB


class Xml :

    class NodeName(enum.Enum) :
        Register="Register"
        Property="Property"
  
    def __init__(this, chipType):
        if chipType == TChip.Type.ANA6705 :
            tree=ET.parse("ANA6705_Register.xml")
        elif chipType == TChip.Type.ANA6706 :
            tree=ET.parse("ANA6706_Register.xml")
        else :
            raise ValueError("[TRegister::TRegister] Not Suported ChipType,  Check TChip.Type")
        this.__Root = tree.getroot()
        this.__Dictionary=dict()
        
        for registerNode in this.__Root :
            if registerNode.tag == this.NodeName.Register.value :
                propNode = registerNode.find('Property')
                this.__Dictionary[propNode.text] = registerNode

    def print(this) :
        for registerNode in this.__Dictionary.values() :
            regAddr = registerNode.get('ID')
            regAddr = int(regAddr, 16)
            propNode = registerNode.find('Property')
            print(propNode.text + "  " + '{:#x}'.format(regAddr) )

    def PrintAllRegName(this) :
        for regNode in this.__Root :
            if regNode.tag == this.NodeName.Register.value :
                regName = regNode.find('Property').text
                regAddr = int(regNode.get('ID'), 16)
                print(regName+'='+'0x%02X' % regAddr )

    def GetAddr(this, regName) :
         nid=regName.upper()
         regNode = this.__Dictionary[nid]
         regAddr = int(regNode.get('ID'), 16)
         return regAddr

    def __getitem__(this, regName) :
        return this.GetAddr(regName)   


class XmlANA6705(Xml) :    
    def __init__(this) :
        Xml.__init__(this, TChip.Type.ANA6705)

class XmlANA6706(Xml) :    
    def __init__(this) :
        Xml.__init__(this, TChip.Type.ANA6706)

