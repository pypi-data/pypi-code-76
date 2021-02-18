#
# AidlabNotificationHandler.py
# Aidlab-SDK
# Created by Szymon Gesicki on 09.05.2020.
#

from Aidlab.AidlabCharacteristicsUUID import AidlabCharacteristicsUUID

class AidlabNotificationHandler(object):


    def __init__(self, aidlab_address, delegate, aidlabCharacteristicsUUID):
        self.aidlab_address = aidlab_address
        self.delegate = delegate
        self.aidlabCharacteristicsUUID = aidlabCharacteristicsUUID

    def handle_notification(self, sender, data):

        try: 
            sender = sender.upper()
        except: 
            pass
        
        if sender == self.aidlabCharacteristicsUUID.temperatureUUID["handle"] or sender == self.aidlabCharacteristicsUUID.temperatureUUID["uuid"].upper():
            self.delegate.did_receive_raw_temperature(data, self.aidlab_address)

        elif sender == self.aidlabCharacteristicsUUID.ecgUUID["handle"] or sender == self.aidlabCharacteristicsUUID.ecgUUID["uuid"].upper():
            self.delegate.did_receive_raw_ecg(data, self.aidlab_address)

        elif sender == self.aidlabCharacteristicsUUID.batteryUUID["handle"] or sender == self.aidlabCharacteristicsUUID.batteryUUID["uuid"].upper():
            self.delegate.did_receive_raw_battery_level(data, self.aidlab_address)

        elif sender == self.aidlabCharacteristicsUUID.respirationUUID["handle"] or sender == self.aidlabCharacteristicsUUID.respirationUUID["uuid"].upper():
            self.delegate.did_receive_raw_respiration(data, self.aidlab_address)

        elif sender == self.aidlabCharacteristicsUUID.activityUUID["handle"] or sender == self.aidlabCharacteristicsUUID.activityUUID["uuid"].upper():
            self.delegate.did_receive_raw_activity(data, self.aidlab_address)

        elif sender == self.aidlabCharacteristicsUUID.stepsUUID["handle"] or sender == self.aidlabCharacteristicsUUID.stepsUUID["uuid"].upper():
            self.delegate.did_receive_raw_steps(data, self.aidlab_address)

        elif sender == self.aidlabCharacteristicsUUID.heartRateUUID["handle"] or sender == self.aidlabCharacteristicsUUID.heartRateUUID["uuid"].upper() or sender == "2A37":
            self.delegate.did_receive_raw_heart_rate(data, self.aidlab_address)

        elif sender == self.aidlabCharacteristicsUUID.healthThermometerUUID["handle"] or sender == self.aidlabCharacteristicsUUID.healthThermometerUUID["uuid"].upper() or sender == "2A1C":
            self.delegate.did_receive_raw_health_thermometer(data, self.aidlab_address)

        elif sender == self.aidlabCharacteristicsUUID.soundVolumeUUID["handle"] or sender == self.aidlabCharacteristicsUUID.soundVolumeUUID["uuid"].upper():
            self.delegate.did_receive_raw_sound_volume(data, self.aidlab_address)

        elif sender == self.aidlabCharacteristicsUUID.cmdUUID["handle"] or sender == self.aidlabCharacteristicsUUID.cmdUUID["uuid"].upper():
            self.delegate.did_receive_raw_cmd_value(data, self.aidlab_address)

        elif sender == self.aidlabCharacteristicsUUID.orientationUUID["handle"] or sender == self.aidlabCharacteristicsUUID.orientationUUID["uuid"].upper():
            self.delegate.did_receive_raw_orientation(data, self.aidlab_address)
    
        elif sender == self.aidlabCharacteristicsUUID.motionUUID["handle"] or sender == self.aidlabCharacteristicsUUID.motionUUID["uuid"].upper():
            self.delegate.did_receive_raw_imu_values(data, self.aidlab_address)
