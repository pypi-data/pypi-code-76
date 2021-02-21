"""Kettle discovery module."""

from fellow.exceptions import FellowException
from fellow.kettle import StaggEKGPlusKettle


async def discover_by_address(address: str) -> StaggEKGPlusKettle:
    """Find a device by a given MAC address or UUID."""
    import bleak

    try:
        device = await bleak.BleakScanner.find_device_by_address(address)
    except bleak.BleakError as e:
        raise FellowException from e
    else:
        return StaggEKGPlusKettle(device.address, device.name)
