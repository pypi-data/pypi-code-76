import os
import time
import datetime
import sys
from pathlib import Path

class Logger:
    def __init__(self, config_dir):
        self.__config_filename = "settradesdk_config.txt"
        self.__config_path = self.__userHomeDir()
        self.__config_dir = config_dir

    def get_current_time(self):
        return time.time()

    def write(self, start_time, level, topic, message):
        start_datetime_str = self.__epoch_to_datetime_str(start_time)
        file = open(self.__get_current_log_file(), "a")
        elap_time = self.__get_elap_time(start_time, self.get_current_time())
        level = "[" + level + "]"
        start_datetime_str = "[" + start_datetime_str + "]"
        seperate = " - "
        elap_time = "[Elapsed time " + elap_time + "s]"
        file.write(start_datetime_str)
        file.write(seperate)
        file.write(elap_time)
        file.write(topic)
        file.write(seperate)
        file.write(str(message))
        file.write(seperate)
        file.write(level)
        file.write("\n")
        file.close()

    def create_log_dir(self):
        try:
            os.mkdir(str(Path(self.__config_path) / Path(self.__config_dir)))
        except Exception as e:
            pass

    def remove_expired_log(self):
        self.__days = self.__get_config_max_log_days(
            str(Path(self.__config_path) / Path(self.__config_filename))
        )
        # get all log files
        dir_path = str(Path(self.__config_path) / Path(self.__config_dir))
        files = os.listdir(dir_path)
        current_time = self.get_current_time()
        minus_time = self.__get_minus_time(self.__days)
        # get expired files
        expired_files = [
            file
            for file in files
            if (
                self.__is_expired(
                    self.__get_last_modified(str(Path(dir_path) / Path(file))),
                    current_time,
                    minus_time,
                )
            )
        ]
        # remove all expired files
        for expired_file in expired_files:
            self.__remove_file(dir_path, expired_file)

    def __get_config_max_log_days(self, config_full_path):
        file = open(config_full_path, "r")
        lines = file.readlines()
        for line in lines:
            try:
                if "clear_log=" in line:
                    line = line.replace("clear_log=", "")
                    line = line.replace(" ", "")
                    return int(line)
            except:
                print("clear_log must be integer! assume to be 30 days")
                return 30

    def __epoch_to_datetime_str(self, epoch):
        return datetime.datetime.fromtimestamp(epoch).strftime("%Y-%m-%d %H:%M:%S")

    def __get_minus_time(self, days):
        return days * 86400

    def __get_last_modified(self, path):
        return os.path.getmtime(path)

    def __remove_file(self, dir_path, file):
        os.remove(str(Path(dir_path) / Path(file)))

    def __is_expired(self, last_modified_time, current_time, minus_time):
        return last_modified_time < current_time - minus_time

    def __get_current_datetime_str(self):
        return datetime.datetime.today().strftime("%Y-%m-%d")

    def __get_elap_time(self, start_time, end_time):
        elap = end_time - start_time
        return "%.6f" % elap

    def __get_current_log_file(self):
        log_file = self.__get_current_datetime_str() + ".txt"
        return str(Path(self.__config_path) / Path(self.__config_dir) / Path(log_file))

    def __userHomeDir(self):
        path = ""
        home = ""
        postfix = ""

        if sys.platform == "win32":
            postfix = "/AppData"

        home = str(os.getenv("HOMEDRIVE")) + str(os.getenv("HOMEPATH"))
        if home == "NoneNone":
            home = os.getenv("USERPROFILE")
        if home == None:
            home = os.getenv("HOME")

        if home == "":
            path = "./"
        else:
            path = home + postfix
        return path
