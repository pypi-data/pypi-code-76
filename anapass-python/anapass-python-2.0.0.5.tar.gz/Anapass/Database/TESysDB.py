
import pymysql
from . import TESys


class TESysDB :  

    def Connect(this) : 
        #print("TESysDB.Connect")
        this.__Conn = pymysql.connect(host='205.239.162.119', port=12919, user='anapass', password='ana!@34', db='TESysDB', charset='utf8')
        assert(this.__Conn != None)
        this.__SingleSc = TESys.Single.Sc(this.__Conn)
        this.__SingleTc = TESys.Single.Tc(this.__Conn)
        this.__SingleHardware = TESys.Single.Hardware(this.__Conn)
        this.__JoinTcStepList = TESys.Join.TcStepList(this.__Conn)

    def Disconnect(this) : 
        #print("TESysDB.Disconnect")
        this.__Conn.close()

    def ExportToCSV(this, csvFileName, *, boardId=-1, jobId=-1, scId=-1, tcId=-1, tcStepId=-1 ) : 
        
        assert(jobId != -1)
        
        hardwareAk=-1
        scAk = -1
        tcAk = -1

        if boardId != -1 :
            hardwareAk = this.__SingleHardware.GetAK(boardId)

        if scId != -1 :
            scAk = this.__SingleSc.GetAK(jobId, scId)

        if tcId != -1 :
            tcAk = this.__SingleTc.GetAKWithJob(jobId, tcId)
        
        
        return this.__JoinTcStepList.ExportToCSV(csvFileName, hardwareAk=hardwareAk, jobId=jobId, scAk=scAk, tcAk=tcAk)




