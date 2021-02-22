import serial

ser = None

def open_fpga(port, baud = None):
    global ser

    if baud == None:
        baud = 1000000
    ser = serial.Serial(port, baud, timeout=2.0)
    return ser

def call_fpga(size, count):
    global ser

    if not ser:
        raise Exception('FPGA I/O not open')

    ser.write(b' ')
    buf = bytearray()
    for i in range(count):
        x = ser.read(size)
        if len(x) == size:
            buf.extend(x)
        else:
            break
    return bytes(buf)

def close_fpga():
    if ser:
        ser.close()
