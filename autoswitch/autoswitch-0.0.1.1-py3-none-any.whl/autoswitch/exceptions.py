import os
import argparse

from serial.tools import list_ports


def comport(string: str) -> str:
    """
    Argparse Type: Comport
    """

    for port in list_ports.comports():
        if string == port.device:
            return string

    raise argparse.ArgumentTypeError(f"{string}: is not a valid COM port")
