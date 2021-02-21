import platform
import pygatt
import os
import sys
from kivy.logger import Logger


def resource_path(rel_path):
    if hasattr(sys, '_MEIPASS'):
        print("Has attr MEIPASS")
        return os.path.join(sys._MEIPASS, rel_path)

    return os.path.join(os.path.abspath("."), rel_path)


def resolve_backend(backend):
    if backend in ['auto', 'gatt', 'bgapi']:
        platformName = platform.system().lower()
        if backend == 'auto':
            if platformName == 'linux' or platformName == 'linux2':
                backend = 'gatt'
            elif platformName == 'windows' and int(platform.version().replace('.', '')) >= 10015063:
                backend = 'bgapi'
            else:
                backend = 'bgapi'
        return backend
    else:
        raise (ValueError('Backend must be one of: auto, gatt, bgapi'))


def find_muse(name=None):
    muses = list_muses()
    if name:
        for muse in muses:
            if muse['name'] == name:
                return muse
    elif muses:
        return muses[0]


def list_muses(backend='bgapi', interface=None):
    Logger.info("initial backend: " + str(backend))
    backend = resolve_backend(backend)
    Logger.info("Resolveed backend: " + str(backend))
    if backend == 'gatt':
        Logger.info("Utilizing pygatt backend...")
        interface = interface or 'hci0'
        adapter = pygatt.GATTToolBackend(interface)
    else:
        Logger.info("Utilizing BGAPI backend")
        adapter = pygatt.BGAPIBackend(serial_port=interface)

    Logger.info("Adapter selection was successful")
    Logger.info("Starting the adapter")
    adapter.start()
    Logger.info("Adapter started without an issue")
    Logger.info("Scanning using: " + str(adapter))
    # print('Searching for Muses, this may take up to 10 seconds...                                 ')
    devices = adapter.scan(timeout=10.5)
    Logger.info("Scanning complete, stopping the adapter")
    Logger.info("Found devices: " + str(devices))
    adapter.stop()
    Logger.info("adapter Stopped")
    muses = []

    for device in devices:
        if device['name'] and 'Muse' in device['name']:
            muses = muses + [device]

    if muses:
        for muse in muses:
            pass
            # print('Found device %s, MAC Address %s' %
            #       (muse['name'], muse['address']))
    else:
        pass
        # print('No Muses found.')
    Logger.info("returning muses: " + str(muses))
    return muses


def is_data_valid(data, timestamps):
    if timestamps == 0.0:
        return False
    if all(data == 0.0):
        return False
    return True


def PPG_error(Exceptions):
    pass
