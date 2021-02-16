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
import pathlib
from io import BytesIO

from divesoft_parser.decoders.header import DLFHeader
from divesoft_parser.decoders.record import DLFRecord
from divesoft_parser.models.dive import Dive

logger: logging.Logger = logging.getLogger(__name__)


class DLFDecoder:
    def __init__(self, bytes: BytesIO) -> None:
        self.bytes = bytes

    def _decode(self) -> Dive:
        dive = DLFHeader(self.bytes).decode()
        for _ in range(0, dive.dive_record_count):
            DLFRecord(self.bytes).decode_and_append(dive)
        return dive

    @staticmethod
    def from_bytes(raw_bytes: bytes) -> Dive:
        return DLFDecoder(BytesIO(raw_bytes))._decode()

    @staticmethod
    def from_file(file_path: str) -> Dive:
        if not pathlib.Path(file_path).is_file():
            raise ValueError(f"{file_path} is not a valid file")

        with open(file_path, "rb") as fh:
            return DLFDecoder(BytesIO(fh.read()))._decode()
