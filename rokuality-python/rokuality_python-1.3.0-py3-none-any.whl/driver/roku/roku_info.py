import copy
from src.exceptions.server_failure_exception import ServerFailureException
from src.driver.roku.roku_device_info import RokuDeviceInfo
from src.driver.roku.roku_media_player_info import RokuMediaPlayerInfo
from src.utils.file_to_string_utils import FileToStringUtils

class RokuInfo():
    session = None
    http_client = None

    def __init__(self, http_client, session):
        self.session = session
        self.http_client = http_client
    
    """
	Gets info about the Roku device under test such as version, power mode, etc.
	
	:returns: RokuDeviceInfo - Various information about the device under test.
	"""
    def get_device_info(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'device_info'
        device_info_json = self.__handler(self.http_client.post_to_server('info', session))
        return RokuDeviceInfo(device_info_json)
    
    """
	Gets info about the Roku media player under test including buffering information, the player state, player errors, etc.
	
	:returns: RokuMediaPlayerInfo - Various information about the device media player under test.
	"""
    def get_media_player_info(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'media_player_info'
        media_info_json = self.__handler(self.http_client.post_to_server('info', session))
        return RokuMediaPlayerInfo(media_info_json)

    """
	Gets the Roku debugger logs from session start to now.
	
	:returns: String - The Roku debugger logs.
	"""
    def get_debug_logs(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'get_debug_logs'
        log_json = self.__handler(self.http_client.post_to_server('info', session))
        return log_json['log_content']

    """
	Gets the Roku performance profile (.bsprof) file from the device which can be used to monitor the apps CPU and memory behavior.
	
    NOTE - you must pass the 'EnablePerformanceProfiling' capability on session start with a value of True to enable this capture.
	The returned .bsprof file can then be loaded into the Roku brightscript profile visualizer tool at http://devtools.web.roku.com/profiler/viewer/
	and will showcase the apps CPU and memory utilizations and help diagnose any performance issues on the device.
	 
    Note - calling this method will reset the performance profile capture on the device and will relaunch the app.
	
	:returns: The path to the Roku brightscript profile which can be loaded into http://devtools.web.roku.com/profiler/viewer/
	:raises ScreenException: If the user did NOT start the test session with the 'EnablePerformanceProfiling' capability set to True, 
	Or an error occurred during the collection of the performance profile data.
	"""
    def get_performance_profile(self):
        session = copy.deepcopy(self.session)
        session['action'] = 'performance_profile'
        profile_json = self.__handler(self.http_client.post_to_server('info', session))
        return FileToStringUtils().convert_to_file(profile_json["performance_profiling_data"], profile_json["performance_profile_file_ext"])


    def __handler(self, element_json):
        if element_json['results'] != 'success':
            raise ServerFailureException(element_json['results'])
        return element_json
