import os
import pytest
import tempfile
import shutil

from mock import MagicMock
from spintop_openhtf.plugs.visa import VISAInterface

class InstrumentMock(object):
    timeout = 5000

    def query(self, cmd):
        pass

    def read(self):
        pass

    def write(self, cmd):
        pass

    def write_binary_values(self, cmd, values, datatype=None):
        pass

    def query_binary_values(self, cmd, datatype=None):
        pass

@pytest.fixture()
def instrument_mock():
    return MagicMock(spec=InstrumentMock)

@pytest.fixture()
def interface(instrument_mock):
    interface = VISAInterface()
    interface.open(_instrument=instrument_mock)
    return interface

@pytest.fixture()
def temp_filename():
    TEMP_FOLDER = tempfile.mkdtemp()
    try:
        yield os.path.join(TEMP_FOLDER, 'destination.txt')
    finally:
        shutil.rmtree(TEMP_FOLDER)

def test_execute_command(interface, instrument_mock):
    READ_VALUE = 'Hello'
    instrument_mock.read.return_value = READ_VALUE
    
    read_value = interface.execute_command('write', doread=True)

    assert read_value == READ_VALUE
    instrument_mock.write.assert_called_with('write')

def test_wait_for_command_end(interface, instrument_mock):
    """Should query '*OPC?' when execute_command called without doread."""
    
    interface.execute_command('write')
    instrument_mock.write.assert_called_with('write')
    instrument_mock.query.assert_called_with('*OPC?')

def test_timeout_is_set_ms(interface, instrument_mock):
    TIMEOUT_S = 29
    interface.execute_command('write', timeout=TIMEOUT_S)

    assert instrument_mock.timeout == TIMEOUT_S*1000

def test_read_file(interface, instrument_mock, temp_filename):
    CONTENT = b'something'
    instrument_mock.query_binary_values.return_value = CONTENT

    interface.read_binary_file('command', temp_filename)

    instrument_mock.query_binary_values.assert_called_with('command', datatype='c')

    with open(temp_filename, 'rb') as written_file:
        assert written_file.read() == CONTENT

def test_write_file(interface, instrument_mock, temp_filename):
    CONTENT = b'something'

    with open(temp_filename, 'wb') as file_to_write:
        file_to_write.write(CONTENT)
    
    interface.write_binary_file('command', temp_filename)

    instrument_mock.write_binary_values.assert_called_with('command', list(CONTENT), datatype='c')

def test_reset(interface, instrument_mock):
    """Should send '*RST' and then query '*OPC?'"""

    interface.reset()

    instrument_mock.write.assert_called_with('*RST')
    instrument_mock.query.assert_called_with('*OPC?')

