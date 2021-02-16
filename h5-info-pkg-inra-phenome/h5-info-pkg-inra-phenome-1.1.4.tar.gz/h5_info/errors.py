class GroupError(Exception):
    """Exception raised for errors in a group."""

    def __init__(self, group_name):
        self.group_name = group_name

    def __str__(self):
        return "Can't open group (can't locate group: '" + self.group_name + "')"


class DataError(Exception):
    """Exception raised for errors in a data."""

    def __init__(self, data_type):
        self.data_type = data_type

    def __str__(self):
        return "Data of type '" + self.data_type + "' is invalid or corrupted"


class TiffDataParseError(Exception):
    """Exception raised for errors during a Tiff data parsing."""

    def __init__(self, message=None):
        self._message = message

    def __str__(self):
        if self._message is None:
            return "Tiff image data is corrupted or invalid"
        else:
            return "Tiff image data error: (" + self._message + ")"
