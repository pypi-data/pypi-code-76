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

from divesoft_parser.models.enums import StatusType, DiveRecordType
from divesoft_parser.utilities import BitArray

logger: logging.Logger = logging.getLogger(__name__)


class StatusRecordParser:
    def __init__(self, record_type: DiveRecordType,
                 bit_array: BitArray,
                 raw_bytes: bytes) -> None:
        self.record_type = record_type
        self.bit_array = bit_array
        self.record_data = raw_bytes
        if len(self.record_data) < 12:
            raise AssertionError(f"Truncated status record ({self.record_data.hex()})")

    def decode(self) -> Optional[None]:
        try:
            status_type = StatusType(self.bit_array.get_int(21, 31))
        except ValueError:
            logger.warning(f'Skipping decoding of status record ({self.record_data.hex()})')
            return None

        if status_type == StatusType.Deco_N2_Low:
            return self._decode_deco_n2_low(status_type)

        elif status_type == StatusType.Deco_N2_High:
            return self._decode_deco_n2_high(status_type)

        else:
            logger.error(f'Unknown status type: {status_type}')

    def _decode_deco_n2_low(self, status_type: StatusType) -> None:
        # TODO: Figure out how these values are encoded
        # x-ref https://gist.github.com/DamianZaremba/3dad27c21be726c5340fa2c7ea3b95ae
        '''
        bf bf 11 bf bf 11 bf bf 11 bf bf 11
        Deco N2 Low, 0.8 bar, 0.8 bar,   0.8 bar, 0.8 bar,   0.8 bar, 0.8 bar,   0.8 bar, 0.8 bar
        '''
        logger.warning(f'Skipping decoding of decompression n2 low ({self.record_data.hex()})')
        return None

    def _decode_deco_n2_high(self, status_type: StatusType) -> None:
        # TODO: Figure out how these values are encoded
        # While the output is similar to the above with low/high being differentiated
        # by the 'header' bit array, the hex -> float does not appear to be the same e.g.
        '''
        cd c9 91 c7 c5 11 c4 c3 11 c2 c1 11
        Deco N2 High, 0.8 bar, 0.8 bar, 0.8 bar, 0.8 bar, 0.8 bar, 0.8 bar, 0.8 bar, 0.8 bar
        '''
        logger.warning(f'Skipping decoding of decompression n2 high ({self.record_data.hex()})')
        return None
