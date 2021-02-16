from divesoft_parser.decoders.records.point import PointRecordParser
from divesoft_parser.models.enums import DiveRecordType
from divesoft_parser.utilities import BitArray


def test_point_decoder_1():
    point = PointRecordParser(
        DiveRecordType.Point,
        BitArray(bytes.fromhex('0000e0ff')),
        bytes.fromhex('7601cf07e803c0cd00000000'),
    ).decode()

    assert point.depth == 3.74
    assert point.ceiling == 0.0
    assert point.ppo2 == 0.1999
    assert point.when == 0


def test_point_decoder_2():
    point = PointRecordParser(
        DiveRecordType.Point,
        BitArray(bytes.fromhex('e80360cb')),
        bytes.fromhex('ca004a0ae80360cb00000000'),
    ).decode()

    assert point.depth == 2.02
    assert point.ceiling == 0.0
    assert point.ppo2 == 0.2634
    assert point.when == 62


def test_point_decoder_3():
    point = PointRecordParser(
        DiveRecordType.Point,
        BitArray(bytes.fromhex('e80330cb')),
        bytes.fromhex('a900040ae80330cb00000000'),
    ).decode()

    assert point.depth == 1.69
    assert point.ceiling == 0.0
    assert point.ppo2 == 0.2564
    assert point.when == 65598
