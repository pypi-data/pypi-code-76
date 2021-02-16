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
from enum import Enum


class ConfigurationType(Enum):
    Serial_Number = 3
    Deco_Configuration = 4
    Version = 5


class MeasurementType(Enum):
    Battery = 1


class BatteryStats(Enum):
    Discharging = 2
    Charging = 3


class StatusType(Enum):
    Deco_N2_Low = 0
    Deco_N2_High = 1


class DiveMode(Enum):
    OC = 1
    Gauge = 5


class DiveStartReason(Enum):
    Manual = 0


class DiveRecordType(Enum):
    Point = 0
    Manipulation = 1
    Auto = 2
    Diver_Error = 3
    Internal_Error = 4
    Configuration = 6
    Measurement = 7
    Status = 8


class EventRecordType(Enum):
    Mix_Changed = 5
    Start = 6
    Too_Fast = 7
    Above_Ceiling = 8
    Toxic = 9
    Key_Down = 18
    Above_Stop = 20
    Safety_Miss = 21
    Change_Mode = 24
    User_Mark = 26
    CNS = 30
