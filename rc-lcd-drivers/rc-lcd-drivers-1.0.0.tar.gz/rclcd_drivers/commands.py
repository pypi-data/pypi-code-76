from __future__ import annotations
from .pin import Pin

try:
    from raspi import raspi as r
    __RASPI_HW = True
    __GPIO_INIT = False
    __GPIO_MODE = r.GPIO.BCM
    __MAX_WIDTH = 10
except ModuleNotFoundError:
    __RASPI_HW = False


def init_hw(pins: [Pin]) -> None:
    if(__RASPI_HW):
        r.GPIO.setwarnings(False)
        r.GPIO.setmode(__GPIO_MODE)
        pins = list(map(lambda x: x.value, pins))
        r.define_in_pins(pins)
        r.define_out_pins(pins)
    else:
        raise ValueError('Non-raspi hardware')


def __set_pin(pin: Pin, mode: bool) -> None:
    if(mode):
        r.pins_high(pin.value)
    else:
        r.pins_low(pin.value)


def __get_pin(pin: Pin) -> bool:
    return r.pins_high(pin.value)


def clear_display():
    __set_pin(Pin.REGISTER_SELECT, False)
    __set_pin(Pin.DATA_RW, False)

    __set_pin(Pin.DB7, False)
    __set_pin(Pin.DB6, False)
    __set_pin(Pin.DB5, False)
    __set_pin(Pin.DB4, False)
    __set_pin(Pin.DB3, False)
    __set_pin(Pin.DB2, False)
    __set_pin(Pin.DB1, False)
    __set_pin(Pin.DB0, True)


def return_home():
    __set_pin(Pin.REGISTER_SELECT, False)
    __set_pin(Pin.DATA_RW, False)

    __set_pin(Pin.DB7, False)
    __set_pin(Pin.DB6, False)
    __set_pin(Pin.DB5, False)
    __set_pin(Pin.DB4, False)
    __set_pin(Pin.DB3, False)
    __set_pin(Pin.DB2, False)
    __set_pin(Pin.DB1, True)
    __set_pin(Pin.DB0, True)


def entry_mode_set(direction: bool, shift: bool):
    __set_pin(Pin.REGISTER_SELECT, False)
    __set_pin(Pin.DATA_RW, False)

    __set_pin(Pin.DB7, False)
    __set_pin(Pin.DB6, False)
    __set_pin(Pin.DB5, False)
    __set_pin(Pin.DB4, False)
    __set_pin(Pin.DB3, False)
    __set_pin(Pin.DB2, True)
    __set_pin(Pin.DB1, direction)
    __set_pin(Pin.DB0, shift)


def display_mode(all_on: bool, cursor_on: bool, cursor_pos_on: bool):
    __set_pin(Pin.REGISTER_SELECT, False)
    __set_pin(Pin.DATA_RW, False)

    __set_pin(Pin.DB7, False)
    __set_pin(Pin.DB6, False)
    __set_pin(Pin.DB5, False)
    __set_pin(Pin.DB4, False)
    __set_pin(Pin.DB3, True)
    __set_pin(Pin.DB2, all_on)
    __set_pin(Pin.DB1, cursor_on)
    __set_pin(Pin.DB0, cursor_pos_on)


def cursor_or_display_shift(vertical: bool, horizontal: bool):
    __set_pin(Pin.REGISTER_SELECT, False)
    __set_pin(Pin.DATA_RW, False)

    __set_pin(Pin.DB7, False)
    __set_pin(Pin.DB6, False)
    __set_pin(Pin.DB5, False)
    __set_pin(Pin.DB4, True)
    __set_pin(Pin.DB3, vertical)
    __set_pin(Pin.DB2, horizontal)
    __set_pin(Pin.DB1, True)
    __set_pin(Pin.DB0, True)


def function_set(dl: bool, nl: bool, font_size: bool):
    __set_pin(Pin.REGISTER_SELECT, False)
    __set_pin(Pin.DATA_RW, False)

    __set_pin(Pin.DB7, False)
    __set_pin(Pin.DB6, False)
    __set_pin(Pin.DB5, True)
    __set_pin(Pin.DB4, dl)
    __set_pin(Pin.DB3, nl)
    __set_pin(Pin.DB2, font_size)
    __set_pin(Pin.DB1, True)
    __set_pin(Pin.DB0, True)


def set_cgram_addr(addr: int):
    bits = list(map(lambda x: int(x, 2) == 1, bin(addr)[2:]))
    if(len(bits) > 6):
        raise ValueError('Address domain: 0x00 <= x <= 0x3f')

    __set_pin(Pin.REGISTER_SELECT, False)
    __set_pin(Pin.DATA_RW, False)

    __set_pin(Pin.DB7, False)
    __set_pin(Pin.DB6, True)
    __set_pin(Pin.DB5, bits[0])
    __set_pin(Pin.DB4, bits[1])
    __set_pin(Pin.DB3, bits[2])
    __set_pin(Pin.DB2, bits[3])
    __set_pin(Pin.DB1, bits[4])
    __set_pin(Pin.DB0, bits[5])


def set_ddram_addr(addr: int):
    bits = list(map(lambda x: int(x, 2) == 1, bin(addr)[2:]))
    if(len(bits) > 7):
        raise ValueError('Address domain: 0x0 <= x <= 0x7f')

    __set_pin(Pin.REGISTER_SELECT, False)
    __set_pin(Pin.DATA_RW, False)

    __set_pin(Pin.DB7, True)
    __set_pin(Pin.DB6, bits[0])
    __set_pin(Pin.DB5, bits[1])
    __set_pin(Pin.DB4, bits[2])
    __set_pin(Pin.DB3, bits[3])
    __set_pin(Pin.DB2, bits[4])
    __set_pin(Pin.DB1, bits[5])
    __set_pin(Pin.DB0, bits[6])


def read_busy_flag(addr: int) -> dict:
    __set_pin(Pin.REGISTER_SELECT, False)
    __set_pin(Pin.DATA_RW, True)

    data_pins = [Pin.DB6, Pin.DB5, Pin.DB4, Pin.DB3, Pin.DB2, Pin.DB1, Pin.DB0]
    return {'busy': __get_pin(Pin.DB7),
            'address': list(map(lambda x: __get_pin(x), data_pins))}


def write_to_ram(bits: [int]):
    if(len(bits) > 8):
        raise ValueError('Can only write 8 bits to RAM')
    __set_pin(Pin.REGISTER_SELECT, True)
    __set_pin(Pin.DATA_RW, False)

    __set_pin(Pin.DB7, bits[0])
    __set_pin(Pin.DB6, bits[1])
    __set_pin(Pin.DB5, bits[2])
    __set_pin(Pin.DB4, bits[3])
    __set_pin(Pin.DB3, bits[4])
    __set_pin(Pin.DB2, bits[5])
    __set_pin(Pin.DB1, bits[6])
    __set_pin(Pin.DB0, bits[7])


def read_from_ram() -> [bool]:
    __set_pin(Pin.REGISTER_SELECT, True)
    __set_pin(Pin.DATA_RW, True)

    data_pins = [Pin.DB7, Pin.DB6, Pin.DB5, Pin.DB4,
                 Pin.DB3, Pin.DB2, Pin.DB1, Pin.DB0]
    return list(map(lambda x: __get_pin(x), data_pins))
