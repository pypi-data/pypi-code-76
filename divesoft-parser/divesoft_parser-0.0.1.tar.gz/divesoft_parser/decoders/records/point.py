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

from divesoft_parser.models.enums import DiveRecordType
from divesoft_parser.models.records.point import PointRecord
from divesoft_parser.utilities import ByteConverter, BitArray

logger: logging.Logger = logging.getLogger(__name__)


class PointRecordParser:
    def __init__(self, record_type: DiveRecordType,
                 bit_array: BitArray,
                 raw_bytes: bytes) -> None:
        self.record_type = record_type
        self.bit_array = bit_array
        self.record_data = raw_bytes
        if len(self.record_data) < 12:
            raise AssertionError(f"Truncated point record ({self.record_data.hex()})")

    def decode(self) -> PointRecord:
        bit_array_2 = BitArray(self.record_data[4:8])
        return PointRecord(
            when=self.bit_array.get_int(4, 21),
            record_type=self.record_type,
            depth=ByteConverter.to_uint16(self.record_data[0:2]) / 100.00,
            ppo2=ByteConverter.to_uint16(self.record_data[2:4]) / 10000.00,
            no_deco_time=bit_array_2.get_int(0, 10) * 60,
            ascent_time=bit_array_2.get_int(10, 20) * 60,
            temperature=bit_array_2.get_int(20, 30) / 10.0,
            ceiling=ByteConverter.to_uint16(self.record_data[8:10]) / 100.0,
            he=self.record_data[10],
        )
