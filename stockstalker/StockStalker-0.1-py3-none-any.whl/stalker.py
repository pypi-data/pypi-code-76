import StockStalker.utils as utils
from StockStalker.present import getLiveData

import pandas as pd
import threading
import time
import os
import logging

class StalkerCallback:
    def __init__(self, function=None):
        self.func = function
        #self.args = arg

class Stalker:
    def __init__(self, target=None, duration=None, verbose=True, name="Bob", long_poll_delay=30, save=True, save_location="saves", dailyCallback=None, doneCallback=None):
        self.target = target
        self.duration = duration
        self.verbose = verbose
        self.name = name
        self.pollDelay = long_poll_delay
        self.save = save
        self.saveLoc = save_location

        self.dailyCallback = dailyCallback
        self.doneCallback = doneCallback

        self.df = pd.DataFrame(columns=["Symbol","Price","Change","P/E","Ranges","Open","previousClose","EPS","marketCap","volume"])

        self.thread = None
        self.__killed = False

    def __update(self):
        newData = None

        try:
            newData = getLiveData(self.target, format="DataFrame")
        except:
            return

        length = len(self.df.index)

        newData = newData.values.tolist()

        self.df.loc[length+1] = newData[0]

        print("Updated Values")

    def __save(self):
        if os.path.exists(self.saveLoc) == False:
            os.mkdir(self.saveLoc)
        print(f"Stalker '{self.name}' saved to file")
        self.df.to_csv(f"{self.saveLoc}/{self.name}.csv")


    def __run(self):
        for x in range(0, self.duration):

            if self.__killed:
                break

            if self.verbose:
                print(f"Stalker '{self.name}' began polling for market open")

            while utils.marketOpen() == False:
                if self.verbose:
                    print(f"Stalker '{self.name}' polled for market open")
                if self.__killed:
                    break

                time.sleep(self.pollDelay)

            self.__update()

            if self.save:
                self.__save()

            if self.dailyCallback != None:
                self.dailyCallback.func()

            print(f"Stalker '{self.name}' is waiting for the next day")

            duration = 18000

            for y in range(0, duration):
                if self.__killed:
                    break
                time.sleep(1)


        if self.doneCallback != None:
            self.doneCallback.func()


    #def loadParams(self, file):


    def run(self):

        self.thread = threading.Thread(target=self.__run)
        self.thread.start()

    def wait(self):
        self.thread.join()
    def kill(self):
        self.__killed = True