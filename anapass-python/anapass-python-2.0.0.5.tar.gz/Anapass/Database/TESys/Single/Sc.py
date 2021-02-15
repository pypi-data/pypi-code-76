

import pymysql
import enum
from Anapass import Database

class Sc(Database.Lib.Single.Table) : 

    class ColIdx(enum.IntEnum) : 
        ScAK = 0
        JobID = 1
        ScID = 2
        Desc = 3
    
    def __init__(this, conn) : 
        Database.Lib.Single.Table.__init__(this, this.__class__.__name__)
        this.__Conn = conn

    def GetAK(this, jobId, scId) : 
        scAk = 0
        sql = "select * from %s where JobID='%d' and ScID='%d' " % (this.GetTableName(), jobId, scId) 
        curs = this.__Conn.cursor()
        curs.execute(sql)

        while True :
            dbRow = curs.fetchone()
            if dbRow == None :
                break
            else :
                scAk = dbRow[Sc.ColIdx.ScAK]
                break

        return scAk
