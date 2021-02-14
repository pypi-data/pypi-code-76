import sys
import dataclasses

import serial

import mp
import mp.micropythonshell
from mp.mpfshell import RemoteIOError
from mp.firmware.update import URL_README

FILENAME_IDENTIFICATION = mp.micropythonshell.FILENAME_IDENTIFICATION

@dataclasses.dataclass
class Identification:
    FILENAME: str
    READ_ERROR: str = None
    FILECONTENT: str = None
    HWTYPE: str = None
    HWVERSION: str = None
    HWSERIAL: str = None

    def print(self, indent='', f=sys.stdout):
        for field in dataclasses.fields(self):
            name = field.name
            value = getattr(self, name)
            if value == None:
                continue
            if value and '\n' in value:
                # Pretty print multiline as FILECONTENT
                fileindent = f'\r\n{indent}     '
                value = fileindent + fileindent.join(value.splitlines())
            print(f'{indent}{self.FILENAME}.{name}: {value}', file=f)


class Board:
    def __init__(self, port, mpfshell, identification):
        assert isinstance(port, serial.tools.list_ports_common.ListPortInfo)
        assert isinstance(mpfshell, (str, mp.micropythonshell.MicropythonShell))
        assert isinstance(identification, Identification)

        self.port = port
        self.mpfshell = mpfshell
        self.identification = identification
        self.micropython_sysname = self.mpfshell.MpFileExplorer.sysname
        self.micropython_release = self.mpfshell.MpFileExplorer.eval("uos.uname().release").decode("utf-8")
        self.micropython_machine = self.mpfshell.MpFileExplorer.eval("uos.uname().machine").decode("utf-8")

    def close(self):
        if isinstance(self.mpfshell, str):
            return
        if self.mpfshell.is_connected:
            self.mpfshell.close()

    @property
    def quickref(self):
        'returns "scanner_pyb_2020(pyboard/COM8)"'
        return f'{self.identification.HWTYPE}({self.micropython_sysname}/{self.port.name})'

    def systemexit_firmware_required(self, min: str=None, max: str=None):
        'Raise a exception if firmware does not fit requirements'
        fail = False
        text = self.micropython_release
        if min is not None:
            fail = fail or (min > self.micropython_release)
            text = f'{min}<={text}'
        if max is not None:
            fail = fail or (max < self.micropython_release)
            text = f'{text}<={max}'
        if fail:
            raise SystemExit(f'ERROR: {self.quickref} firmware {self.micropython_release} is installed, but {text} is required! To update see {URL_README}')

    def print(self, f=sys.stdout):
        print(f'    Board Query {self.port.name}', file=f)
        print(f'      pyserial.description: {self.port.description}', file=f)
        print(f'      pyserial.hwid: {self.port.hwid}', file=f)
        if isinstance(self.mpfshell, str):
            print(f'      mpfshell-error: {self.mpfshell}', file=f)
        else:
            print(f'      mpfshell.micropython_sysname: {self.micropython_sysname}', file=f)
            print(f'      mpfshell.micropython_release: {self.micropython_release}', file=f)
            print(f'      mpfshell.micropython_machine: {self.micropython_machine}', file=f)
        self.identification.print(indent='      ', f=f)


