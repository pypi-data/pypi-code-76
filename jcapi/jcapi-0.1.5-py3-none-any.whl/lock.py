"""Controls Jiachang lock devices."""
import json
from .account import JcDevice


class JcLock(JcDevice):
    def __init__(self, JcDirector, idx):
        """Creates a Jiachang lock object.

        Parameters:
            `JcDirector` - A `jcapi.director.JcDirector` object that corresponds to the Jiachang Director that the lock is connected to.

            `item_id` - The Jiachang item ID of the switch.
        """
        self.director = JcDirector
        self._device_id = idx

    async def get_state(self):
        """Returns the lock state of a lock as a boolean (True=locked, False=open).
        """
        if str(self.value) == "2":
            return True
        else:
            return False

    async def async_get_record(self):
        """get the name of last changed by user.
        """
        res = await self.director.get_item_info(self._device_id)
        print(res)
        records=json.loads(res)["detail"]["ksrecord"]
        name = sorted(records.items())[-1][1][0]["text"]
        return name

    async def async_unlock(self):
        """unlock a lock.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self._device_id,
            "rsargs[1][m]": "0",
        }
        return await self.director.request(uri="/devattr/devattr.php", params=data)

    async def async_lock(self):
        """lock a lock.
        """
        data = {
            "rs": "execAttr",
            "rsargs[]": self._device_id,
            "rsargs[1][m]": "1",
        }
        return await self.director.request(uri="/devattr/devattr.php", params=data)