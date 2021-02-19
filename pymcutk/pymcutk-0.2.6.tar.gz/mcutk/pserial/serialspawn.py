import io
import logging
import pexpect
from pexpect.spawnbase import SpawnBase


class SerialSpawn(SpawnBase):
    """Due to pyserial not support file descriptor for windows, fdspawn could not be used.
    This class implement a spawn for pyserial, all interfaces are defined from the base
    `SpawnBase`. For more information about the usage, please refer the pexpect documentation.

    Note: logfile_read detault is used in it's internal.

    Simple example:
        >>> from mcutk.pserial import Serial
        >>> ser = Serial('COM3', 9600)
        >>> spawn = ser.SerialSpawn()
        >>> spawn.logfile = sys.stdout
        >>> spawn.write_expect("Waiting for power mode select..", timeout=3)
        >>> print spawn.before
        >>> print spawn.after
        >>> spawn.close()
        >>> print ser.data
    """
    def __init__(self, serial, searchwindowsize=None,
                 logfile=None, logfile_read=None, encoding=None,
                 codec_errors='strict', open_port=True):
        """
        Arguments:
            serial: {serial.Serial object}
            open_port: {boolean} open port if it is not open, default True
        """

        if not serial.is_open and open_port:
            serial.open()

        if hasattr(serial, 'reader_isalive'):
            if serial.reader_isalive:
                serial.stop_reader()
                logging.debug('reader thread is stopped!')

        self.serial = serial
        self.serial.timeout = 0.3
        super(SerialSpawn, self).__init__(
            timeout=3,
            searchwindowsize=searchwindowsize,
            logfile=logfile,
            encoding=encoding,
            codec_errors=codec_errors
        )

        self.logfile_read = logfile_read
        self.closed = not self.serial.is_open

    def read_nonblocking(self, size=1, timeout=None):
        """This is fake nonblocking, the size is decided by how many data in the buffer, rather than
        specific value, this is because big size will block the serial read, small size will effect the
        performance when many data in buffer. timeout is useless.
        """
        raw = self.serial.read(self.serial.in_waiting or 1)
        self._log(raw, 'read')
        str_data = self._decoder.decode(raw, final=False)
        return str_data

    def send(self, s):
        """Send data to serial, and logging to log_send."""
        s = self._coerce_send_string(s)
        self._log(s, 'send')
        b = self._encoder.encode(s, final=False)
        return self.serial.write(b)

    def sendline(self, s):
        """Send line"""
        s = self._coerce_send_string(s)
        return self.send(s + self.linesep)

    def write(self, s):
        self.send(s)

    def writelines(self, sequence):
        for s in sequence:
            self.write(s)

    def flush(self):
        self.serial.flush()

    def flush_log(self):
        """Flush logfile_read to a readable attribute: SerialSpawn.data"""

        if hasattr(self.serial, 'append_data') and isinstance(self.logfile_read, io.BytesIO):
            logging.debug("dump reading log to serial object!")
            self.logfile_read.seek(0)
            data = self.logfile_read.read()
            self.serial.append_data(data)
            # clear io.Bytes file object
            self.logfile_read.seek(0)
            self.logfile_read.truncate()

    def find(self, pattern, timeout=30):
        """Return the matches of pattern within a specific timeout
        in the serial reading stream. If EOF, return value is None.

        If timeout occured, that will raise pexpect.TIMEOUT exception.
        """
        try:
            self.expect(pattern, timeout=timeout)
            return self.before + self.after
        except pexpect.EOF:
            return None

    def test_input(self, input, expect, timeout=30):
        """Input value to serial, and test the output if match the expectation.

        Arguments:
            input {str} -- input string
            expect {str} -- pattern
            timeout {float} -- timeout in seconds

        Returns:
            str -- the output
        """
        self.write(input)
        self.expect(expect, timeout=timeout)
        self.flush_log()

        return self.before + self.after

    def close(self):
        """Close serial port, and dump the logfile_read to mcutk.pserial.Serial.data.
        If the serial instance is comes from pyserial, dump action will not take.
        """
        self.serial.close()
        self.flush_log()
        self.closed = True

    def isalive(self):
        """Return a boolean the port is open or not
        """
        return self.serial.is_open
