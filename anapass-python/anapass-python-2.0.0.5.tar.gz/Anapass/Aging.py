

from Anapass.TModule import *
from abc import ABCMeta, abstractmethod
import os
import sys
import getopt

class Base(metaclass=ABCMeta) :

    class Status(enum.IntEnum) : 
        Begin = 1
        End = 2

    class Item :
        def __init__(this, obj, loopCnt) : 
            this.__Obj = obj
            this.__loopCnt = loopCnt

        def Run(this) :
            for i in range(this.__loopCnt) :
                this.__Obj.Run()

        def GetObj(this) :
            return this.__Obj

    def __init__(this, device, dutIdx, id, desc) : 
        this.device = device
        this.ID = id;
        this.desc = desc
        this.__ItemList=[]
        this.DutIdx = dutIdx
        this.IsRunTcStep = True

    def Add(this, obj, loopCnt=1) :
        item = Base.Item(obj, loopCnt)
        this.__ItemList.append(item)

    def Begin(this) : this.__Begin__()
    def __Begin__(this) : pass
    def End(this) : this.__End__()
    def __End__(this) : pass
    def Run(this) :
        this.Begin()
        for item in this.__ItemList :
            item.Run()
        this.__Run__()
        this.End()
    def __Run__(this) : pass

    def GetItemList(this) :
        return this.__ItemList

    def GetItemCount(this) :
        return len(this.__ItemList)

    def GetID(this):
        return this.ID

    def SetRunTcStep(this, flag) :
        this.IsRunTcStep = flag
        for item in this.__ItemList :
            item.GetObj().SetRunTcStep(flag)

class TCStepBase(Base) : 

    def ParsingID(className) :
        assert className[0:7]=='TCStep_'
        szID = className[7:]
        ID=int(szID)
        return ID

    def __init__(this, classID, device, dutIdx, desc) : 
        
        if type(classID) == type('') :
            #print("type is String")
            Base.__init__(this, device, dutIdx, TCStepBase.ParsingID(classID), desc)   #className must be  format  'TCStep_XX' 
        elif type(classID) == type(1) : 
            #print("type is INT")
            Base.__init__(this, device, dutIdx, classID, desc)
        else :
            raise AssertionError()

        this._JobID = -1
        this._ScID = -1
        this._TcID = -1
        this._TcIndex = -1
        
        this._ScCount = 0
        this._TcCount = 0
        this._TcStepCount = 0


    def Begin(this) : 

        this.device.AgingSetCurTcStepInfo(this.DutIdx, this.ID, Base.Status.Begin.value, this.desc)
        sysErrFlag = this.device.SysGetErrFlag()

        print("-------------------------------------------------------------------------------------------------------------------------")
        print("TCStep[%d-(%d/%d)] : %s  JobID=%d ScID=%d/%d TcIdx=%d/%d  SysErrFlag=0x%016X" %(this._TcID, this.ID, this._TcStepCount, this.desc, this._JobID, this._ScID, this._ScCount, this._TcIndex, this._TcCount, sysErrFlag) )
        print("--------------------------------------------------------------------------------------------------------------------------")

        if this.IsRunTcStep : 
            this.__Begin__()
        
    
    def End(this) : 

        this.device.AgingMeasureADC(this.DutIdx)
        sysErrFlag = this.device.SysGetErrFlag()

        if this.IsRunTcStep : 
            this.__End__()

        print("");
        print("");
        this.device.AgingSetCurTcStepInfo(this.DutIdx, this.ID, Base.Status.End.value, this.desc)

    def Run(this) :
        this.Begin()

        sysErrFlag = this.device.SysGetErrFlag()
        if this.IsRunTcStep  : 
            this.__Run__()
        else :
            print("TCStep[%d-(%d/%d)] : SKIP  SysErrFlag=0x%016X" %(this._TcID, this.ID, this._TcStepCount, sysErrFlag) )

        this.End()

    def SetJobID(this, jobID) :
        this._JobID = jobID
    
    def SetScID(this, scID) :
        this._ScID = scID
    
    def SetTcID(this, tcID) :
        this._TcID = tcID

    def SetTcIndex(this, tcIdx) :
        this._TcIndex = tcIdx

    def SetScCount(this, scCnt) :
        this._ScCount = scCnt

    def SetTcCount(this, tcCnt) :
        this._TcCount = tcCnt

    def SetTcStepCount(this, tcStepCount) :
        this._TcStepCount = tcStepCount
    

