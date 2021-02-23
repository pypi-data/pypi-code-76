"""
Networking Functions
"""
import os
import netmiko
import pprint


def load_with_ssh(args):
    """
    Configures device with ssh
    """
    pass


def load_with_telnet(args):
    """
    Configures device with telnet
    """
    pass


def load_with_serial(args: dict):
    """
    Configures device with serial
    """

    device_config = {
        "device_type": "cisco_ios_serial",
        "username": args["username"],
        "password": args["password"],
        "secret": args["secret"],
        "serial_settings": {"port": args["port"],
                            "baudrate": args["baudrate"]}
    }

    with Device(**device_config) as device:
        device.load(args["load"])


class Device:
    def __init__(self, **kwargs) -> None:

        kwargs.update({"default_enter": "\n",
                       "global_delay_factor": 2})

        self.conn = netmiko.ConnectHandler(**kwargs)

        self.output = ""

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.conn.disconnect()

    def load(self, filename):
        """
        load config from txt file
        """
        self.conn.enable()
        self.output = self.conn.send_config_from_file(filename)
        print(self.output)
