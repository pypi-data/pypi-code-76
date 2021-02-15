"""
    This is a class that helps store data into a local location on the clients computer.

    Written By: Carlos Rueda Carrasco
    Date: 2021-01-08
"""
# Import all the necessary packages
import json
from datetime import datetime
from pandas import DataFrame
from .data import Data

class Minecraft_Store:
   
    def store_filesystem(self, data, name):
        """
            Method that takes the data from the client and then stores it into the local computer.

            @param data: The data being stored, will be in a json dictionary format
        """
        time = str(self.timestamp_format())
        client_data = Data(filename=name + time)
        client_data.add_observation(data)
        client_data.save_data()
        return str(client_data.absolute_path())

    def timestamp_format(self):
        """
            Method that retrieves the time and date for our file naming
        """
        time_sent_back = ""
        current = datetime.now().strftime("%Y-%m-%d")
        time_sent_back = time_sent_back + current
        return time_sent_back