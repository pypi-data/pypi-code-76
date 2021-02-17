import json
from attrdict import AttrDict


class Configuration(object):


    def __init__(self, config_file_name=None):
        if config_file_name != None:
            fp = open( config_file_name, "r" )
            self.config_dir = json.load( fp )


    def get_data_structure( self ):
        return AttrDict( self.config_dir )


    def convert_to_dotted( self, dict_to_confert : dict):
        return AttrDict( dict_to_confert )
