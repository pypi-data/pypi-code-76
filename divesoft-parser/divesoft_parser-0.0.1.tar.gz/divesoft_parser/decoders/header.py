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
from datetime import datetime
from io import BytesIO

from ..models.dive import DiveMode, Dive
from ..utilities import ByteConverter, BitArray

logger: logging.Logger = logging.getLogger(__name__)


class DLFHeader:
    def __init__(self, bytes: BytesIO) -> None:
        raw_bytes = bytes.read(32)
        if len(raw_bytes) < 32:
            raise AssertionError(f"Truncated header ({raw_bytes.hex()})")
        self.bytes = BytesIO(raw_bytes)

    def decode(self) -> Dive:
        header_marker = self.bytes.read(4)
        if header_marker != b"DivE":
            raise AssertionError(f"Header missing marker ({header_marker})")
        self.bytes.read(2)  # ?
        log_number = ByteConverter.to_uint16(self.bytes.read(2))
        start_time = datetime.utcfromtimestamp(
            946684800 + ByteConverter.to_uint32(self.bytes.read(4))
        )

        bit_array_1 = BitArray(self.bytes.read(4))

        duration = bit_array_1.get_int(0, 17)
        no_deco = bool(bit_array_1.get_int(24))
        dive_mode = DiveMode(bit_array_1.get_int(27, 30))
        test = not bit_array_1.get_int(31)

        bit_array_2 = BitArray(self.bytes.read(4))
        dive_record_count = bit_array_2.get_int(0, 18)
        min_temperature = bit_array_2.get_int(18, 28) / 10.0
        dive_day_number = bit_array_2.get_int(28, 32) + 1
        max_depth = ByteConverter.to_uint16(self.bytes.read(2)) / 100.0
        otu = ByteConverter.to_uint16(self.bytes.read(2))

        return Dive(
            log_number=log_number,
            dive_day_number=dive_day_number,
            date=start_time,
            duration=duration,
            no_deco=no_deco,
            mode=dive_mode,
            test=test,
            dive_record_count=dive_record_count,
            min_temperature=min_temperature,
            max_depth=max_depth,
            otu=otu,
            records=[],
            points=[],
        )
