from pathlib import Path

from divesoft_parser import DLFDecoder
from divesoft_parser.models.enums import DiveRecordType, MeasurementType, BatteryStats, EventRecordType
from divesoft_parser.models.records.event import EventKeyRecord, EventMixChangeRecord
from divesoft_parser.models.records.measurement import MeasurementBatteryRecord
from divesoft_parser.models.records.point import PointRecord


def test_header_decoder_1():
    path = Path(__file__).parent / 'sample.DLF'
    dive = DLFDecoder.from_file(path.as_posix())

    assert dive.mode.name == "OC"
    assert dive.log_number == 170
    assert dive.dive_day_number == 1
    assert dive.dive_record_count == 1088
    assert dive.max_depth == 41.06
    assert dive.test is False
    assert dive.no_deco is False
    assert dive.duration == 3945
    assert dive.min_temperature == 7.2

    assert MeasurementBatteryRecord(
        when=2,
        record_type=DiveRecordType.Measurement,
        measurement_type=MeasurementType.Battery,
        volt=4.173,
        percentage=99,
        status=BatteryStats.Discharging,
    ) in dive.records

    assert MeasurementBatteryRecord(
        when=3902,
        record_type=DiveRecordType.Measurement,
        measurement_type=MeasurementType.Battery,
        volt=4.111,
        percentage=97,
        status=BatteryStats.Discharging,
    ) in dive.records

    assert EventKeyRecord(
        when=2611,
        record_type=DiveRecordType.Manipulation,
        event_type=EventRecordType.Key_Down,
        key1=True,
        key2=True,
    ) in dive.records

    assert EventMixChangeRecord(
        when=2631,
        record_type=DiveRecordType.Manipulation,
        event_type=EventRecordType.Mix_Changed,
        o2=50,
        he=0,
    ) in dive.records

    assert EventKeyRecord(
        when=2612,
        record_type=DiveRecordType.Manipulation,
        event_type=EventRecordType.Key_Down,
        key1=True,
        key2=False,
    ) in dive.records

    assert PointRecord(
        when=1,
        record_type=DiveRecordType.Point,
        depth=1.58,
        ppo2=0.2474,
        no_deco_time=60000,
        ascent_time=0,
        temperature=14.6,
        ceiling=0.0,
        he=0,
    ) in dive.points

    assert PointRecord(
        when=1417,
        record_type=DiveRecordType.Point,
        depth=40.04,
        ppo2=1.0615,
        no_deco_time=0,
        ascent_time=360,
        temperature=7.2,
        ceiling=4.7,
        he=0,
    ) in dive.points
