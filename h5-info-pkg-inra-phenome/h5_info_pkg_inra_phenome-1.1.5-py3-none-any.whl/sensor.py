import sys
import struct
import numpy as np

from PIL import Image

from h5_info.constants import TYPE_CAMERA, TYPE_LIDAR, TYPE_MULTISPECTRAL
from h5_info.errors import DataError, DATA_ERROR_MESSAGE
from h5_info.position import Position
from h5_info.camera_image import CameraImage
from h5_info.lidar_image import LidarImage
from h5_info.multispectral_camera_image import MultispectralCameraImage
from datetime import datetime
from h5_info.logger import Logger


class Sensor:
    """Store HDF5 CameraImage attributes in a simplified structure"""

    def __init__(self):
        self.description = ""
        self.manufacturer = ""
        self.model = ""
        self.serial_nb = ""
        self.uri = ""
        self.type = ""
        self.position = Position()
        self.images = []  # Transient
        self.id = 0

    def to_json(self):
        json_dict = {
            "type": self.type,
            "id": str(self.id),
            "description": self.description,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "serial_nb": self.serial_nb,
            "uri": self.uri,
            "position": self.position.to_json(),
            "images": []
        }

        for image in self.images:
            json_dict["images"].append(image.to_json())

        return json_dict

    def from_json(self, json_dict):
        self.type = json_dict["type"]
        self.description = json_dict["description"]
        self.manufacturer = json_dict["manufacturer"]
        self.model = json_dict["model"]
        self.serial_nb = json_dict["serial_nb"]
        self.uri = json_dict["uri"]
        self.id = int(json_dict["id"])
        self.position.from_json(json_dict["position"])

        for image_dict in json_dict["images"]:
            if self.type == TYPE_CAMERA:
                image = CameraImage()
                image.from_json(image_dict)
                self.images.append(image)
            elif self.type == TYPE_LIDAR:
                image = LidarImage()
                image.from_json(image_dict)
                self.images.append(image)
            elif self.type == TYPE_MULTISPECTRAL:
                image = MultispectralCameraImage()
                image.from_json(image_dict)
                self.images.append(image)

    def set_type_from_description(self, description):
        if description.startswith('camera'):
            self.type = TYPE_CAMERA
        elif description.startswith('lms'):
            self.type = TYPE_LIDAR
        elif description.startswith('multispectral'):
            self.type = TYPE_MULTISPECTRAL
        else:
            self.type = "undefined"

    def load_data(self, data_gp, sensor_gp):
        # Extract data for Camera type
        if self.type == TYPE_CAMERA:
            try:
                data = data_gp.get("Data")

                offset = 0
                image_index = 1
                while data is not None and offset < len(data):
                    image = CameraImage()
                    date_int = int.from_bytes(data[offset:offset + 8], "little") / 1e6
                    image.date = datetime.utcfromtimestamp(date_int)
                    image.shutter_time = int.from_bytes(data[offset + 8:offset + 12], "little")
                    image.width = int.from_bytes(data[offset + 12:offset + 16], "little")
                    image.height = int.from_bytes(data[offset + 16:offset + 20], "little")
                    nb_bytes_per_line = int.from_bytes(data[offset + 20:offset + 24], "little")
                    offset += 24
                    image.size = image.height * nb_bytes_per_line
                    image.image = Image.frombytes('I;16', (image.width, image.height), data[offset:offset + image.size])
                    offset += image.size
                    image.name = self.description + "_" + str(image_index)
                    image_index += 1
                    self.images.append(image)
                if len(self.images) == 0:
                    raise ValueError("data is empty")
            except BaseException as error:
                Logger.debug("Internal error: '{0}'".format(error))
                raise DataError(DATA_ERROR_MESSAGE, self.type)
        elif self.type == TYPE_LIDAR:
            try:
                data = data_gp.get("Data")

                image = LidarImage()
                if data is not None and len(data) >= 20:
                    date_int = int.from_bytes(data[0: 8], "little") / 1e6
                    image.date = datetime.utcfromtimestamp(date_int)
                    image.frequency = struct.unpack('<f', data[8:12])[0]
                    image.angle_increment = struct.unpack('<f', data[12:16])[0]
                    image.name = self.description + "_LID.csv"

                offset = 0

                date = []
                angle = []
                distance = []
                reflectivity = []

                # Loading Lidar dataset
                while data is not None and offset < len(data):
                    date_micros = int.from_bytes(data[offset: offset + 8], "little")
                    nb_layers = int.from_bytes(data[offset + 16:offset + 20], "little")
                    offset += 20
                    for l in range(0, nb_layers):
                        nb_scans = int.from_bytes(data[offset:offset + 4], "little")
                        offset += 4
                        data_bytes = bytearray(data[offset:offset + 12 * nb_scans])
                        scan_offset = 0

                        for s in range(0, nb_scans):
                            date.append(date_micros)
                            angle.append(struct.unpack('<f', data_bytes[scan_offset:scan_offset + 4])[0])
                            distance.append(struct.unpack('<f', data_bytes[scan_offset + 4:scan_offset + 8])[0])
                            reflectivity.append(struct.unpack('<f', data_bytes[scan_offset + 8:scan_offset + 12])[0])
                            offset += 12
                            scan_offset += 12

                image.scans['date'] = np.array(date)
                image.scans['angle'] = np.array(angle)
                image.scans['distance'] = np.array(distance)
                image.scans['reflectivity'] = np.array(reflectivity)

                self.images.append(image)
                if len(self.images) == 0:
                    raise ValueError("data is empty")

            except BaseException as error:
                Logger.debug("Internal error: '{0}'".format(error))
                raise DataError(DATA_ERROR_MESSAGE, self.type)

        elif self.type == TYPE_MULTISPECTRAL:
            try:
                for band_gp_id in data_gp:
                    data = data_gp.get(band_gp_id + "/Data")

                    band_gp = sensor_gp.get(band_gp_id)
                    band_channel = int(band_gp.attrs['WaveLength'])

                    offset = 0
                    image_index = 1
                    while data is not None and offset < len(data):
                        image = MultispectralCameraImage()
                        date_int = int.from_bytes(data[offset:offset + 8], "little") / 1e6
                        image.date = datetime.utcfromtimestamp(date_int)
                        image.size = int.from_bytes(data[offset + 8:offset + 16], "little")
                        image.name = self.description + "_" + str(band_channel) + "_" + str(image_index) + "_MS.tif"
                        image.channel = band_channel
                        offset += 16
                        image.data = bytearray(data[offset:offset + image.size])
                        offset += image.size
                        image_index += 1
                        self.images.append(image)
                    if len(self.images) == 0:
                        raise ValueError("data is empty")

            except BaseException as error:
                Logger.debug("Internal error: '{0}'".format(error))
                raise DataError(DATA_ERROR_MESSAGE, self.type)
