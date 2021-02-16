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
from typing import Optional, Union

from divesoft_parser.models.dive import DiveMode
from divesoft_parser.models.enums import DiveStartReason, DiveRecordType
from divesoft_parser.models.records.event import (EventRecordType,
                                                  EventMixChangeRecord,
                                                  EventStartRecord,
                                                  EventChangeModeRecord,
                                                  EventKeyRecord,
                                                  EventUserMarkRecord,
                                                  EventCnsRecord,
                                                  EventOccurrenceRecord)
from divesoft_parser.utilities import ByteConverter, BitArray

logger: logging.Logger = logging.getLogger(__name__)


class EventRecordParser:
    def __init__(self, record_type: DiveRecordType,
                 bit_array: BitArray,
                 raw_bytes: bytes) -> None:
        self.record_type = record_type
        self.bit_array = bit_array
        self.record_data = raw_bytes
        if len(self.record_data) < 12:
            raise AssertionError(f"Truncated event record ({self.record_data.hex()})")

    def decode(self) -> Union[None,
                              EventMixChangeRecord,
                              EventStartRecord,
                              EventKeyRecord,
                              EventUserMarkRecord,
                              EventCnsRecord,
                              EventOccurrenceRecord,
                              EventChangeModeRecord]:
        try:
            event_type = EventRecordType(ByteConverter.to_uint16(self.record_data[0:2]))
        except ValueError:
            logger.warning(f'Skipping decoding of event record ({self.record_data.hex()})')
            return

        if event_type == EventRecordType.Mix_Changed:
            return self._decode_event_mix_changed()

        elif event_type == EventRecordType.Start:
            return self._decode_event_start()

        elif event_type in [
            EventRecordType.Too_Fast,
            EventRecordType.Above_Ceiling,
            EventRecordType.Toxic,
            EventRecordType.Above_Stop,
            EventRecordType.Safety_Miss,
        ]:
            return self._decode_event_occurrence(event_type)

        elif event_type == EventRecordType.Key_Down:
            return self._decode_event_key()

        elif event_type == EventRecordType.Change_Mode:
            return self._decode_event_mode_change()

        elif event_type == EventRecordType.User_Mark:
            return self._decode_event_user_mark()

        elif event_type == EventRecordType.CNS:
            return self._decode_event_cns()

        else:
            logger.error(f"Unknown event type: {event_type}")

    def _decode_event_mode_change(self) -> Optional[EventChangeModeRecord]:
        try:
            dive_mode = DiveMode(ByteConverter.to_uint8(self.record_data[4:5]))
        except ValueError as e:
            logger.error(f"Unknown dive mode: {e}")
            return

        return EventChangeModeRecord(
            when=self.bit_array.get_int(4, 21),
            record_type=self.record_type,
            event_type=EventRecordType.Change_Mode,
            o2=ByteConverter.to_uint8(self.record_data[2:3]),
            he=ByteConverter.to_uint8(self.record_data[3:4]),
            measured=ByteConverter.to_bool(self.record_data[5:6]),
            mode=dive_mode,
        )

    def _decode_event_user_mark(self) -> EventUserMarkRecord:
        return EventUserMarkRecord(
            when=self.bit_array.get_int(4, 21),
            record_type=self.record_type,
            event_type=EventRecordType.User_Mark,
            order=ByteConverter.to_uint16(self.record_data[2:4]),
            category=ByteConverter.to_uint8(self.record_data[4:5]),
        )

    def _decode_event_cns(self) -> EventCnsRecord:
        return EventCnsRecord(
            when=self.bit_array.get_int(4, 21),
            record_type=self.record_type,
            event_type=EventRecordType.CNS,
            cns=ByteConverter.to_uint8(self.record_data[2:3]),
        )

    def _decode_event_key(self) -> EventKeyRecord:
        return EventKeyRecord(
            when=self.bit_array.get_int(4, 21),
            record_type=self.record_type,
            event_type=EventRecordType.Key_Down,
            key1=ByteConverter.to_bool(self.record_data[2:3]),
            key2=ByteConverter.to_bool(self.record_data[3:4]),
        )

    def _decode_event_start(self) -> Optional[EventStartRecord]:
        try:
            reason = DiveStartReason(ByteConverter.to_uint8(self.record_data[1:2]))
        except ValueError as e:
            logger.error(f"Unknown start reason {e}")
            return

        return EventStartRecord(
            when=self.bit_array.get_int(4, 21),
            record_type=self.record_type,
            event_type=EventRecordType.Start,
            reason=reason,
        )

    def _decode_event_mix_changed(self) -> EventMixChangeRecord:
        return EventMixChangeRecord(
            when=self.bit_array.get_int(4, 21),
            record_type=self.record_type,
            event_type=EventRecordType.Mix_Changed,
            o2=ByteConverter.to_uint8(self.record_data[2:3]),
            he=ByteConverter.to_uint8(self.record_data[3:4]),
        )

    def _decode_event_occurrence(self, event_type: EventRecordType) -> EventOccurrenceRecord:
        return EventOccurrenceRecord(
            when=self.bit_array.get_int(4, 21),
            record_type=self.record_type,
            event_type=event_type,
        )
