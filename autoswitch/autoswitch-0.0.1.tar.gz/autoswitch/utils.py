from serial.tools import list_ports


def list_serial_ports():
    for port in list_ports.comports(True):
        print(port.device)


def get_default_serial_port() -> str:
    try:
        return list_ports.comports()[0].device
    except IndexError:
        # No comport
        return ""
