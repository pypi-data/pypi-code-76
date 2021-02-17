# -*- coding: utf-8 -*-
"""
=== Light Conversion EthMotorBoard API ===

This class can be used to control motors connected to the EthMotorBoard.

Before using this API:
    - Set the static IP address of the EthMotorBoard using the DIP switch
        matrix on the PCB. All boards and any other devices connected to the
        same network must have unique IP addresses.
    - Connect the EthMotorBoard to an Ethernet port on the computer. A
        dedicated USB to Ethernet adapter is recommended.
    - Power up the EthMotorBoard.
    - Configure the Ethernet adapter to use a static IP address 10.1.1.x,
        where x is anything from 1 to 255.

A detailed description of the commands can be found:
    http://nova/display/HAR/EthMotorBoard

Author: Vytautas Butkus, Lukas Kontenis
Contact: vytautas.butkus@lightcon.com, lukas.kontenis@lightcon.com
Copyright 2019-2020 Light Conversion
"""

import socket
import time


class EthMotorBoard:
    """Class to control EthMotorBoards."""
    BUFFER_SIZE = 1024
    sock = None
    connected = False
    name = None
    timeout = 100
    fv = None
    ip_address = None
    max_position = 2**21-1

    status_registers = [
        (0x01, 0x01, 'HiZ'), (0x02, 0x0, 'BUSY'), (0x04, 0x04, 'SW_F'),
        (0x08, 0x08, 'SW_ENV'), (0x60, 0x00, 'Stopped'),
        (0x60, 0x20, 'Acceleration'), (0x60, 0x40, 'Deceleration'),
        (0x60, 0x60, 'Constant speed'), (0x80, 0x80, 'NOTPERF_CMD'),
        (0x100, 0x100, 'WRONG_CMD'), (0x200, 0x0, 'OVLO'),
        (0x400, 0x0, 'TH_WRN'), (0x800, 0x0, 'TH_SD'), (0x1000, 0x0, 'OCD'),
        (0x2000, 0x0, 'STEP_LOSS_A'), (0x4000, 0x0, 'STEP_LOSS_B'),
        (0x8000, 0x8000, 'SCK_MOD')]

    ls_registers = [
        (0x01, 0x01, 'Left LS reached'), (0x02, 0x02, 'Right LS reached')]

    def __init__(self, ip_address='10.1.1.0'):
        self.ip_address = ip_address

        self.name = self.send('GET BOARD_NAME')
        self.fv = self.send('FIRMWARE_VERSION')

        self.connected = self.fv is not None

        if self.connected:
            print('Successfullly connected to {:}'.format(self.name)
                  + '(firmware version: {:})'.format(self.fv))
        else:
            print('Motor board not found at {:}'.format(self.ip_address))


    def send(self, message, args=None):
        """Send command to board and get a response.

        This should probably be called querry.
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout/1000)
            self.sock.connect((self.ip_address, 80))

            if args is None:
                self.sock.send((str(message)+'\r\n').encode('UTF-8'))
            else:
                self.sock.send((
                    str(message) + ' '
                    + ' '.join([str(arg) for arg in args])
                    + '\r\n').encode('UTF-8'))

            data = self.sock.recv(self.BUFFER_SIZE)
            self.sock.close()
            return data[:-2].decode()
        except socket.timeout:
            return None

    def get_status(self, motor_index=0):
        """Get board status."""
        status = int(self.send('GET STATUS', [motor_index]))
        ls_result = self.send('GET LIMIT_SWITCH', [motor_index])
        ls_status = eval(ls_result)['Logical']
        return [stat for mask, val, stat in self.status_registers if status & mask == val] \
            + [stat for mask, val, stat in self.ls_registers if ls_status & mask == val]

    def wait_until_stopped(self, motor_index=0):
        """Wait until motor stops."""
        repeat = True
        while repeat:
            status = self.send('GET STATUS ' + str(motor_index))
            repeat = int(status) & 0x60 != 0
            time.sleep(0.05)

    def get_abs_pos(self, motor_index=0):
        """Get absolute position in steps."""
        return self.send('GET ABS_POS ' + str(motor_index))

    def move_rel(self, motor_index=0, move_dir=0, pos_delta=0):
        """Move a given distance from the current position."""
        ret_code = self.send('MOVE {:d} {:d} {:d}'.format(
            motor_index, move_dir, pos_delta))

        self.check_error(ret_code)

    def move_abs(self, motor_index=0, abs_pos=0):
        """Move to relative position."""
        ret_code = self.send('GOTO {:d} {:d}'.format(motor_index, abs_pos))
        self.check_error(ret_code)

    def check_error(self, ret_code):
        """Check the return value.

        ERR0 means that everything is fine. ERR4 means that the limit switch
        has been reached. These two codes can be ignored in most cases.
        Anything else indicates an error.
        """
        ret_code = strip_whitespace(ret_code)

        if ret_code not in ['ERR0', 'ERR4']:
            print("Error: " + ret_code)

    def reset_motor(self, motor_index=0, move_dir=0, speed=10000):
        """Reset motor to limit switch and set position to 0."""
        ret_code = self.send('RUN {:d} {:d} {:d}'.format(
            motor_index, move_dir, speed))

        self.check_error(ret_code)
        self.wait_until_stopped(motor_index)
        ret_code = self.send('RESET_POS {:d}'.format(motor_index))
        self.check_error(ret_code)


# === Helper functions ===

def strip_whitespace(s):
    return s.translate(str.maketrans('', '', string.whitespace))
