


import pymysql
import enum
from Anapass import Database

class DutPcb(Database.Lib.Single.Table) : 

    class ColIdx(enum.IntEnum) : 
        DutPcbName = 0
        DutCount = 1
        Date = 2
        Version = 3

    class Type(enum.Enum) : 
        AGING_DUT_QTAB_ANA6707_P_10321 = "AGING_DUT_QTAB_ANA6707(P_10321)"
    
    def __init__(this, conn) : 
        Database.Lib.Single.Table.__init__(this, this.__class__.__name__)
        this.__Conn = conn
    