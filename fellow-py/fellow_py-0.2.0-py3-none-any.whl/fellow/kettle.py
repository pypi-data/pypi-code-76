"""Define a Kettle class."""

import asyncio
import functools
import logging
from binascii import hexlify

from fellow.exceptions import FellowException

MAGIC_PASSWORD = "efdd0b3031323334353637383930313233349a6d"
CHARACTERISTIC_1820 = "00002a80-0000-1000-8000-00805f9b34fb"


logger = logging.getLogger(__name__)


def wait(func):
    """Decorator to provide reusable wait_for logic around bluetooth commands."""

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        """Function to return in place of the original function."""

        try:
            await asyncio.wait_for(func(self, *args, **kwargs), self._timeout)
        except asyncio.TimeoutError as e:
            raise FellowException from e

    return wrapper


class StaggEKGPlusKettle:
    def __init__(self, address, name=None, command_timeout=None):
        """Initialize Stagg Kettle."""
        from bleak import BleakClient

        self._address = address
        self._client = BleakClient(address)
        self._current_temperature = None
        self._last_seen = None
        self._name = name
        self._ss = 0
        self._target_temperature = None
        self._timeout = command_timeout or 5

    @property
    def address(self):
        """Return mac address or uuid."""
        return self._address

    @property
    def name(self):
        return self._name

    @property
    def current_temperature(self):
        """Return current temperature."""
        return self._current_temperature

    @property
    def target_temperature(self):
        """Return target temperature."""
        return self._target_temperature

    def _subscription_callback(self, _, data):
        """Handle data sent by kettle."""

        hex_data = hexlify(data)

        if self._last_seen is None:
            if hex_data == b"ffffffff":
                self._last_seen = 0
            else:
                return

        if hex_data == b"ffffffff":
            self._last_seen = 0
        elif len(hex_data) == 8 and hex_data != b"00000000":
            if self._last_seen == 0:
                self._current_temperature = int(hex_data[:2], 16)
                self._last_seen = 1
            elif self._last_seen == 1:
                self._target_temperature = int(hex_data[:2], 16)
                self._last_seen = 2

    async def _write(self, uuid: str, data: str):
        """Use bleak library to write data to physical kettle."""

        logger.debug(f"Writing data {data} to characteristic {uuid}")

        try:
            await self._client.write_gatt_char(uuid, bytes.fromhex(data))
        except Exception as e:
            raise FellowException from e

    @wait
    async def connect(self):
        """Establish a bluetooth connection to the kettle."""
        logger.debug("Connecting to self._client...")
        await self._client.connect()
        await self._write(CHARACTERISTIC_1820, MAGIC_PASSWORD)
        await self._client.start_notify(CHARACTERISTIC_1820, self._subscription_callback)

    @wait
    async def disconnect(self):
        """Disconnect from the bluetooth device."""
        logger.debug("Disconnecting from self._client...")
        await self._client.stop_notify(CHARACTERISTIC_1820)
        await self._client.disconnect()

    @wait
    async def is_connected(self):
        """Check if the kettle is connected."""
        logger.debug("Checking if kettle is connected...")
        return await self._client.is_connected()

    @wait
    async def turn_on(self):
        """Turn the kettle on."""
        logger.debug("Turning the kettle on...")
        await self._write(CHARACTERISTIC_1820, "efdd0a0000010100")

    @wait
    async def turn_off(self):
        """Turn the kettle off."""
        logger.debug("Turning the kettle off...")
        await self._write(CHARACTERISTIC_1820, "efdd0a0400000400")

    @wait
    async def set_target_temperature(self, target_temp: int):
        """Set the target temperature for the kettle."""
        logger.debug(f"Setting the kettle's target temperature to {target_temp}...")

        if not (104 <= target_temp <= 212):
            raise ValueError(
                f"Target temperature {target_temp} is outside the supported temperature range of 104 degrees F to 212 degrees F."  # noqa
            )

        ss_hex = hex(self._ss).lstrip("0x")
        while len(ss_hex) < 2:
            ss_hex = f"0{ss_hex}"

        tt_hex = hex(target_temp).lstrip("0x")
        while len(tt_hex) < 2:
            tt_hex = f"0{tt_hex}"

        checksum = hex((self._ss + target_temp) & 0xFF).lstrip("0x")
        while len(checksum) < 2:
            checksum = f"0{checksum}"

        data = f"efdd0a{ss_hex}01{tt_hex}{checksum}01"

        await self._write(CHARACTERISTIC_1820, data)
        self._ss += 1 % 256


async def main():

    # import sys
    # l = logging.getLogger("asyncio")
    # l.setLevel(logging.DEBUG)
    # h = logging.StreamHandler(sys.stdout)
    # h.setLevel(logging.DEBUG)
    # l.addHandler(h)
    # logger.addHandler(h)

    address = "B437CABC-98F4-4188-B404-11890D0A3F48"

    from bleak import BleakScanner

    device = await BleakScanner.find_device_by_address(address)
    kettle = StaggEKGPlusKettle(device.address, device.name)

    await kettle.connect()
    await kettle.turn_on()
    if await kettle._client.is_connected():
        print("Connected!")

    print(kettle.current_temperature, kettle.target_temperature)
    await asyncio.sleep(1.0)
    print(kettle.current_temperature, kettle.target_temperature)
    await asyncio.sleep(1.0)
    print(kettle.current_temperature, kettle.target_temperature)
    await asyncio.sleep(1.0)
    print(kettle.current_temperature, kettle.target_temperature)
    await asyncio.sleep(1.0)
    print(kettle.current_temperature, kettle.target_temperature)

    await kettle.turn_off()
    await kettle.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(main())
