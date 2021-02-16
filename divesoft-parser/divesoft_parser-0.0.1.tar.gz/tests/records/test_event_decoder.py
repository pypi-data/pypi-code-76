from divesoft_parser.decoders.records.event import EventRecordParser
from divesoft_parser.models.enums import DiveRecordType, EventRecordType, \
    DiveStartReason
from divesoft_parser.utilities import BitArray


def test_event_decoder_1():
    event = EventRecordParser(
        DiveRecordType.Manipulation,
        BitArray(bytes.fromhex('0100e0ff')),
        bytes.fromhex('05001500ffffffffffffffff'),
    ).decode()

    assert event.record_type == DiveRecordType.Manipulation
    assert event.event_type == EventRecordType.Mix_Changed
    assert event.o2 == 21
    assert event.when == 0


def test_event_decoder_2():
    event = EventRecordParser(
        DiveRecordType.Manipulation,
        BitArray(bytes.fromhex('0200e0ff')),
        bytes.fromhex('0600ffff01ffffffffffffff'),
    ).decode()

    assert event.record_type == DiveRecordType.Manipulation
    assert event.event_type == EventRecordType.Start
    assert event.reason == DiveStartReason.Manual
    assert event.when == 0


def test_event_decoder_3():
    event = EventRecordParser(
        DiveRecordType.Manipulation,
        BitArray(bytes.fromhex('e153e0ff')),
        bytes.fromhex('1200010000ffffffffffffff'),
    ).decode()

    assert event.record_type == DiveRecordType.Manipulation
    assert event.event_type == EventRecordType.Key_Down
    assert event.key1 is True
    assert event.key2 is False
    assert event.when == 1342


def test_event_decoder_4():
    event = EventRecordParser(
        DiveRecordType.Manipulation,
        BitArray(bytes.fromhex('410ae0ff')),
        bytes.fromhex('1a00010000ffffffffffffff'),
    ).decode()

    assert event.record_type == DiveRecordType.Manipulation
    assert event.event_type == EventRecordType.User_Mark
    assert event.when == 164


def test_event_decoder_5():
    event = EventRecordParser(
        DiveRecordType.Manipulation,
        BitArray(bytes.fromhex('b312e0ff')),
        bytes.fromhex('1e004e00ffffffffffffffff'),
    ).decode()

    assert event.record_type == DiveRecordType.Manipulation
    assert event.event_type == EventRecordType.CNS
    assert event.cns == 78
    assert event.when == 299


def test_event_decoder_6():
    event = EventRecordParser(
        DiveRecordType.Manipulation,
        BitArray(bytes.fromhex('0100e0ff')),
        bytes.fromhex('180015000100ffffffffffff'),
    ).decode()

    assert event.record_type == DiveRecordType.Manipulation
    assert event.event_type == EventRecordType.Change_Mode
    assert event.o2 == 21
    assert event.when == 0


def test_event_decoder_7():
    event = EventRecordParser(
        DiveRecordType.Manipulation,
        BitArray(bytes.fromhex('636ee0ff')),
        bytes.fromhex('0700ccf7ffffffffffffffff'),
    ).decode()

    assert event.record_type == DiveRecordType.Manipulation
    assert event.event_type == EventRecordType.Too_Fast
    assert event.when == 1766


def test_event_decoder_8():
    event = EventRecordParser(
        DiveRecordType.Manipulation,
        BitArray(bytes.fromhex('b30ae1ff')),
        bytes.fromhex('0800ffffffffffffffffffff'),
    ).decode()

    assert event.record_type == DiveRecordType.Manipulation
    assert event.event_type == EventRecordType.Above_Ceiling
    assert event.when == 4267


def test_event_decoder_9():
    event = EventRecordParser(
        DiveRecordType.Manipulation,
        BitArray(bytes.fromhex('036be0ff')),
        bytes.fromhex('0900ffffffffffffffffffff'),
    ).decode()

    assert event.record_type == DiveRecordType.Manipulation
    assert event.event_type == EventRecordType.Toxic
    assert event.when == 1712


def test_event_decoder_10():
    event = EventRecordParser(
        DiveRecordType.Manipulation,
        BitArray(bytes.fromhex('73d8e0ff')),
        bytes.fromhex('1400ffffffffffffffffffff'),
    ).decode()

    assert event.record_type == DiveRecordType.Manipulation
    assert event.event_type == EventRecordType.Above_Stop
    assert event.when == 3463


def test_event_decoder_11():
    event = EventRecordParser(
        DiveRecordType.Manipulation,
        BitArray(bytes.fromhex('03a4e0ff')),
        bytes.fromhex('1500ffffffffffffffffffff'),
    ).decode()

    assert event.record_type == DiveRecordType.Manipulation
    assert event.event_type == EventRecordType.Safety_Miss
    assert event.when == 2624
