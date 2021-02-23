import logging
import syslog
# syslog.syslog("### gulliversoft: This is a test message")
# syslog.syslog(syslog.LOG_INFO, "### gulliversoft: Test message at INFO priority")
# syslog.syslog(syslog.LOG_DEBUG, "### gulliversoft: Test message at DEBUG priority")

LOG_FORMATTER = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")        
ROOT_LOGGER = logging.getLogger()
ROOT_LOGGER.setLevel(logging.WARN)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(LOG_FORMATTER)
ROOT_LOGGER.addHandler(CONSOLE_HANDLER)

LOGGER = logging.getLogger("Daisy")

def setInfo():
    ROOT_LOGGER.setLevel(logging.INFO)

def setDebug():
    ROOT_LOGGER.setLevel(logging.DEBUG)
    
def debugEnabled():
    return ROOT_LOGGER.level == logging.DEBUG

def logToFile(filename):
    FILE_HANDLER = logging.FileHandler(filename)
    FILE_HANDLER.setFormatter(LOG_FORMATTER)
    ROOT_LOGGER.addHandler(FILE_HANDLER)

def debug(message):
    LOGGER.debug(message)
    syslog.syslog(syslog.LOG_DEBUG, message)

def info(message):
    LOGGER.info(message)
    syslog.syslog(syslog.LOG_INFO, message)

def warn(message):
    LOGGER.warn(message)
    syslog.syslog(syslog.LOG_WARNING, message)

def error(message):
    LOGGER.error(message)
    syslog.syslog(syslog.LOG_ERR, message)

def exception(message):
    LOGGER.exception(message)
    syslog.syslog(syslog.LOG_ALERT, message)

def printBytes(buff):
    for i in range(0, len(buff)):
        print("%03d: 0x%02X %03d %c" % (i, buff[i], buff[i], buff[i]))
        
