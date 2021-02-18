#
# IAidlab.py
# Aidlab-SDK
# Created by Szymon Gesicki on 22.06.2020.
#


class IAidlab:

    firmware_revision = ""
    serial_number = ""
    hardware_revision = ""
    address = ""

    def __init__(self, delegate):
        self.delegate = delegate

    def set_ecg_filtration_method(self, method):
        self.delegate.set_ecg_filtration_method(method)

    def start_synchronization(self):
        self.delegate.start_synchronization(self.address)        

    def stop_synchronization(self):
        self.delegate.stop_synchronization(self.address)
    
    def send(self, command):
        self.delegate.send(self.address, command)


    
    