class BoardQueryBase:
    # Names to compare in pyboard()
    NAME_PYBOARD = 'pyboard'
    NAME_ESP32 = 'esp32'

    def __init__(self):
        self.board = None

    def select_pyserial(self, port):
        assert isinstance(port, serial.tools.list_ports_common.ListPortInfo)
        if self.select_pyserial_pyboard(port):
            return True
        if self.select_pyserial_esp32(port):
            return True
        if self.select_pyserial_espruino(port):
            return True
        # This hardware is unknown
        return False

    def select_pyserial_pyboard(self, port):
        # The usb chip used for the pyboard
        return (port.vid == 0xF055) and (port.pid == 0x9800)

    def select_pyserial_esp32(self, port):
        # The usb chip used for the esp32
        return (port.vid == 0x10C4) and (port.pid == 0xEA60)

    def select_pyserial_espruino(self, port):
        # The usb chip used for the espruino
        # The sysname of 'espruino' is 'pyboard'.
        return (port.vid == 0xF055) and (port.pid == 0x9800)

    def select_identification(self, identification):
        assert isinstance(identification, Identification)
        return True

    @classmethod
    def read_identification(cls, mpfshell):
        if isinstance(mpfshell, str):
            return Identification(READ_ERROR=mpfshell, FILENAME=FILENAME_IDENTIFICATION)
        try:
            source = mpfshell.MpFileExplorer.gets(src=FILENAME_IDENTIFICATION)
        except RemoteIOError as e:
            return Identification(READ_ERROR=str(e), FILENAME=FILENAME_IDENTIFICATION)
        globals = {}
        exec(source, globals)
        # Only take keys in uppercase
        # identification = {key:value for key, value in globals.items() if key.isupper()}
        identification = Identification(FILENAME=FILENAME_IDENTIFICATION, FILECONTENT=source)
        for key, value in globals.items():
            if not key.isupper():
                continue
            setattr(identification, key, value)
        return identification

    @classmethod
    def iter_pyserial(cls, query):
        assert isinstance(query, BoardQueryBase)
        for port in serial.tools.list_ports.comports():
            if query.select_pyserial(port):
                yield port

    @classmethod
    def iter_mpshell(cls, query):
        assert isinstance(query, BoardQueryBase)
        for port in cls.iter_pyserial(query):
            try:
                mpfshell = mp.micropythonshell.MicropythonShell(str_port=port.name)
            except Exception as e:
                yield port, str(e)
                continue
            yield port, mpfshell

    @classmethod
    def print_all(cls, f=sys.stdout):
        print('*** Board Query: scan', file=f)
        query = BoardQueryBase()
        boards = []
        try:
            for port, mpfshell in cls.iter_mpshell(query):
                identification = cls.read_identification(mpfshell)
                board = Board(port, mpfshell, identification)
                boards.append(board)

            print('*** Board Query: Micropython boards found:', file=f)
            for board in boards:
                board.print(f=f)
        finally:
            for board in boards:
                board.close()

    @classmethod
    def connect(cls, queries):
        assert isinstance(queries, list)
        queries = queries.copy()
        for port, mpfshell in cls.iter_mpshell(queries[0]):
            identification = cls.read_identification(mpfshell)
            for query in queries:
                if query.select_identification(identification):
                    query.board = Board(port, mpfshell, identification)
                    queries.remove(query)
            if len(queries) == 0:
                # All micropython boards found
                return True
        # board not found
        return False


class BoardQueryPyboard(BoardQueryBase):
    '''
    Selects pyboards with a 'config_identification.py' of given 'hwtype'
    '''
    def __init__(self, hwtype):
        super().__init__()
        self.hwtype = hwtype

    def select_pyserial(self, port):
        return self.select_pyserial_pyboard(port)

    def select_identification(self, identification):
        assert isinstance(identification, Identification)
        if self.hwtype is None:
            # We want to select any pyboard
            return True
        return identification.HWTYPE == self.hwtype


class BoardQueryComport(BoardQueryBase):
    '''
    Selects pyboards with a 'config_identification.py' of given 'hwtype'
    '''
    def __init__(self, comport):
        super().__init__()
        self.comport = comport

    def select_pyserial(self, port):
        return port.name.lower() == self.comport.lower()


def Connect(list_queries):
    found = BoardQueryBase.connect(list_queries)
    if not found:
        msg = f'Pyboards not found!'
        print(f'ERROR: {msg}')
        BoardQueryBase.print_all()
        raise Exception(msg)


def ConnectPyboard(hwtype):
    query = BoardQueryPyboard(hwtype)
    found = BoardQueryBase.connect([query])
    if not found:
        msg = f'Pyboard of HWTYPE={hwtype} not found!'
        print(f'ERROR: {msg}')
        BoardQueryBase.print_all()
        raise Exception(msg)
    return query.board


def ConnectComport(comport):
    query = BoardQueryComport(comport)
    found = BoardQueryBase.connect([query])
    if not found:
        msg = f'Pyboard with {comport} not found!'
        print(f'ERROR: {msg}')
        BoardQueryBase.print_all()
        raise Exception(msg)
    return query.board


def example_A():
    _board = ConnectComport('COM9')
    # This call will list a 'connected' com port.
    BoardQueryBase.print_all()


def example_B():
    print('start')
    scanner = BoardQueryPyboard('scanner_pyb_2020')
    compact = BoardQueryPyboard('compact_2012')
    Connect([compact, scanner])
    print('done')

def main():
    BoardQueryBase.print_all()

if __name__ == "__main__":
    main()
