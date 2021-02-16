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
from dataclasses import dataclass
from datetime import datetime
from typing import List, Union

from divesoft_parser.models.enums import DiveMode
from divesoft_parser.models.records.event import (EventChangeModeRecord,
                                                  EventCnsRecord,
                                                  EventKeyRecord,
                                                  EventMixChangeRecord,
                                                  EventStartRecord,
                                                  EventUserMarkRecord,
                                                  EventOccurrenceRecord)
from divesoft_parser.models.records.measurement import MeasurementBatteryRecord
from divesoft_parser.models.records.point import PointRecord


@dataclass(repr=True, frozen=True)
class Dive:
    log_number: int
    dive_day_number: int
    date: datetime
    duration: int
    no_deco: bool
    mode: DiveMode
    test: bool
    dive_record_count: int
    min_temperature: float
    max_depth: float
    otu: int
    records: List[Union[EventChangeModeRecord,
                        EventCnsRecord,
                        EventKeyRecord,
                        EventMixChangeRecord,
                        EventStartRecord,
                        EventUserMarkRecord,
                        EventOccurrenceRecord,
                        MeasurementBatteryRecord]]
    points: List[PointRecord]