class TCBase(Base) : 

    def ParsingID(pyFileName) :
        baseName = os.path.basename(pyFileName)
        assert baseName[0]=='T'
        assert baseName[1]=='C'
        assert baseName[2]=='_'
        szID = baseName[3:7]
        assert baseName[7]=='.'
        assert baseName[8]=='p'
        assert baseName[9]=='y'
        ID=int(szID)
        return ID

    def __init__(this, pyFileName, device, dutIdx, desc) : 
        Base.__init__(this, device, dutIdx, TCBase.ParsingID(pyFileName), desc)
        this.__List=[]

        this._JobID = -1
        this._ScID = -1
        this._ScCount = 0
        this._TcCount = 0
        this._TcIndex = 0

        this._IsRunAvailable = True
         
    def Begin(this) : 

        this.device.AgingSetCurTcInfo(this.DutIdx, this.ID, Base.Status.Begin.value, 0, this.GetItemCount(), this.desc)
        sysErrFlag = this.device.SysGetErrFlag()

        print("***********************************************************************************")
        print("TC_%04d Begin : TcStepCnt=%d  %s  Job=%d Sc=%d tcCnt=%d  SysErr=0x%016X" %(this.ID, this.GetItemCount(), this.desc, this._JobID, this._ScID, this._TcCount, sysErrFlag) )
        
        tcStepList = this.GetItemList()
        for tcStepItem in tcStepList :
            tcStepItem.GetObj().SetJobID(this._JobID)
            tcStepItem.GetObj().SetScID(this._ScID)
            tcStepItem.GetObj().SetScCount(this._ScCount)
            tcStepItem.GetObj().SetTcID(this.GetID())
            tcStepItem.GetObj().SetTcIndex(this._TcIndex)
            tcStepItem.GetObj().SetTcCount(this._TcCount)
            tcStepItem.GetObj().SetTcStepCount(this.GetItemCount())
        

        if this.IsRunTcStep : 
            this.__Begin__()

    
    def End(this) : 

        sysErrFlag = this.device.SysGetErrFlag()
        if this.IsRunTcStep : 
            this.__End__()
        
        print("TC_%04d End : TcStepCnt=%d  %s  sysErrFlag=0x%016X" %(this.ID, this.GetItemCount(), this.desc, sysErrFlag) )
        print("***********************************************************************************")
        print()

        this.device.AgingSetCurTcInfo(this.DutIdx, this.ID, Base.Status.End.value, this.GetItemCount()-1, this.GetItemCount(), this.desc)
    
    def SetJobID(this, jobID) :
        this._JobID = jobID

    def SetScID(this, scID) :
        this._ScID = scID

    def SetTcIndex(this, tcIdx) :
        this._TcIndex = tcIdx
    
    def SetTcCount(this, tcCount) :
        this._TcCount = tcCount
    
    def SetScCount(this, scCount) :
        this._ScCount = scCount
    
        
class SCBase(Base) : 

    def ParsingID(pyFileName) :
        baseName = os.path.basename(pyFileName)
        assert baseName[0]=='S'
        assert baseName[1]=='C'
        assert baseName[2]=='_'
        szID = baseName[3:7]
        assert baseName[7]=='.'
        assert baseName[8]=='p'
        assert baseName[9]=='y'
        ID=int(szID)
        return ID


    def __init__(this, classID, device, dutIdx, desc) : 
        
        if type(classID) == type('') :
            #print("type is String")
            Base.__init__(this, device, dutIdx, SCBase.ParsingID(classID), desc)   #className must be  format  'TCStep_XX' 
        elif type(classID) == type(1) : 
            #print("type is INT")
            Base.__init__(this, device, dutIdx, classID, desc)
        else :
            raise AssertionError()

        this.__List=[]
        this._JobID = -1
        this._ScCount = 0
    
    def Begin(this) : 
        print("###############################################################################################################")
        print("SC_%04d Begin: TcCnt=%d %s  JobID=%d ScCnt=%d" %(this.ID, this.GetItemCount(), this.desc, this._JobID, this._ScCount) )
        
        tcIdx = 0
        tcStepList = this.GetItemList()
        for tcStepItem in tcStepList :
            tcStepItem.GetObj().SetJobID(this._JobID)
            tcStepItem.GetObj().SetScID(this.GetID())
            tcStepItem.GetObj().SetScCount(this._ScCount)
            tcStepItem.GetObj().SetTcIndex(tcIdx)
            tcStepItem.GetObj().SetTcCount(this.GetItemCount())

            tcIdx = tcIdx +1 


        this.__Begin__()
        this.device.AgingSetCurScInfo(this.DutIdx, this.ID, Base.Status.Begin.value, 0, this.GetItemCount(), this.desc)


    def End(this) : 
        this.device.AgingSetCurScInfo(this.DutIdx, this.ID, Base.Status.End.value, this.GetItemCount()-1, this.GetItemCount(), this.desc)
        this.__End__()
                
        print("SC_%04d End: TcCnt=%d %s  JobID=%d ScCnt=%d" %(this.ID, this.GetItemCount(), this.desc, this._JobID, this._ScCount) )
        print("###############################################################################################################")
        print()
        print()
        
    def SetJobID(this, jobID) :
        this._JobID = jobID

    def SetScCount(this, scCount) :
        this._ScCount = scCount
    

