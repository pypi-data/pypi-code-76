import vlc,os,json,logging

FM_DICT = {
    "Ohm Namashivaya[Chennai, India]":"http://162.144.239.190:8000/stream.mp3?listening-from-radio-garden=1612918979424",
    "Namakkal Thedal FM[Namakkal, India]":"http://dione.shoutca.st:8968/stream?listening-from-radio-garden=1612919057965",
    "Natrinai FM[Tiruchirappalli, India]":"http://centova32.instainternet.com:8340/stream?listening-from-radio-garden=1612919115682",
    "Pudukkottai Thedal FM[Pudukkottai, India]":"http://dione.shoutca.st:8972/stream?listening-from-radio-garden=1612919169681",
    "முத்தமிழ் FM மேலூர்[Melur, India]":"http://node-35.zeno.fm/kvpm9a0pb2zuv?listening-from-radio-garden=1612919268729&rj-tok=AAABd4mEDpIA2pXdZ2PkN--SLA&rj-ttl=5",
    "Virudhunagar Thedal FM[Virudhunagar, India]":"http://dione.shoutca.st:8976/stream?listening-from-radio-garden=1612919368792",
    "முகில்[Aruppukkottai, India]":"https://stream.zeno.fm/phv06yfkwzzuv?listening-from-radio-garden=1612919390648",
    "தமிழர் வானொலி Tamilar Radio[Sempatti, India]":"https://stream.zeno.fm/fef5f0avy7zuv?listening-from-radio-garden=1612919448064",
    "Thendral[Madathupatti, India]":"https://stream.zeno.fm/xzt706p3h2zuv?listening-from-radio-garden=1612919498933",
    "Kovilpatti Thedal FM[Kovilpatti, India]":"http://dione.shoutca.st:8936/stream?listening-from-radio-garden=1612919548825"
}

class Radio:
    def __init__(self):
        logging.basicConfig(level="INFO")
        self.player = 0
        self.getFmList = self.getlist()

    def getlist(self):
        try:
            dumpFmList = list()
            for item in (FM_DICT):
                dumpFmList.append(item)
            return dumpFmList
        except Exception as e:
            logging.error(e)
            return None

    def pause(self):
        try:
            if type(self.player) == int:
                logging.info("set Stream Fm")
            else:
                self.player.pause()
        except Exception as e:
            logging.error(e)
            return None

    def stop(self):
        try:
            if type(self.player) == int:
                logging.info("set Stream Fm")
            else:
                self.player.stop()
        except Exception as e:
            logging.error(e)
            return None

    def play(self):
        try:
            if self.player == 0:
                logging.info("set Stream Fm")
            else:
                self.player.play()
        except Exception as e:
            logging.error(e)
            return None

    def set_stream(self,index=int):
        try:
            if type(index) == int:
                if len(self.getFmList) >= index:
                    if self.player != 0:
                        self.player.stop()
                    FmName = self.getFmList[index]
                    FmStreamLink = FM_DICT[FmName]
                    vlcInstance = vlc.Instance()
                    self.player = vlcInstance.media_player_new()
                    self.player.set_mrl(FmStreamLink)
                else:
                    logging.info("out of index in fm number")
            else:
                logging.info("Input For int\nUse list_fm() fun!")
        except Exception as e:
            logging.error(e)
            return None

    def list_fm(self):
        try:
            dumplist = list()
            for item in enumerate(self.getFmList):
                # dumplist.append(item)
                print(item)
            # return dumplist
        except Exception as e:
            logging.info(e)

if __name__ == "__main__":
    Radio().set_stream(2)