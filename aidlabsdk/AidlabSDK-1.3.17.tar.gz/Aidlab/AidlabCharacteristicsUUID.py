#
# AidlabCharacteristicsUUID.py
# Aidlab-SDK
# Created by Szymon Gesicki on 10.05.2020.
#

import sys
from packaging import version

class AidlabCharacteristicsUUID:

    def __init__(self, fw_version):

        if version.parse("3.0.0") < version.parse(fw_version):
            self.orientationUUID =        {"uuid": "63366e80-cf3a-11e1-9ab4-0002a5d5c51b", "handle": 58} 
            self.motionUUID =             {"uuid": "49366e80-cf3a-11e1-9ab4-0002a5d5c51b", "handle": 61}
        else:
            self.orientationUUID =        {"uuid": "63366e80-cf3a-11e1-9ab4-0002a5d5c51b", "handle": 55} 
            self.motionUUID =             {"uuid": "49366e80-cf3a-11e1-9ab4-0002a5d5c51b", "handle": 58}

        self.temperatureUUID =        {"uuid": "45366e80-cf3a-11e1-9ab4-0002a5d5c51b", "handle": 25}
        self.ecgUUID =                {"uuid": "46366e80-cf3a-11e1-9ab4-0002a5d5c51b", "handle": 16}
        self.batteryUUID =            {"uuid": "47366e80-cf3a-11e1-9ab4-0002a5d5c51b", "handle": 22}
        self.respirationUUID =        {"uuid": "48366e80-cf3a-11e1-9ab4-0002a5d5c51b", "handle": 19}
        self.activityUUID =           {"uuid": "61366e80-cf3a-11e1-9ab4-0002a5d5c51b", "handle": 49}
        self.stepsUUID =              {"uuid": "62366e80-cf3a-11e1-9ab4-0002a5d5c51b", "handle": 52}
        self.soundVolumeUUID =        {"uuid": "52366e80-cf3a-11e1-9ab4-0002a5d5c51b", "handle": 31}
        self.cmdUUID =                {"uuid": "51366e80-cf3a-11e1-9ab4-0002a5d5c51b", "handle": 13}
        self.heartRateUUID =          {"uuid": "00002a37-0000-1000-8000-00805f9b34fb", "handle": 45}
        self.healthThermometerUUID =  {"uuid": "00002a1c-0000-1000-8000-00805f9b34fb", "handle": 63}

        



    
