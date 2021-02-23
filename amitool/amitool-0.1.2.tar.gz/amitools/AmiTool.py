import os
import redis
import traceback
from loguru import logger
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class AmiTools(object):
    """[初始化session和redis,自动创建log文件,loggers属性可以在此模块外使用]

    Args:
        LogDir (str): 日志文件目录, 
        ConnString (str): 数据库连接字符串,
        Host (str): redis的主机名, 
        PassWord (str): redis的auth密码, 
        Port (int): redis的端口号, 
        db (int): redis的连接库
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.__initLog()
        self.logger = logger
        self.diagnose = False
        
    def __initLog(self):
        logDir = self.kwargs.get("LogDir", "./log")
        logFileName = os.path.join(logDir, datetime.now().strftime("%Y%m%d") + ".log")
        logger.add(logFileName, format="{time:YYYY-MM-DD HH:mm:ss} - {file} - {line} - {level}: {message}", diagnose=self.diagnose)
    
    def initSession(self):
        connStr = self.kwargs.get("ConnString", "")
        try:
            engine = create_engine(connStr, echo=False)
            conn = engine.connect()
            result = conn.execute("select 1")
            assert result.fetchone()
        except Exception as e:
            logger.error(e.with_traceback(None))
            logger.error(traceback.format_exc())
            return None
        dbSession = scoped_session(sessionmaker(bind=engine))
        return dbSession()
    
    def initRedis(self):
        host = self.kwargs.get("Host", "")
        passwd = self.kwargs.get("PassWord", "")
        port = self.kwargs.get("Port", 6379)
        db = self.kwargs.get("db", 10)
        try:
            pool = redis.ConnectionPool(host=host,port=port,password=passwd,db=db)
            redis_conn = redis.Redis(connection_pool=pool)
            assert redis_conn.ping()
        except Exception as e:
            logger.error(e.with_traceback(None))
            logger.error(traceback.format_exc())
            return None
        return redis_conn
    
    def __getLogger(self):
        return self.logger
    
    def __setDiagnose(self):
        self.diagnose = True
    
    loggers = property(__getLogger)
    diagnose = property(__setDiagnose)
        
        
if __name__ == '__main__':
    ami = AmiTools(LogDir="./log", ConnString="", Host="127.0.0.1", PassWord="", Port=6379, db=10)
    # log = ami.initLog()
    session = ami.initSession()
    rs = ami.initRedis()
    