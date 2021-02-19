# -*- coding: utf-8 -*-
"""@author: skynet-devel"""

import os
import sys
import re
from pathlib import Path

import importlib_resources
from gi.repository import GLib
from PySide2 import QtCore
from PySide2.QtCore import QFile, QIODevice
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader

try:
    import appinfo
    from device_item import DeviceItem
    from modules.udisks2 import UDisks2
    from modules.filesize import FileSize
    from threads import Signals, WritingThread
    RESOURCES_UI = 'resources.ui'
    RESOURCES_ICONS = 'resources.icons'
except ImportError:
    # Works for pip installation
    from usb_imager import appinfo
    from usb_imager.device_item import DeviceItem
    from usb_imager.modules.udisks2 import UDisks2
    from usb_imager.modules.filesize import FileSize
    from usb_imager.threads import Signals, WritingThread
    RESOURCES_UI = 'usb_imager.resources.ui'
    RESOURCES_ICONS = 'usb_imager.resources.icons'


STATUSBAR_TIMEOUT = 5000

ABOUT = f"""\
The {appinfo.__appname__} is {appinfo.__copyright__} by {appinfo.__organisation__}.
It is released under the {appinfo.__license__} license.

Author:  {appinfo.__author__}
E-mail:  {appinfo.__author_email__}

Contributors:  {appinfo.__contributors__[0]}

Websites:
{appinfo.__url_source__}
{appinfo.__url_pip__}
"""

DONATION = f"""\
The developer needs some money for sex, drugs and rock'n roll !!!

PayPal:  {appinfo.__donation_paypal__}

€€€ $$$ Thank you !!! $$$ €€€
"""


