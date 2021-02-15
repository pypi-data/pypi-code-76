



import pymysql
import enum
from Anapass import Database

class SocPcb(Database.Lib.Single.Table) : 

    class ColIdx(enum.IntEnum) : 
        SocPcbName = 0
        CpuName =1
        Date = 2
        Version =3

    class Type(enum.Enum) :
        MV8865_BASE_V2_1="MV8865 BASE v2.1"

    def __init__(this, conn) : 
        Database.Lib.Single.Table.__init__(this, this.__class__.__name__)
        this.__Conn = conn
    