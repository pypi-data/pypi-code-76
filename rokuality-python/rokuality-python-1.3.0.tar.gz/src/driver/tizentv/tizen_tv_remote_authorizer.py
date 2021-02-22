
from src.httpexecutor.http_client import HttpClient
from src.driver.device_capabilities import DeviceCapabilities
from src.driver.base_driver import BaseDriver
from src.driver.finder import Finder
from src.exceptions.session_not_started_exception import SessionNotStartedException
from src.driver.options import Options
from src.driver.tizentv.tizen_tv_remote import TizenTVRemote
from src.driver.screen import Screen


class TizenTVRemoteAuthorizer(BaseDriver):
    pass

    http_client = None
    device_ip_address = None

    """
	Initiates the Tizen TV remote authorizer.

	:param server_url: String - The url your server is listening at, i.e. http://localhost:port
	:param device_ip_address: String - The Tizen TV device IP address.
	"""

    def __init__(self, server_url, device_ip_address):
        self.http_client = HttpClient(server_url)
        self.device_ip_address = device_ip_address

    """
	Initiates the TizenTV remote and waits for the user to manually authorize the device. When this call is made the user will have 60 seconds to accept the
	alert that displays on their Tizen TV Screen. Once authorized, this method
	will return an api key which can be passed to the 'DeviceAPIToken' capability
	for future remote control commands on future driver sessions. The device api
	token will last as long as the tv is powered on and awake, and can be used for any
	subsequent driver sessions.
	
	:raises RemoteInteractException: If the remote control fails to authorize.
    """

    def authorize(self):
        session = {}
        session['action'] = 'authorize_remote'
        session['device_ip'] = self.device_ip_address
        response_obj = self.__handler(
            self.http_client.post_to_server('remote', session))
        return response_obj['device_api_token']

    def __handler(self, session_json):
        if session_json['results'] != 'success':
            raise RemoteInteractException(session_json['results'])
        return session_json
