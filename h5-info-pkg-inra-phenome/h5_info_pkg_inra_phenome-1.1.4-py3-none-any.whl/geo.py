from h5_info import END_LINE_W


class Geo:
    """Store HDF5 Geolocalisation attributes in a simplified structure"""
    def __init__(self):
        self.date = 0
        self.longitude = 0.0
        self.latitude = 0.0
        self.uncertainty = 0.0
        self.tray_height = 0.0
        self.heading = 0.0
        self.course = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.sog = 0.0

    def write_to(self, file):
        file.write(str(self.date) + ";")
        file.write(str(round(self.longitude, 8)) + ";")
        file.write(str(round(self.latitude, 8)) + ";")
        file.write(str(round(self.uncertainty, 6)) + ";")
        file.write(str(round(self.tray_height, 6)) + ";")
        file.write(str(round(self.heading, 8)) + ";")
        file.write(str(round(self.course, 8)) + ";")
        file.write(str(round(self.roll, 8)) + ";")
        file.write(str(round(self.pitch, 8)) + ";")
        file.write(str(round(self.sog, 6)) + END_LINE_W)

    def read_from_line(self, line):
        values = line.strip().split(';')

        self.date = int(values[0])
        self.longitude = float(values[1])
        self.latitude = float(values[2])
        self.uncertainty = float(values[3])
        self.tray_height = float(values[4])
        self.heading = float(values[5])
        self.course = float(values[6])
        self.roll = float(values[7])
        self.pitch = float(values[8])
        self.sog = float(values[9])

    @staticmethod
    def to_dict_array(geo_list):
        """Converts a list of Geo objects to a dictionary array with Geo attributes as keys"""
        res = {
            'date': [],
            'longitude': [],
            'latitude': [],
            'uncertainty': [],
            'tray_height': [],
            'heading': [],
            'course': [],
            'roll': [],
            'pitch': [],
            'sog': [],
        }
        for item in geo_list:
            res['date'].append(item.date)
            res['longitude'].append(item.longitude)
            res['latitude'].append(item.latitude)
            res['uncertainty'].append(item.uncertainty)
            res['tray_height'].append(item.tray_height)
            res['heading'].append(item.heading)
            res['course'].append(item.course)
            res['roll'].append(item.roll)
            res['pitch'].append(item.pitch)
            res['sog'].append(item.sog)

        return res
