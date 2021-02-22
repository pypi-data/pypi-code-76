
class RokuDeviceInfo():
    
    device_info_obj = None

    def __init__(self, info_json):
        self.device_info_obj = info_json["device-info"]

    """
	Gets the device info of key/value device info entries.
	
	:returns: The complete Roku device info object of device info name/values.
	"""
    def get_device_info(self):
        return self.device_info_obj

    """
	Gets the device info Object value of the provided attribute name.
    i.e. get_device_info_attribute('friendly-device-name')
	
	:param attribute_name: - The attribute name of the value to be returned.
    :returns: The Roku attribute value.
	"""
    def get_device_info_attribute(self, attribute_name):
        return self.device_info_obj[attribute_name]

