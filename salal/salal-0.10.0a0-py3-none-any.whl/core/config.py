import sys
import os.path
import json
import argparse
from salal.core.log import log
from salal.core.utilities import utilities

# After initialization, the following attributes are available on
# the <config> object:
# - action: the action to be executed
# - profile: the build profile to use while executing it
# - system: a dict of system configuration variables
# - project: a dict of project configuration variables

class Config:

    #---------------------------------------------------------------------------

    @classmethod
    def initialize (cls):
        cls.set_salal_root()
        cls.parse_arguments ()
        cls.load_system_configuration ()
        cls.load_build_profiles ()
        cls.initialize_variables ()
    
    #---------------------------------------------------------------------------
 
    @classmethod
    def set_salal_root (cls):
        cls.system = {}
        cls.system['paths'] = {}
        cls.system['paths']['salal_root'] = os.path.normpath(os.path.dirname(sys.modules['__main__'].__file__))
    
    #---------------------------------------------------------------------------
   
    @classmethod
    def parse_arguments (cls):
        parser = argparse.ArgumentParser()
        parser.add_argument('action', action = 'store')
        parser.add_argument('profile', action = 'store', nargs = '?', default = 'default')
        parser.add_argument('--config-file', action = 'store', default = os.path.join(cls.system['paths']['salal_root'], 'system.json'))
        parser.add_argument('--logging-level', action = 'store', default = 'INFO')
        cls._arguments = parser.parse_args()
        # we shouldn't do any logging until this point has been reached,
        # otherwise it won't be impacted by the logging level
        log.set_logging_level(cls._arguments.logging_level)
        cls.action = cls._arguments.action
        log.message('DEBUG', 'Parsed command line arguments')

    #---------------------------------------------------------------------------

    @classmethod
    def load_system_configuration (cls):
        log.message('DEBUG', 'Loading system configuration from ' + cls._arguments.config_file)
        with open(cls._arguments.config_file) as system_variables_fh:
            utilities.deep_update(cls.system, json.load(system_variables_fh))

    #---------------------------------------------------------------------------

    @classmethod
    def load_build_profiles (cls):
        log.message('DEBUG', 'Loading build profiles from ' + cls.system['paths']['profiles_file'])
        with open(cls.system['paths']['profiles_file']) as build_profiles_fh:
            cls._build_profiles = json.load(build_profiles_fh)
        
    #---------------------------------------------------------------------------
    @classmethod
    def initialize_variables (cls):
        log.message('DEBUG', 'Using salal root directory of ' + cls.system['paths']['salal_root'])
        # convert the profile specifier to the correct profile name
        if cls._arguments.profile == 'default':
            cls.profile = None
            for build_profile in cls._build_profiles:
                if build_profile == 'common':
                    continue
                else:
                    cls.profile = build_profile
                    break
            if cls.profile == None:
                log.message('ERROR', 'Default profile specified, but there are no profiles configured')
        elif cls._arguments.profile in cls._build_profiles:
            cls.profile = cls._arguments.profile
        else:
            log.message('ERROR', 'Specified profile ' + cls._arguments.profile + ' does not exist')
        log.message('INFO', 'Using profile ' + cls.profile)
        cls.system['paths']['profile_build_dir'] = os.path.join(cls.system['paths']['build_root'], cls.profile)
        
        log.message('DEBUG', 'Initializing system and project variables')
        cls.project = dict()
        profile_vars = { 'system': cls.system, 'project': cls.project }
        for var_type in ['system', 'project']:
            if 'common' in cls._build_profiles and var_type in cls._build_profiles['common']:
                utilities.deep_update(profile_vars[var_type], cls._build_profiles['common'][var_type])
            if var_type in cls._build_profiles[cls.profile]:
                utilities.deep_update(profile_vars[var_type], cls._build_profiles[cls.profile][var_type])
        if 'theme_root' in config.system:
            log.message('INFO', 'Using theme ' + config.system['theme_root'])
                
    #---------------------------------------------------------------------------

config = Config
