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
from io import BytesIO

from divesoft_parser.decoders.records.configuration import ConfigurationRecordParser
from divesoft_parser.decoders.records.event import EventRecordParser
from divesoft_parser.decoders.records.measurement import MeasurementRecordParser
from divesoft_parser.decoders.records.point import PointRecordParser
from divesoft_parser.decoders.records.status import StatusRecordParser
from divesoft_parser.models.dive import Dive
from divesoft_parser.models.enums import DiveRecordType
from divesoft_parser.utilities import BitArray

logger: logging.Logger = logging.getLogger(__name__)


class DLFRecord:
    def __init__(self, bytes: BytesIO) -> None:
        raw_bytes = bytes.read(16)
        if len(raw_bytes) < 16:
            raise AssertionError(f"Truncated record ({raw_bytes.hex()})")
        self.bytes = BytesIO(raw_bytes)

    def decode_and_append(self, dive: Dive) -> None:  # noqa: C901
        bit_array = BitArray(self.bytes.read(4))

        try:
            record_type = DiveRecordType(bit_array.get_int(0, 4))
        except ValueError:
            logger.warning(f'Unknown record type: {bit_array.get_int(0, 4)}')
            return None

        if record_type == DiveRecordType.Point:
            point = PointRecordParser(record_type, bit_array, self.bytes.read()).decode()
            if point:
                dive.points.append(point)

        elif record_type == DiveRecordType.Measurement:
            record = MeasurementRecordParser(record_type, bit_array, self.bytes.read()).decode()
            if record:
                dive.records.append(record)

        elif record_type == DiveRecordType.Status:
            record = StatusRecordParser(record_type, bit_array, self.bytes.read()).decode()
            if record:
                dive.records.append(record)

        elif record_type in [
            DiveRecordType.Manipulation,
            DiveRecordType.Auto,
            DiveRecordType.Diver_Error,
            DiveRecordType.Internal_Error,
        ]:
            record = EventRecordParser(record_type, bit_array, self.bytes.read()).decode()
            if record:
                dive.records.append(record)

        elif record_type == DiveRecordType.Configuration:
            record = ConfigurationRecordParser(record_type, bit_array, self.bytes.read()).decode()
            if record:
                dive.records.append(record)

        else:
            logger.error(f'Unknown record type: {record_type}')
