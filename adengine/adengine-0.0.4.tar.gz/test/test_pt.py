import pytest
import os
import unittest.mock as mock
import tempfile

from adengine.pt import *

from test import TEST_DATA, USE_VIRTUAL_DISPLAY, READ_FILE_TIMEOUT


@pytest.fixture(scope='module')
def launch_packet_tracer_session():
    session = PacketTracerSession(use_virtual_display=USE_VIRTUAL_DISPLAY)
    session.start()
    yield session
    session.stop()


@pytest.mark.parametrize(
    ['filepath', 'password'],
    [
        pytest.param(
            os.path.join(TEST_DATA, 'with_password.pka'), '123', id='with_password'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'without_password.pka'), None, id='without_password'
        ),
    ]
)
def test_extract_data(filepath, password, launch_packet_tracer_session):
    extract_data(launch_packet_tracer_session, filepath, password, READ_FILE_TIMEOUT)


@pytest.mark.parametrize(
    ['filepath', 'password', 'exception'],
    [
        pytest.param(
            os.path.join(TEST_DATA, 'no_such_file.pka'), None, ActivityFileReadingError, id='ActivityFileReadingError'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'with_password.pka'), 1234, WrongPassword, id='WrongPassword'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'with_password.pka'), None, ActivityNeedsPassword, id='ActivityNeedsPassword'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'topology.pkt'), None, TopologyFilesNotSupported, id='TopologyFilesNotSupported'
        ),
    ]
)
def test_extract_data_exceptions(filepath, password, exception, launch_packet_tracer_session):
    with pytest.raises(exception):
        extract_data(launch_packet_tracer_session, filepath, password, READ_FILE_TIMEOUT)


def test_connection_failed(launch_packet_tracer_session):
    with mock.patch('adengine.pt.PacketTracerSession.port', new_callable=lambda: 80):
        with pytest.raises(ConnectionFailed):
            extract_data(launch_packet_tracer_session, os.path.join(TEST_DATA, 'without_password.pka'), None,
                         READ_FILE_TIMEOUT)


@pytest.mark.parametrize(
    ['filepath', 'password', 'net_stabilization_delay', 'total_percentage'],
    [
        pytest.param(
            os.path.join(TEST_DATA, 'with_net_stabilization_delay_small.pka'), '123', 0, 0.0, id='small'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'with_net_stabilization_delay_big.pka'), '123', 20, 97.0, id='big'
        ),
    ]

)
def test_net_stabilization_delay(launch_packet_tracer_session, filepath, password, net_stabilization_delay,
                                 total_percentage):
    data = extract_data(launch_packet_tracer_session, filepath, password, READ_FILE_TIMEOUT, net_stabilization_delay)
    assert abs(data['totalPercentage'] - total_percentage) < 1.0


def test_extract_corrupted_file(launch_packet_tracer_session):
    with tempfile.NamedTemporaryFile() as temp_file:
        with pytest.raises(ActivityFileReadingError):
            extract_data(launch_packet_tracer_session, temp_file.name, 'test_password', READ_FILE_TIMEOUT)
