#!/usr/bin/env python3

import logging
import typing as t
from contextlib import contextmanager
from enum import Enum
from struct import pack
from time import sleep

from serial import Serial

log = logging.getLogger(__name__)

MICROSECOND = 1e-6
MILLISECOND = 1e-3


class SPISpeed(Enum):
    S30k = 0
    S125k = 1
    S250k = 2
    S1M = 3
    S2M = 4
    S2M6 = 5
    S4M = 6
    S8M = 8


CONFIRM = b"\x01"


class Unexpected(ValueError):
    pass


Data = t.Union[bytes, bytearray]


class Mode(Enum):
    BITBANG = 1
    SPI = 2


# sentinel default value for receive's timeout kwarg because None is
# also a legit value there
LEAVE_TIMEOUT_ALONE = object()

TBP = t.TypeVar("TBP", bound="BusPirate")


class BusPirate:
    serial: Serial
    spi_wtr_0r_confirm: bool
    mode: t.Optional[Mode] = None

    def __init__(self, serial: Serial, spi_wtr_0r_confirm=True) -> None:
        self.serial = serial
        self.spi_wtr_0r_confirm = spi_wtr_0r_confirm

    def receive(self, size, timeout=LEAVE_TIMEOUT_ALONE) -> bytes:
        if timeout is LEAVE_TIMEOUT_ALONE:
            rv = self.serial.read(size)
            # log.debug(f"<- {rv.hex()}")
            return rv

        orig_timeout = self.serial.timeout
        self.serial.timeout = timeout
        try:
            rv = self.serial.read(size)
            # log.debug(f"<- {rv.hex()}")
            return rv
        finally:
            self.serial.timeout = orig_timeout

    def send(
        self,
        data: Data,
        expect: t.Optional[bytes] = CONFIRM,
        timeout=LEAVE_TIMEOUT_ALONE,
    ) -> None:
        # log.debug(f"-> {data.hex()}")
        self.serial.write(data)
        # print(ser.out_waiting, ser.in_waiting)
        self.serial.flush()
        sleep(MILLISECOND)
        if expect is not None:
            resp = self.receive(len(expect), timeout=timeout)
            if resp != expect:
                raise Unexpected(f"Expected {expect!r}, got {resp!r}")

    def enter_bitbang(self) -> None:
        if self.mode is None:
            # discard all pending serial data
            while self.receive(1024) != b"":
                pass
            for i in range(25):
                try:
                    self.send(b"\x00", expect=b"BBIO1")
                except Unexpected:
                    pass
                else:
                    self.mode = Mode.BITBANG
                    break

            if self.mode != Mode.BITBANG:
                raise RuntimeError("Couldn't enter binary mode")
        else:
            # self.mode is not None - we're in some binary mode. Even
            # if we're already in bitbang, sending a zero won't hurt.
            self.send(b"\x00", expect=b"BBIO1")
            self.mode = Mode.BITBANG
        log.info("Entered binary bitbang mode")

    def reset(self) -> None:
        self.enter_bitbang()  # just to make sure
        self.send(b"\x0F")
        self.mode = None
        sleep(250 * MILLISECOND)
        self.receive(1024, timeout=0)

    def __enter__(self: TBP) -> TBP:
        return self

    def __exit__(self, *args: t.Any) -> None:
        self.reset()
        self.serial.close()

    def enter_spi(self) -> None:
        if self.mode == Mode.SPI:
            return  # log something?
        if self.mode != Mode.BITBANG:
            self.enter_bitbang()

        self.send(b"\x01", expect=b"SPI1")
        self.mode = Mode.SPI
        log.info("Entered SPI mode")

    def _expect_mode(self, mode: Mode) -> None:
        if self.mode != mode:
            # Maybe this could be an assert?
            raise RuntimeError(f"Need mode {mode}, but BP is in {self.mode}")

    def spi_speed(self, speed: SPISpeed) -> None:
        self._expect_mode(Mode.SPI)
        self.send(pack("B", 0x60 | speed.value))

    def spi_config(
        self,
        output_3v3=False,
        clock_idle_phase_high=False,
        clock_edge_falling=False,
        sample_time_end=False,
    ) -> None:
        self._expect_mode(Mode.SPI)

        cmd = 0x80
        if output_3v3:
            cmd |= 8
        if clock_idle_phase_high:
            cmd |= 4
        if clock_edge_falling:
            cmd |= 2
        if sample_time_end:
            cmd |= 1
        self.send(pack("B", cmd))

    def spi_periph_config(
        self,
        power=False,
        pullups=False,
        aux=False,
        cs=False,
    ) -> None:
        self._expect_mode(Mode.SPI)

        cmd = 0x40
        if power:
            cmd |= 8
        if pullups:
            cmd |= 4
        if aux:
            cmd |= 2
        if cs:
            cmd |= 1
        self.send(pack("B", cmd))

    def spi(
        self,
        speed: SPISpeed,
        output_3v3=False,
        clock_idle_phase_high=False,
        clock_edge_falling=True,
        sample_time_end=False,
        power=True,
        pullups=False,
        aux=False,
        cs=True,
    ) -> None:
        self.enter_spi()
        self.spi_speed(speed)
        self.spi_config(
            output_3v3=output_3v3,
            clock_idle_phase_high=clock_idle_phase_high,
            clock_edge_falling=clock_edge_falling,
            sample_time_end=sample_time_end,
        )
        self.spi_periph_config(power=power, pullups=pullups, aux=aux, cs=cs)

    @contextmanager
    def spi_cs(self):
        self._expect_mode(Mode.SPI)

        self.send(b"\x02")
        try:
            yield
        finally:
            self.send(b"\x03")

    def spi_write_then_read(self, data: Data, read: int, cs: bool = True) -> bytes:
        self._expect_mode(Mode.SPI)

        if cs:
            cmd = 0x04
        else:
            cmd = 0x05
        self.send(pack(">BHH", cmd, len(data), read), expect=b"")
        # If the number of bytes to read or write are out of bounds,
        # the Bus Pirate will return 0x00 now <- this is why we split
        # into two send calls
        if read == 0 and not self.spi_wtr_0r_confirm:
            # Workaround for https://github.com/BusPirate/Bus_Pirate/pull/158
            #
            # There's a bug in BP firmware where write-then-read
            # operation doesn't send confirmation when there is 0
            # bytes to read. Additional problem is that we don't know
            # when BP has finished writing, so client needs to sleep
            # after WTR to avoid interfering with ongoing write.
            expect = b""
        else:
            expect = CONFIRM
        self.send(data, timeout=30, expect=expect)
        if read > 0:
            return self.receive(read, timeout=30)  # FIXME: adjustable timeout?
        return b""

    def spi_transfer(self, data: Data) -> bytes:
        self._expect_mode(Mode.SPI)

        assert len(data) <= 16
        self.send(pack(">B", 0x10 | len(data) - 1))
        self.send(data, expect=None)
        return self.receive(len(data))
