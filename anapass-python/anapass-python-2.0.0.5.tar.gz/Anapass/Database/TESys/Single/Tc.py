

import pymysql
import enum
import datetime
from Anapass import Database

class Tc(Database.Lib.Single.Table) : 

    class ColIdx(enum.IntEnum) : 
        TcAK = 0
        TcID = 1
        TcStepCount = 2
        CreateDateTime=3
        Desc = 4
    
    def __init__(this, conn) : 
        Database.Lib.Single.Table.__init__(this, this.__class__.__name__)
        this.__Conn = conn

    def GetAK(this, tcId, tcStepCount, tcCreateTime) : 
        sql = "select * from %s where TcID='%d' and TcStepCount='%d' and CreateDateTime='%s' " % (this.GetTableName(), tcId, tcStepCount, tcCreateTime) 
        curs = this.__Conn.cursor()
        curs.execute(sql)
        dbRow = curs.fetchone()
        assert(dbRow != None)
        return dbRow[Tc.ColIdx.TcAK]

    def GetAKWithJob(this, jobId, tcId) :

        if jobId == 13 \
           or jobId == 14 \
           or jobId == 21 \
           or jobId == 22 \
           or jobId == 23 \
           or jobId == 24 \
           or jobId == 25 \
           or jobId == 26 :
            if tcId==1 : tcStepCount = 4
            elif tcId==2 : tcStepCount = 14
            elif tcId==3 : tcStepCount = 1380
            elif tcId==4 : tcStepCount = 77
            elif tcId==5 : tcStepCount = 768
            elif tcId==6 : tcStepCount = 12
            else : assert(False)

            tcCreateTime = datetime.datetime(2020, 12, 1, 0, 0, 0)
            
        elif jobId == 15 or jobId==16 :
            if tcId==1 : tcStepCount = 4
            elif tcId==2 : tcStepCount = 14
            elif tcId==3 : tcStepCount = 1346
            elif tcId==4 : tcStepCount = 77
            elif tcId==5 : tcStepCount = 768
            elif tcId==6 : tcStepCount = 12
            else : assert(False)

            tcCreateTime = datetime.datetime(2020, 12, 1, 0, 0, 0)

        elif jobId == 17 or jobId==18 or jobId==19 or jobId==20 :
            if tcId==1 : tcStepCount = 4
            elif tcId==2 : tcStepCount = 14
            elif tcId==3 : tcStepCount = 1338
            elif tcId==4 : tcStepCount = 77
            elif tcId==5 : tcStepCount = 768
            elif tcId==6 : tcStepCount = 12
            else : assert(False)

            tcCreateTime = datetime.datetime(2020, 12, 1, 0, 0, 0)

        else :
           assert(False)

        return this.GetAK(tcId, tcStepCount, tcCreateTime)

