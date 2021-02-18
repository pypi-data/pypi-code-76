"""Controls Jiachang Climate devices.
"""
from .account import JcDevice


class JcClimate(JcDevice):
    def __init__(self, JcDirector, idx):
        """Creates a Jiachang climate object.

        Parameters:
            `JcDirector` - A `jcapi.director.JcDirector` object that corresponds to the Jiachang Director that the climate is connected to.

            `item_id` - The Jiachang item ID of the climate.
        Climate varis:
       {
            "type": "air",
            "attr": {
                "ID": "332",
                "DEVID": "1037",
                "NAME": "空调",
                "SYSNAME": "kt",
                "ICON": null,
                "INUSE": "1",
                "CANDEL": "1",
                "ISR": "0",
                "ISS": "0",
                "ISC": "1",
                "ATTRINT": "1",
                "YYBM": null
            },
            "value": {
                "open": "1",
                "mode": "0",
                "temp": "16",
                "wind": "0",
                "winddir": "0"
            },
            "other": {
                "open": {
                    "1": "关",
                    "0": "开"
                },
                "mode": [
                    "自动",
                    "制冷",
                    "除湿",
                    "通风",
                    "制热"
                ],
                "temp": {
                    "16": 16,
                    "17": 17,
                    "18": 18,
                    "19": 19,
                    "20": 20,
                    "21": 21,
                    "22": 22,
                    "23": 23,
                    "24": 24,
                    "25": 25,
                    "26": 26,
                    "27": 27,
                    "28": 28,
                    "29": 29
                },
                "wind": [
                    "自动",
                    "低",
                    "中",
                    "高"
                ],
                "winddir": [
                    "自动",
                    "上下扫风",
                    "左右扫风",
                    "双向扫风",
                    "固定风向"
                ]
            },
            "detail": false,
            "phydev": "1"
        },
        """
        self.director = JcDirector
        self._device_id = idx

    async def set_hvac_mode(self, mode,**kwargs):
        """Set new target hvac mode."""
        data = {
            'rs': 'execKT',
            'rsargs[]': self._device_id,
            'rsargs[1][op]': 'setMode',
            'rsargs[1][value]': mode
        }
        return await self.director.request(uri="/home/status.php", params=data)

    async def set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        data = {
            'rs': 'execKT',
            'rsargs[]': self._device_id,
            'rsargs[1][op]': 'setFanspeed',
            'rsargs[1][value]': fan_mode
        }
        return await self.director.request(uri="/home/status.php", params=data)

    # async def set_swing_mode(self, swing_mode):
    #     """Set new target swing operation."""

    async def set_temperature(self, temp,**kwargs):
        """Set new target temperature."""
        data = {
            'rs': 'execKT',
            'rsargs[]': self._device_id,
            'rsargs[1][op]': 'setTemp',
            'rsargs[1][value]': temp
        }
        return await self.director.request(uri="/home/status.php", params=data)

    async def open_climate(self):
        """turns on a climate.
        """
        data = {
            'rs': 'execKT',
            'rsargs[]': self._device_id,
            'rsargs[1][op]': 'turnOn',
            'rsargs[1][value]': 1
        }
        return await self.director.request(uri="/home/status.php", params=data)

    async def close_climate(self):
        """turns off a climate.
        """
        data = {
            'rs': 'execKT',
            'rsargs[]': self._device_id,
            'rsargs[1][op]': 'turnOff',
            'rsargs[1][value]': 1
        }
        return await self.director.request(uri="/home/status.php", params=data)
