import json
import copy
from src.exceptions.screen_exception import ScreenException
from src.driver.element import Element
from src.driver.screen import Screen

class RokuScreen(Screen):
    pass

    session = None
    http_client = None

    def __init__(self, http_client, session):
        self.session = session
        self.http_client = http_client
    
    """
	Gets the xml page source of the Roku device under test.

	:returns: String - The application page source.
	:raises ScreenException: If the page source cannot be captured.
	"""
    def get_page_source(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'get_screen_source'
        screen_json = self.__handler(self.http_client.post_to_server('screen', session))
        return screen_json["source"]

    """
	Gets the current focused element within the app under test.

	:returns: Element - The currently focused element.
	:raises ScreenException: If the active element cannot be determined.
	"""
    def get_active_element(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'get_active_element'
        screen_json = self.__handler(self.http_client.post_to_server('screen', session))
        return Element(screen_json)

    def __handler(self, element_json):
        if element_json['results'] != 'success':
            raise ScreenException(element_json['results'])
        return element_json

