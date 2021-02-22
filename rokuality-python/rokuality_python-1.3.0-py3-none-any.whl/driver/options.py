import copy
from src.exceptions.server_failure_exception import ServerFailureException
from src.enums.session_status import SessionStatus

class Options:

    session = None
    http_client = None

    def __init__(self, http_client, session):
        self.session = session
        self.http_client = http_client
    
    """
	Overrides the default Image Match Similarity value for all Image based elements. It will last for the duration
	of the driver session, or until a new value is set. A lower value 
	will increase the likelihood that your image locator will find a match, but too low a value
	and you can introduce false positives.
	
	:param image_match_similarity: float - the image match similarity to apply to all image elements i.e. '0.95'
	:raises ServerFailureException: If the image match similarity cannot be applied.
	"""
    def set_image_match_similarity(self, image_match_similarity):
        session = copy.deepcopy(self.session)
        session['action'] = 'image_match_similarity'
        session['image_match_similarity'] = str(image_match_similarity)
        element_json = self.__handler(self.http_client.post_to_server('settings', session))

    """
	Sets an implicit wait for all elements in milliseconds. It will last for the duration
	of the driver session, or until a new value is set. By default, when performing a finder().findElement
	command, the locator find will be evaluated immediately and throw an exception if the element is not immediately found.
	By setting this value, the server will search for the element repeatedly until the element is found, or will throw
	the NoSuchElementException if the element is not found after the duration expires. Setting this timeout is recommended
	but setting too high a value can result in increased test time.
	
	:param timeout_in_milliseconds: long - the timeout in milliseconds to wait for an element before throwing an exception.
	:raises ServerFailureException: If the timeout cannot be applied.
	"""
    def set_element_timeout(self, timeout_in_milliseconds):
        session = copy.deepcopy(self.session)
        session['action'] = 'element_find_timeout'
        session['element_find_timeout'] = str(timeout_in_milliseconds)
        element_json = self.__handler(self.http_client.post_to_server('settings', session))

    """
	Sets a dely in milliseconds for remote control interactions. By default there is no pause between 
	remote control commands so remote interactions can happen very fast and may lead to test flake 
	depending on the test scenario. This option allows you to throttle those remote control commands.
	It will last for the duration of the driver session, or until a new value is set.
	
	:param delay_in_milliseconds: long - The pause between remote commands in milliseconds. i.e. '1000'.
	:raises ServerFailureException: If the interact delay cannot be applied.
	"""
    def set_remote_interact_delay(self, delay_in_milliseconds):
        session = copy.deepcopy(self.session)
        session['action'] = 'remote_interact_delay'
        session['remote_interact_delay'] = str(delay_in_milliseconds)
        element_json = self.__handler(self.http_client.post_to_server('settings', session))

    """
	Sets a poll interval for all elements in milliseconds. It will last for the duration
	of the driver session, or until a new value is set. Only applicable if an element timeout has been applied. By
	default the element poll interval is 250 milliseconds.
	
    :param poll_interval_in_milliseconds: long - the poll interval in milliseconds.
	:raises ServerFailureException: If the poll interval cannot be applied.
	"""
    def set_element_poll_interval(self, poll_interval_in_milliseconds):
        session = copy.deepcopy(self.session)
        session['action'] = 'element_polling_interval'
        session['element_polling_interval'] = str(poll_interval_in_milliseconds)
        element_json = self.__handler(self.http_client.post_to_server('settings', session))

    """
	Sets a session status that can be later retrieved during the course of a session. By default the session status is 'In Progress'.
	Useful if you want to set a pass/fail/broken status during the course of a test run and then later retrieve the status
	for communicating with a 3rd party service. The status will last only so long as the session is active and will be lost
	once the user stops the session.
	
    :param status: SessionStatus - the session status.
	:raises ServerFailureException: If the session status cannot be applied.
	"""
    def set_session_status(self, status):
        session = copy.deepcopy(self.session)
        session['action'] = 'set_session_status'
        session['session_status'] = status.value
        self.__handler(self.http_client.post_to_server('settings', session))

    """
	Gets the session status.
	
    :returns: SessionStatus - the session status as set by the user during the course of the session.
	:raises ServerFailureException: If the session status cannot be retrieved.
	"""
    def get_session_status(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'get_session_status'
        option_json = self.__handler(self.http_client.post_to_server('settings', session))
        return option_json['session_status']

    def __handler(self, element_json):
        if element_json['results'] != 'success':
            raise ServerFailureException(element_json['results'])
        return element_json

