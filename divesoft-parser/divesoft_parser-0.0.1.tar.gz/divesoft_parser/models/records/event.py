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

from divesoft_parser.models.enums import (DiveMode,
                                          DiveRecordType,
                                          EventRecordType,
                                          DiveStartReason)


@dataclass(frozen=True, repr=True)
class EventMixChangeRecord:
    when: int
    record_type: DiveRecordType
    event_type: EventRecordType
    o2: int
    he: int


@dataclass(frozen=True, repr=True)
class EventStartRecord:
    when: int
    record_type: DiveRecordType
    event_type: EventRecordType
    reason: DiveStartReason


@dataclass(frozen=True, repr=True)
class EventKeyRecord:
    when: int
    record_type: DiveRecordType
    event_type: EventRecordType
    key1: bool
    key2: bool


@dataclass(frozen=True, repr=True)
class EventChangeModeRecord:
    when: int
    record_type: DiveRecordType
    event_type: EventRecordType
    o2: int
    he: int
    measured: bool
    mode: DiveMode


@dataclass(frozen=True, repr=True)
class EventUserMarkRecord:
    when: int
    record_type: DiveRecordType
    event_type: EventRecordType
    order: int
    category: int


@dataclass(frozen=True, repr=True)
class EventCnsRecord:
    when: int
    record_type: DiveRecordType
    event_type: EventRecordType
    cns: int


@dataclass(frozen=True, repr=True)
class EventOccurrenceRecord:
    when: int
    record_type: DiveRecordType
    event_type: EventRecordType
