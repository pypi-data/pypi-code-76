"""Controls Jiachang Switch devices.
"""
from .account import JcDevice


class JcSwitch(JcDevice):
    def __init__(self, JcDirector, idx):
        """Creates a Jiachang Switch object.

        Parameters:
            `JcDirector` - A `jcapi.director.JcDirector` object that corresponds to the Jiachang Director that the switch is connected to.

            `item_id` - The Jiachang item ID of the switch.
  
        """
        self.director = JcDirector
        self._device_id = idx

    async def turn_on(self):
        """turns on a switch.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self._device_id,
            "rsargs[m]": "1",
        }
        return await self.director.request(uri="/devattr/devattr.php", params=data)

    async def turn_off(self):
        """turns off a switch.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self._device_id,
            "rsargs[m]": "0",
        }
        return await self.director.request(uri="/devattr/devattr.php", params=data)
