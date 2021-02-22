import json
import copy
from src.exceptions.server_failure_exception import ServerFailureException
from src.driver.options import Options

class RokuOptions(Options):
    pass

    session = None
    http_client = None

    def __init__(self, http_client, session):
        self.session = session
        self.http_client = http_client
    
    """
	Attempts to reboot the device.

	:raises ServerFailureException: If an exception occurs during reboot.
	"""
    def reboot(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'reboot_device'
        self.__handler(self.http_client.post_to_server('settings', session))

    def __handler(self, element_json):
        if element_json['results'] != 'success':
            raise ServerFailureException(element_json['results'])
        return element_json

