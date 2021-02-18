"""a Jiachang Sensor devices.
"""
from .account import JcDevice


class JcB_sensor(JcDevice):
    def __init__(self, JcDirector, idx):
        """Creates a Jiachang Sensor object.

        Parameters:
            `JcDirector` - A `jcapi.director.JcDirector` object that corresponds to the Jiachang Director that the sensor is connected to.
            `item_id` - The Jiachang item ID of the sensor.
       
        """
        self.director = JcDirector
        self._device_id = idx

    async def get_state(self):
        """Returns the power state of a dimmer or sensor as a boolean (True=on, False=off).
        """

        if str(self.value) == "0":
            return False
        else:
            return True
