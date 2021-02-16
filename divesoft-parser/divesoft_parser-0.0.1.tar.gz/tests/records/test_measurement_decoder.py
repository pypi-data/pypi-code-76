from divesoft_parser.decoders.records.measurement import MeasurementRecordParser
from divesoft_parser.models.enums import DiveRecordType, MeasurementType, BatteryStats
from divesoft_parser.utilities import BitArray


def test_measurement_decoder_1():
    measurement = MeasurementRecordParser(
        DiveRecordType.Measurement,
        BitArray(bytes.fromhex('27002080')),
        bytes.fromhex('04106402ffffff00ffffffff'),
    ).decode()

    assert measurement.measurement_type == MeasurementType.Battery
    assert measurement.status == BatteryStats.Discharging
    assert measurement.percentage == 100
    assert measurement.volt == 4.1
    assert measurement.when == 2
