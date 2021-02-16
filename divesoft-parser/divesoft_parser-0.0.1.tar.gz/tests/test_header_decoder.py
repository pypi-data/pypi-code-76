from io import BytesIO

from divesoft_parser.decoders.header import DLFHeader
from divesoft_parser.models.enums import DiveMode


def test_header_decoder_1():
    dive = DLFHeader(
        BytesIO(bytes.fromhex('4469764506760100768019228500fe6b92005c03e988ffff5c2715000046821d'))
    ).decode()
    assert dive.dive_record_count == 146
    assert dive.dive_day_number == 1
    assert dive.log_number == 1
    assert dive.mode == DiveMode.Gauge


def test_header_decoder_2():
    dive = DLFHeader(
        BytesIO(bytes.fromhex('446976458114640036c19824e606fecbe500b4025a02ffff4829150000468203'))
    ).decode()
    assert dive.dive_record_count == 229
    assert dive.dive_day_number == 1
    assert dive.log_number == 100
    assert dive.mode == DiveMode.OC


def test_header_decoder_3():
    dive = DLFHeader(
        BytesIO(bytes.fromhex('44697645f064fa0052b14327b107fecb9001c0014606ffff1027150000468203'))
    ).decode()
    assert dive.dive_record_count == 400
    assert dive.dive_day_number == 1
    assert dive.log_number == 250
    assert dive.mode == DiveMode.OC
