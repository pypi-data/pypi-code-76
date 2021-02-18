#
# Aidlab_peripheral.py
# Aidlab-SDK
# Created by Szymon Gesicki on 10.05.2020.
#

from Aidlab.AidlabCharacteristicsUUID import AidlabCharacteristicsUUID
from Aidlab.AidlabNotificationHandler import AidlabNotificationHandler

from bleak import BleakClient, discover, BleakError
import asyncio
from multiprocessing import Process
import sys
import logging

logging.getLogger("bleak").setLevel(logging.ERROR)

class AidlabPeripheral():
    connected_aidlab = []

    def __init__(self, aidlab_delegate):
        self.aidlab_delegate = aidlab_delegate
        self.queue_to_send = []
        self.max_cmd_length = 20

    async def scan_for_aidlab(self):

        devices = await discover()
        # Container for Aidlab's MAC addresses (these were found during the scan process)
        aidlabMACs = []

        for dev in devices:
            # Device found with dev.name
            if dev.name == "Aidlab" and dev.address not in self.connected_aidlab:
                aidlabMACs.append(dev.address)
        return aidlabMACs

    def run(self, characteristics, aidlabs_address=None):
        
        loop = asyncio.get_event_loop()
        self.connect(characteristics, loop, aidlabs_address)

    def connect(self, characteristics, loop, aidlabs_address=None):

        # Connect to all Aidlabs from `aidlabsMAC` list
        if aidlabs_address:
            logging.info("Connecting to %s", aidlabs_address)
            self.create_task(characteristics, aidlabs_address, loop, False)
            # All Aidlabs connected, end the loop
            return

        # Connect to every discoverable Aidlab
        else:
            print("Scanning ...")

            while True:
                aidlabs_address = loop.run_until_complete(self.scan_for_aidlab())

                if aidlabs_address != []:
                    logging.info("Connecting to %s",aidlabs_address)
                    self.create_task(characteristics, aidlabs_address, loop, True)

    def create_task(self, characteristics, aidlabs_address, loop, should_scan):

        if 'linux' in sys.platform:
            for aidlab_address in aidlabs_address:
                Process(target=self.between, args=(characteristics, aidlab_address, loop)).start()
                self.connected_aidlab.append(aidlab_address)
        else:
            for aidlab_address in aidlabs_address:
                try:
                    loop.create_task(self.connect_to_aidlab(characteristics, aidlab_address, loop))
                except:
                    pass
                finally:
                    self.connected_aidlab.append(aidlab_address)

            if should_scan:
                # task to look for more aidlabs
                loop.create_task(self.connect(characteristics, loop))

            loop.run_forever()

    def between(self, characteristics, aidlab_address, loop):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.connect_to_aidlab(characteristics, aidlab_address, loop))
        except:
            pass

    async def connect_to_aidlab(self, characteristics, aidlab_address, loop):

        client = BleakClient(aidlab_address, loop=loop)

        try:
            await client.connect(timeout=10)

            self.aidlab_delegate.create_aidlabSDK(aidlab_address)

            # Harvest Device Information
            firmware_revision = (await client.read_gatt_char("00002a26-0000-1000-8000-00805f9b34fb")).decode('ascii')
            self.aidlab_delegate.did_receive_raw_firmware_revision(firmware_revision, aidlab_address)

            self.aidlab_delegate.did_receive_raw_hardware_revision(
                (await client.read_gatt_char("00002a27-0000-1000-8000-00805f9b34fb")).decode('ascii'), aidlab_address)

            self.aidlab_delegate.did_receive_raw_manufacture_name(
                (await client.read_gatt_char("00002a29-0000-1000-8000-00805f9b34fb")).decode('ascii'), aidlab_address)

            self.aidlab_delegate.did_receive_raw_serial_number(
                (await client.read_gatt_char("00002a25-0000-1000-8000-00805f9b34fb")).decode('ascii'), aidlab_address)

            self.aidlab_delegate.did_connect_aidlab(aidlab_address)

            # We always want to notify the command line
            if not "cmd" in characteristics:
                characteristics.append("cmd")

            self.aidlabCharacteristicsUUID = AidlabCharacteristicsUUID(firmware_revision)

            aidlabNotificationHandler = AidlabNotificationHandler(aidlab_address,  self.aidlab_delegate, self.aidlabCharacteristicsUUID)

            for characteristic in characteristics:
                await client.start_notify(self.converter_to_uuid(characteristic, aidlab_address), aidlabNotificationHandler.handle_notification)

            while True:
                await self.send_command_if_needed(client)
                await asyncio.sleep(1, loop=loop)
                if not await client.is_connected():
                    self.aidlab_delegate.did_disconnect_aidlab(aidlab_address)
                    self.aidlab_delegate.destroy(aidlab_address)
                    self.connected_aidlab.remove(aidlab_address)
                    break
        except:
            if aidlab_address in self.connected_aidlab: self.connected_aidlab.remove(aidlab_address)


    def start_synchronization(self, address):
        self.queue_to_send.append({"address": address, "command": "sync start"})

    def stop_synchronization(self, address):
        self.queue_to_send.append({"address": address, "command": "sync stop"})
    
    def send(self, address, command):
        self.queue_to_send.append({"address": address, "command": command})

    async def send_command_if_needed(self, client):
        while self.queue_to_send:
            command = self.queue_to_send.pop(0)
            await self.send_command(client, command["address"], command["command"])

    async def send_command(self, client, aidlab_address, command):
        write_value = self.aidlab_delegate.get_command(aidlab_address, command)
        size = write_value[3] | (write_value[4] << 8)
        message = [write_value[i] for i in range(size)]

        for i in range(round(int(size/self.max_cmd_length) + (size%self.max_cmd_length > 0))):
            message_byte = bytearray(message[i*self.max_cmd_length:(i+1)*self.max_cmd_length])
            await client.write_gatt_char(AidlabCharacteristicsUUID.cmdUUID["uuid"], message_byte)
        
    def converter_to_uuid(self, characteristic, aidlab_address):
        if characteristic == "temperature":
            return self.aidlabCharacteristicsUUID.temperatureUUID["uuid"]
        elif characteristic == "ecg":
            return self.aidlabCharacteristicsUUID.ecgUUID["uuid"]
        elif characteristic == "battery":
            return self.aidlabCharacteristicsUUID.batteryUUID["uuid"]
        elif characteristic == "respiration":
            return self.aidlabCharacteristicsUUID.respirationUUID["uuid"]
        elif characteristic == "motion":
            return self.aidlabCharacteristicsUUID.motionUUID["uuid"]
        elif characteristic == "activity":
            return self.aidlabCharacteristicsUUID.activityUUID["uuid"]
        elif characteristic == "steps":
            return self.aidlabCharacteristicsUUID.stepsUUID["uuid"]
        elif characteristic == "orientation":
            return self.aidlabCharacteristicsUUID.orientationUUID["uuid"]
        elif characteristic == "heartRate":
            return self.aidlabCharacteristicsUUID.heartRateUUID["uuid"]
        elif characteristic == "healthThermometer":
            return self.aidlabCharacteristicsUUID.healthThermometerUUID["uuid"]
        elif characteristic == "soundVolume":
            return self.aidlabCharacteristicsUUID.soundVolumeUUID["uuid"]
        elif characteristic == "cmd":
            return self.aidlabCharacteristicsUUID.cmdUUID["uuid"]

        logging.error(f"Signal {characteristic} not supported")
        self.aidlab_delegate.did_disconnect_aidlab(aidlab_address)
        exit()
