'''
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
'''
import dataclasses
import datetime
import json
import logging
from enum import Enum
from typing import Optional, List

from divesoft_parser.models.dive import Dive

logger: logging.Logger = logging.getLogger(__name__)


class ByteConverter:
    @staticmethod
    def to_int8(data: bytes) -> int:
        """Convert 1 byte into an un-signed 8bit integer."""
        if len(data) != 1:
            raise ValueError(f"to_int8 requires one bytes ({data})")
        return data[0]

    @staticmethod
    def to_bool(data: bytes) -> bool:
        """Convert 1 byte into a bool."""
        if len(data) != 1:
            raise ValueError(f"to_bool requires one bytes ({data})")
        return bool(data[0])

    @staticmethod
    def to_uint8(data: bytes) -> int:
        """Convert 1 byte into a signed 8bit integer."""
        if len(data) != 1:
            raise ValueError(f"to_uint8 requires one bytes ({data})")
        return data[0] & 255

    @staticmethod
    def to_int16(data: bytes) -> int:
        """Convert 2 bytes into a signed 16bit integer."""
        if len(data) != 2:
            raise ValueError(f"to_int16 requires two bytes ({data})")
        return (data[1] << 8) | (data[0] & 255)

    @staticmethod
    def to_uint16(data: bytes) -> int:
        """Convert 2 bytes into an un-signed 16bit integer."""
        if len(data) != 2:
            raise ValueError(f"to_uint16 requires two bytes ({data})")
        return ((data[1] & 255) << 8) | (data[0] & 255)

    @staticmethod
    def to_int32(data: bytes) -> int:
        """Convert 4 bytes into a signed 32bit integer."""
        if len(data) != 4:
            raise ValueError(f"to_int32 requires four bytes ({data})")
        return (data[3] << 24 |
                (data[2] & 255) << 16 |
                (data[1] & 255) << 8 |
                (data[0] & 255))

    @staticmethod
    def to_uint32(data: bytes) -> int:
        """Convert 4 bytes into an un-signed 32bit integer."""
        if len(data) != 4:
            raise ValueError(f"to_uint32 requires four bytes ({data})")
        return ((data[3] & 255) << 24 |
                (data[2] & 255) << 16 |
                (data[1] & 255) << 8 |
                (data[0] & 255))


class BitArray:
    """Create a bit array from a byte sequence"""

    def __init__(self, byteArray: bytes) -> None:
        self._bits: List[bool] = []
        for byte in byteArray:
            for bitOffset in (0, 1, 2, 3, 4, 5, 6, 7):
                self._bits.append(bool(byte & (1 << bitOffset)))

    def get_int(self, start_offset: int, end_offset: Optional[int] = None) -> int:
        """Return the an int using bits from offset X-Y."""
        if end_offset is None:
            end_offset = start_offset + 1

        if len(self._bits) < end_offset:
            raise ValueError(f"Ran out of bits for offset {end_offset} ({self._bits})")

        num = 0
        for i in range(start_offset, end_offset):
            if self._bits[i]:
                num |= 1 << (i - start_offset)
        return num

    def get_bit(self, offset: int) -> int:
        """Return the bit at offset N."""
        if len(self._bits) < offset:
            raise ValueError(f"BitArray ran out of bits for offset {offset}")

        return self._bits[offset]


class ExtendedDiveEncoder(json.JSONEncoder):
    """Helper encoder for internal types."""

    # pyre-ignore
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, (datetime.datetime,)):
            return o.isoformat()
        if isinstance(o, (Enum,)):
            return o.name
        return super().default(o)


def convert_to_json(dive: Dive) -> str:
    """Export a dive as string."""
    return json.dumps(dive, cls=ExtendedDiveEncoder, indent=4, sort_keys=True)
