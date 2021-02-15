import pytest
from mock import MagicMock
import paramiko

from spintop_openhtf.plugs.ssh import SSHInterface


ADDR = 'x'
USER = 'y'
PASS = 'z'
TIMEOUT = 23

def test_ssh_client_created():
    ssh_interface = SSHInterface(ADDR, USER, PASS, create_timeout=TIMEOUT)
    ssh_client_mock = MagicMock(paramiko.SSHClient)
    ssh_interface.open(ssh_client_mock)

    assert isinstance(ssh_client_mock.set_missing_host_key_policy.call_args[0][0], paramiko.AutoAddPolicy)
    ssh_client_mock.connect.assert_called_with(ADDR, port=22, username=USER, password=PASS, timeout=TIMEOUT)

def test_ssh_client_close_works():
    ssh_interface = SSHInterface(ADDR, USER, PASS, create_timeout=TIMEOUT)
    ssh_client_mock = MagicMock(paramiko.SSHClient)
    ssh_interface.open(ssh_client_mock)
    ssh_interface.close()

    ssh_client_mock.close.assert_called_once()



