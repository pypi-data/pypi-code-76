"""
divesoft_parser - Divesoft DLF parser

MIT License

Copyright (c) 2021 Damian Zaremba

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import logging
from typing import Optional

from divesoft_parser.models.enums import MeasurementType, BatteryStats, DiveRecordType
from divesoft_parser.models.records.measurement import MeasurementBatteryRecord
from divesoft_parser.utilities import ByteConverter, BitArray

logger: logging.Logger = logging.getLogger(__name__)


class MeasurementRecordParser:
    def __init__(self, record_type: DiveRecordType,
                 bit_array: BitArray,
                 raw_bytes: bytes) -> None:
        self.record_type = record_type
        self.bit_array = bit_array
        self.record_data = raw_bytes
        if len(self.record_data) < 12:
            raise AssertionError(f"Truncated measurement record ({self.record_data.hex()})")

    def decode(self) -> Optional[MeasurementBatteryRecord]:
        try:
            measurement_type = MeasurementType(self.bit_array.get_int(21, 31))
        except ValueError:
            logger.warning(f'Skipping decoding of measurement record ({self.record_data.hex()})')
            return None

        if measurement_type == MeasurementType.Battery:
            return self._decode_battery_measurement()
        else:
            logger.error(f'Unknown measurement type: {measurement_type}')

    def _decode_battery_measurement(self) -> Optional[MeasurementBatteryRecord]:
        volt, percentage, status = None, None, None
        if self.record_data[0] != 255:
            volt = ByteConverter.to_uint16(self.record_data[0:2]) / 1000.00
            percentage = self.record_data[2]
            try:
                status = BatteryStats(ByteConverter.to_uint8(self.record_data[3:4]))
            except ValueError as e:
                logger.warning(f"Unknown battery status {e}")
                return

        return MeasurementBatteryRecord(
            when=self.bit_array.get_int(4, 21),
            record_type=self.record_type,
            measurement_type=MeasurementType.Battery,
            volt=volt,
            percentage=percentage,
            status=status,
        )