class JobBase(Base) : 
    
    def ParsingID(pyFileName) :
        baseName = os.path.basename(pyFileName)
        assert baseName[0]=='J'
        assert baseName[1]=='O'
        assert baseName[2]=='B'
        assert baseName[3]=='_'
        szID = baseName[4:8]
        ID=int(szID)
        assert baseName[8]=='.'
        assert baseName[9]=='p'
        assert baseName[10]=='y'
        return ID

    def __init__(this, pyFileName, device, dutIdx, desc) : 
        Base.__init__(this, device, dutIdx, JobBase.ParsingID(pyFileName), desc)
        this.__List=[]

    def Begin(this) : 
        print()
        print()
        print("//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
        print("JOB_%04d Begin: ScCnt=%d  %s" %(this.ID, this.GetItemCount(), this.desc) )
        
        tcStepList = this.GetItemList()
        for tcStepItem in tcStepList :
            tcStepItem.GetObj().SetJobID(this.GetID())
            tcStepItem.GetObj().SetScCount(this.GetItemCount())

        this.__Begin__()
        this.device.AgingSetCurJobInfo(this.DutIdx, this.ID, Base.Status.Begin.value, 0, this.GetItemCount(), this.desc)

    def End(this) : 
        this.__End__()
        this.device.AgingSetCurJobInfo(this.DutIdx, this.ID, Base.Status.End.value, this.GetItemCount()-1, this.GetItemCount(), this.desc)

        print("-------------------------------------------------")
        print("JOB_%04d End: ScCnt=%d  %s" %(this.ID, this.GetItemCount(), this.desc) )
        print("//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
        print()
        print()
        print()
        

class App :

    def print_help() :
        print(" ")
        print("py TC_xxxx.py --boardid=<boardid> ")
        print(" ")
        print("   <options-name>")
        print("       --boardid:  execute board id")
        print(" ")

    def __init__(this, pyFileName, argv) : 

        try :
            # opts : getopt 옵션에 따라 파싱 ex) [('-i', 'myin')]
            # etc_args: getopt 옵션 이외에 입력된 일반 Argument
            # argv 첫번째 (index:0) 는 Python파일명, 두번째 (index:1) 부터  Arguments
            opts, etc_args = getopt.getopt(sys.argv[1:], "hb:", ["help", "boardid=" ])

        except getopt.GetoptError:  #옵션지정이 올바르지 않은 경우
            print("ERROR :  the name of option is invalid")
            sys.exit()

        this._PyFileName = os.path.basename(pyFileName)
        this.__BoardID = -1
        for opt, arg in opts :
            if opt in ("-h", "--help") :
                App.print_help()
                sys.exit();

            elif opt in ("-b", "--boardid") :
                this.__BoardID = int(arg)

    def GetBoardID(this) :
        return this.__BoardID;

    def GetDevice(this) :
        return this.__TDevice

    def Begin(this) : 
        #TDevice Create
        this.__TDevice = TDevice(TDevice.Type.TESys)
        this.__TDevice.SysSetServerIPAddr("127.0.0.1")  
        
        print("Connect To " + this.__TDevice.GetName() )
    
        #TDevice Connect
        isConnect = this.__TDevice.Connect()
        assert isConnect 

        #if user set BoardID, it sends BoardID to TESys-Python-Module 
        if(this.__BoardID > 0) :
            print("SetBoardID  %d" % this.__BoardID )
            this.__TDevice.SysSetBoardID(this.__BoardID)

        #Notify PyStart
        this.__TDevice.AgingNotifyPyStart(this._PyFileName)


    def End(this) :

        #Notify PyStop
        this.__TDevice.AgingNotifyPyStop(this._PyFileName)

        #Disconnect
        print("Disconnect from " + this.__TDevice.GetName() )
        this.__TDevice.Disonnect()
        
        
        print("----------------------------------------------------------------");
        print("MeasourceAdCCount = %d"%this.__TDevice.GetAgingMeasureADCCount())
        print("----------------------------------------------------------------");

        print("End of Exam. Bye!!")
        print()

        


