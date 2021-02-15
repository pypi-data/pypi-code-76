import pytest
import time
import threading
import queue

from spintop_openhtf.plugs.comport import ComportInterface, IOTargetTimeout

class FakeSerial(object):
    def __init__(self):
        self.to_read = ""
        self.is_open = True
        self.in_waiting = False
        self.echo = True
        self.was_read = threading.Event()

    def close(self):
        self.is_open = False

    def read(self, *args, **kwargs):
        if self.to_read:
            value = self.to_read
            self.to_read = ""
            self.in_waiting = False
            self.was_read.set()
            return value.encode('utf8')
        else:
            time.sleep(0.5)
            return None
    
    def write(self, string):
        if self.echo:
            self.in_waiting = True
            self.to_read += string.decode('utf8')

@pytest.fixture()
def fake_serial():
    fake_serial = FakeSerial()
    return fake_serial

@pytest.fixture()
def comport(fake_serial):
    # comport = ComportInterface('/dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_ComPort_in_FS_Mode_00000000050C-if00', 115200)
    comport = ComportInterface(None, None)
    comport.open(fake_serial)
    yield comport
    comport.close()


def test_receive_no_eol(fake_serial, comport):
    comport.write('Hello')
    line = comport.next_line(timeout=2)
    assert line == 'Hello'

def test_receive_immediate_eol(fake_serial, comport):
    fake_serial.was_read.clear()
    comport.write('Hello\n')
    # no wait now (only enough time for the thread to call read)
    fake_serial.was_read.wait()
    assert comport.next_line(timeout=0.1) == 'Hello\n'

def test_multi_lines(fake_serial, comport):
    fake_serial.was_read.clear()
    LINES = ('0\n', '1\n', '2\n')

    for line in LINES:
        comport.write(line)

    fake_serial.was_read.wait()

    for line in LINES:
        assert comport.next_line(timeout=0.1) == line


def test_keep_lines(fake_serial, comport):
    comport.write('0\n')
    comport.write('1\n')
    comport.write('2\n')

    fake_serial.was_read.wait()
    time.sleep(0.1)
    comport.keep_lines(1)

    assert comport.next_line(timeout=0.1) == '2\n'
    

def test_keep_lines_0(fake_serial, comport):
    comport.write('0\n')
    comport.write('1\n')
    comport.write('2\n')

    fake_serial.was_read.wait()
    time.sleep(0.1)
    comport.keep_lines(0)

    assert comport.next_line(timeout=0.1) is None

def test_clear(fake_serial, comport):
    comport.write('0\n')
    comport.clear_lines()

    assert comport.next_line(timeout=0.1) is None

def test_message_target(fake_serial, comport):
    def write_future():
        for i in (1,2,3):
            time.sleep(0.2)
            comport.write('line%d' % i)
    
    thread = threading.Thread(target=write_future)
    thread.start()
    response = comport.message_target('hello\n', 'line3')

    assert response == 'hello\nline1line2line3'
    
def test_message_target_timeout(fake_serial, comport):
    start = time.time()
    with pytest.raises(IOTargetTimeout):
        response = comport.message_target('hello\n', 'line3', timeout=0.2)

    delta = time.time() - start
    assert delta < 0.5, f'Timeout is 0.2s, message_target took {delta}'

def test_message_target_timeout_no_message(fake_serial, comport):
    start = time.time()
    with pytest.raises(IOTargetTimeout):
        response = comport.message_target('', 'something-that-wont-happen', timeout=0.2)

    delta = time.time() - start
    assert delta < 0.5, f'Timeout is 0.2s, message_target took {delta}s'