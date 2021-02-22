import os
import stat
import datetime
import json


class LOG_Variable:
    LOG_RANGE = ["debug", "info", "error", "warn"]
    LOG_FOLDER = os.path.join(os.getcwd(), 'static', 'logs')


class LogHelper:

    def __init__(self):
        self._LOG_Variable = LOG_Variable
        for type in self._LOG_Variable.LOG_RANGE:
            filepath = os.path.join(self._LOG_Variable.LOG_FOLDER, type)
            if not os.path.exists(filepath):
                os.makedirs(filepath)
                os.chmod(filepath, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    def writeFile(self, type, str):
        if type in self._LOG_Variable.LOG_RANGE:
            filepath = os.path.join(self._LOG_Variable.LOG_FOLDER, type)
            f = open(os.path.join(filepath, datetime.datetime.today().strftime('%Y-%m-%d') + '.log'), mode="a+",
                     encoding='utf-8')
            f.writelines(str + "\n")
            f.close()
            return True
        else:
            return False

    def error(self, msg):
        msg = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {json.dumps(msg, ensure_ascii=False)}"
        flag = self.writeFile('error', msg)
        if flag:
            print("\033[31m", msg, "\033[0m")

    def debug(self, msg):
        msg = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {json.dumps(msg, ensure_ascii=False)}"
        flag = self.writeFile('debug', msg)
        if flag:
            print("\033[32m", msg, "\033[0m")

    def warning(self, msg):
        msg = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {json.dumps(msg, ensure_ascii=False)}"
        flag = self.writeFile('warn', msg)
        if flag:
            print("\033[33m", msg, "\033[0m")

    def info(self, msg):
        msg = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {json.dumps(msg, ensure_ascii=False)}"
        flag = self.writeFile('info', msg)
        if flag:
            print("\033[36m", msg, "\033[0m")