class Application(QApplication):
    """QApplication"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # BUILD MAINWINDOW
        with importlib_resources.path(RESOURCES_UI,
                                      'usb-imager.ui') as ui_file_path:
            ui_file_name = str(ui_file_path)
            ui_file = QFile(ui_file_name)
            if not ui_file.open(QIODevice.ReadOnly):
                sys.exit(
                    f"Cannot open {ui_file_name}: {ui_file.errorString()}")

        loader = QUiLoader()
        window = loader.load(ui_file)

        ui_file.close()

        if not window:
            sys.exit(loader.errorString())

        # SET INSTANCE VARIABLES
        self.signal = Signals()
        self.__copythread = None
        # blksize is stored in comboBox_buffers data.

        self.__udisks2 = UDisks2()

        self.__udisks2.signal_connect_object_added(
            self.__callback_object_added)
        self.__udisks2.signal_connect_object_removed(
            self.__callback_object_removed)

        self.__ui = window
        with importlib_resources.path(RESOURCES_ICONS,
                                      'usb-imager.ico') as ico_path:
            self.__window_icon = QIcon(str(ico_path))
        self.__srcpath = None
        # Target path is stored in comboBox_devices data.

        # SLOTS
        self.__ui.pushButton_open.clicked.connect(self.__get_source_image)
        self.__ui.pushButton_write.clicked.connect(self.__write)

        self.__ui.actionAboutQt.triggered.connect(
            lambda: QMessageBox.aboutQt(self.__ui.centralwidget))

        self.__ui.actionAbout.triggered.connect(
            lambda: QMessageBox.about(
                self.__ui.centralwidget, "About USB-Imager", ABOUT))
        self.__ui.actionDonation.triggered.connect(
            lambda: QMessageBox.about(
                self.__ui.centralwidget, "Donation", DONATION))

        # SETTINGS
        self.__ui.setWindowIcon(self.__window_icon)
        self.__init_target_devices()

        self.__center_window(self.__ui)
        self.__ui.adjustSize()
        height = self.__ui.height()
        self.__ui.setFixedHeight(height)

    @property
    def udisks2(self):
        """Getter"""
        return self.__udisks2

    def __init_target_devices(self) -> None:
        block_device_pathes = self.__udisks2.get_object_pathes('block_devices')

        for object_path in block_device_pathes:
            if self.__is_usb_key(object_path):
                self.__add_device_item(object_path)

        mib = 1024 * 1024
        buffers = [mib * multiplier
                   for multiplier in range(1, 17)]
        for blksize in buffers:
            filesize = str(FileSize(blksize).convert('MiB'))
            self.__ui.comboBox_buffers.addItem(filesize, blksize)

    def __center_window(self, window) -> None:
        screen = self.desktop().screenNumber()
        screen_width = self.desktop().screenGeometry(screen).width()
        screen_height = self.desktop().screenGeometry(screen).height()

        width = (screen_width - window.width()) / 2
        height = (screen_height - window.height()) / 2

        window.move(width, height)

    def show_mainwindow(self) -> None:
        """Show mainwindow"""
        self.__ui.show()

    def __callback_object_added(self, sender, dbus_object):
        object_path = dbus_object.get_object_path()

        if self.__is_usb_key(object_path):
            device_name = self.__add_device_item(object_path)
            if device_name:
                self.__ui.statusbar.showMessage(
                    f"USB-Device added:  {device_name}", STATUSBAR_TIMEOUT)

    def __callback_object_removed(self, sender, dbus_object):
        object_path = dbus_object.get_object_path()

        device_name = self.__remove_device_item(object_path)
        current_msg = self.__ui.statusbar.currentMessage()
        if device_name and not current_msg.startswith("Error"):
            self.__ui.statusbar.showMessage(
                f"USB-Device removed:  {device_name}", STATUSBAR_TIMEOUT)

    def __is_usb_key(self, object_path: str) -> bool:
        is_usbdev = True

        whole_block_device_pathes = \
            self.__udisks2.get_object_pathes_whole_block_device()
        interface = self.__udisks2.get_interface(object_path, 'Block')
        if not interface:
            return False

        if object_path not in whole_block_device_pathes:
            is_usbdev = False
        elif re.search(r"[0-9]$", object_path):
            is_usbdev = False
        else:
            drive_path, device_path, size = \
                interface.get_properties('drive', 'device', 'size')

            if not drive_path or drive_path == '/':
                is_usbdev = False
            elif not device_path or device_path == '/':
                is_usbdev = False
            elif not size or size == 0:
                is_usbdev = False
            else:
                interface = self.__udisks2.get_interface(drive_path, 'Drive')
                if not interface:
                    return False

                connection_bus, removable = \
                    interface.get_properties('connection-bus', 'removable')

                if removable is False or connection_bus != "usb":
                    is_usbdev = False

        return is_usbdev

    def __add_device_item(self, object_path: str) -> str:
        device_name = ""

        device_item = DeviceItem()

        drive_path = \
            self.__udisks2.get_property(object_path, 'Block', 'drive')

        # Set device_item attributes
        device_item.object_path = object_path
        device_path = self.__udisks2.get_property(object_path,
                                                  'Block', 'device')
        device_item.path = Path(device_path)

        interface = self.__udisks2.get_interface(drive_path, 'Drive')
        device_item.size, vendor, model = \
            interface.get_properties('size', 'vendor', 'model')

        if vendor:
            device_item.vendor = vendor
        if model:
            device_item.model = model

        # Add device_item to combobox
        size = FileSize(device_item.size).convert(max_decimals=1)
        combobox_text = "{} - {} {} - {}".format(
            device_item.path.name, device_item.vendor, device_item.model, size)
        self.__ui.comboBox_devices.addItem(combobox_text, device_item)
        device_name = f"{device_item.vendor} {device_item.model}"

        return device_name

    def __remove_device_item(self, object_path: str) -> str:
        device_name = ""

        index_count = self.__ui.comboBox_devices.count()
        for index in range(index_count):
            device_item = self.__ui.comboBox_devices.itemData(index)
            if not device_item:
                continue
            if object_path == device_item.object_path:
                device_name = f"{device_item.vendor} {device_item.model}"
                self.__ui.comboBox_devices.removeItem(index)

        return device_name

    @QtCore.Slot()
    def __get_source_image(self) -> None:
        homedir = Path.home()
        filters = ('Image Files (*.iso *.img *.raw *.bin *.dd)',)

        path_name = QFileDialog.getOpenFileName(
            parent=self.__ui.centralwidget,
            caption="Open Image",
            dir=str(homedir),
            filter=';;'.join(filters)
            )[0]

        if path_name:
            path = Path(path_name)
            if path.match('*.iso') and not self.__is_bootable_iso(path):
                return
            self.__srcpath = path
            self.__ui.label_srcpath.setText(self.__srcpath.name)

    def __is_bootable_iso(self, path: Path) -> bool:
        is_bootable = False

        try:
            with open(str(path), 'rb') as file:
                file.seek(510)
                mbr_signature = file.read(2).hex()
        except OSError as error:
            self.__ui.statusbar.showMessage(error.args)
        else:
            if mbr_signature == '55aa':
                is_bootable = True
            else:
                message = "Selected ISO file is not bootable!"
                self.__ui.statusbar.showMessage(message, STATUSBAR_TIMEOUT)

        return is_bootable

    @QtCore.Slot()
    def __write(self) -> None:
        if self.__copythread and self.__copythread.isRunning():
            return

        device_item = self.__ui.comboBox_devices.currentData()

        # IS SOURCE IMAGE AND TARGET DEVICE SELECTED?
        if not self.__srcpath:
            message = "Please select an image to use!"
            self.__ui.statusbar.showMessage(message, STATUSBAR_TIMEOUT)
            return
        if not device_item:
            message = "Please select a device to use!"
            self.__ui.statusbar.showMessage(message, STATUSBAR_TIMEOUT)
            return

        # IS THE TARGET DEVICE TOO SMALL FOR WRITING THE IMAGE?
        srcfile_size = os.path.getsize(str(self.__srcpath))
        if srcfile_size > device_item.size:
            message = \
                "Error:  " \
                "The size of the device is too small to write the image."
            self.__ui.statusbar.showMessage(message, STATUSBAR_TIMEOUT)
            return

        # ARE ALL PARTITIONS OF THE TARGET DEVICE UNMOUNTED AND UNLOCKED?
        mounted_filesystem_interfaces = \
            self.__udisks2.get_mounted_filesystems(device_item.object_path)

        if mounted_filesystem_interfaces:
            # Security question
            text = \
                "This device is mounted in the filesystem.\n\n" \
                "Would you like to unmount it?"
            result = QMessageBox.warning(self.__ui.centralwidget,
                                         "Warning", text,
                                         QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.No:
                return

            for iface_fs in mounted_filesystem_interfaces:
                # Unmount device
                arg_options = self.__udisks2.preset_args['unmount']
                try:
                    iface_fs.call_unmount_sync(arg_options)
                except GLib.Error as error:
                    self.__ui.statusbar.showMessage(error.message)
                    return

                self.__udisks2.settle()

                # Lock device if unlocked
                object_path = iface_fs.get_object_path()
                unlocked_encrypted = \
                    self.__udisks2.get_unlocked_encrypted(object_path)
                if unlocked_encrypted:
                    arg_options = self.__udisks2.preset_args['lock']
                    try:
                        unlocked_encrypted.call_lock_sync(arg_options)
                    except GLib.Error as error:
                        self.__ui.statusbar.showMessage(error.message)
                        return

                    self.__udisks2.settle()

        # SECURITY QUESTION BEFORE WRITING.
        text = \
            "The device will be completely overwritten " \
            "and data on it will be lost.\n\n" \
            "Do you want to continue the process?"

        result = QMessageBox.warning(self.__ui.centralwidget,
                                     "Warning", text,
                                     QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.No:
            return

        # START WRITING
        blksize = self.__ui.comboBox_buffers.currentData()
        self.__copythread = WritingThread(self.__srcpath,
                                          device_item.object_path,
                                          self,
                                          blksize)
        self.__start_writing()

    def __start_writing(self):
        # SLOTS
        self.__copythread.signal.progressbar_value.connect(
            self.__ui.progressBar.setValue)
        self.__copythread.signal.statusbar_message.connect(
            self.__ui.statusbar.showMessage)
        self.__ui.pushButton_cancel.clicked.connect(
            self.signal.cancel_thread.emit)
        self.__copythread.finished.connect(
            self.__finished_writing)

        self.__ui.pushButton_open.setEnabled(False)
        self.__ui.comboBox_devices.setEnabled(False)
        self.__ui.comboBox_buffers.setEnabled(False)
        self.__ui.pushButton_write.setEnabled(False)
        self.__ui.statusbar.clearMessage()

        self.__copythread.start()

    def __finished_writing(self):
        self.__copythread.wait()
        self.__ui.pushButton_open.setEnabled(True)
        self.__ui.comboBox_devices.setEnabled(True)
        self.__ui.comboBox_buffers.setEnabled(True)
        self.__ui.pushButton_write.setEnabled(True)
