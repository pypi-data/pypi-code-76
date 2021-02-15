


import pymysql
import enum
import datetime
from Anapass import Database

class Hardware(Database.Lib.Single.Table) : 

    class ColIdx(enum.IntEnum) : 
        HardwareAK = 0
        BoardID = 1
        SocPcbName = 2
        DutPcbName = 3
        HardwareVersion = 4
    
    def __init__(this, conn) : 
        Database.Lib.Single.Table.__init__(this, this.__class__.__name__)
        this.__Conn = conn

    def GetAK(this, boardId) : 
        sql = "select * from %s where BoardID='%d' and SocPcbName='%s' and DutPcbName='%s' " \
            % (this.GetTableName(), \
            boardId, \
            Database.TESys.Single.SocPcb.Type.MV8865_BASE_V2_1.value, \
            Database.TESys.Single.DutPcb.Type.AGING_DUT_QTAB_ANA6707_P_10321.value) 

        curs = this.__Conn.cursor()
        curs.execute(sql)
        dbRow = curs.fetchone()
        assert(dbRow != None)
        return dbRow[Hardware.ColIdx.HardwareAK]

    