from serial.tools import list_ports


def list_serial_ports():
    for port in list_ports.comports(True):
        print(port.device)
    if len(list_ports.comports(True)) == 0:
        print("No comports to list")
