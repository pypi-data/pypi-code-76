import os
from salal.core.log import log
from salal.core.config import config
from salal.core.utilities import utilities 
from salal.core.file_processing import file_processing

class Build:
    
    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['build']
    
    #---------------------------------------------------------------------------

    @classmethod
    def process_content (cls):
        for file_type in config.system['content_file_types']:
            log.message('TRACE', 'Looking for ' + file_type + 'files')
            for file_relative_path in utilities.find_files_by_extension(config.system['paths']['content_root'], file_type):
                # create the target directory if it doesn't exist
                os.makedirs(os.path.join(config.system['paths']['profile_build_dir'], os.path.dirname(file_relative_path)), exist_ok = True)
                log.message('INFO', os.path.join(config.system['paths']['content_root'], file_relative_path))
                file_processing.process(config.system['paths']['content_root'], config.system['paths']['profile_build_dir'], file_relative_path)

    #---------------------------------------------------------------------------

    @classmethod
    def process_resources (cls):
        # Copy all the files in the resources directory to the build
        # directory, processing them according to the appropriate
        # file processing handler.
        #
        # We write files to the same relative path in the build
        # directory as they had in the resources directory. So, for
        # profile <test>, /resources/js/app.js will become
        # /build/test/js/app.js.
        #
        # Theme files get processed first, so they can be overridden
        # by local files. This is accomplished simply by overwriting
        # the theme version of the file.
        resource_dirs = [os.path.join(config.system['paths']['design_root'], config.system['paths']['resource_dir'])]
        if 'theme_root' in config.system['paths']:
            resource_dirs.insert(0, os.path.join(config.system['paths']['theme_root'], config.system['paths']['resource_dir']))
        for resource_dir in resource_dirs:
            # Check if the resource directory exists before processing it
            if not os.path.isdir(resource_dir):
                continue
            log.message('DEBUG', 'Processing resources from ' + resource_dir)
            resource_files = utilities.find_files(resource_dir)
            for file_relative_path in resource_files:
                # create the target directory if it doesn't exist
                os.makedirs(os.path.join(config.system['paths']['profile_build_dir'], os.path.dirname(file_relative_path)), exist_ok = True)
                log.message('INFO', os.path.join(resource_dir, file_relative_path))
                file_processing.process(resource_dir, config.system['paths']['profile_build_dir'], file_relative_path)

    #---------------------------------------------------------------------------

    @classmethod
    def process_modules (cls):
        # Copy module files to the build directory, processing them
        # according to the appropriate file processing handler.
        #
        # The destination directory that is used depends on the system
        # variable <module_mappings>, which is used to set an appropriate
        # destination based on module name and/or file extension.
        #
        # Theme files get processed first, so they can be overridden
        # by local files. This is accomplished simply by overwriting
        # the theme version of the file.
        file_types_to_copy = {'css': 'css', 'js': 'js', 'py': 'py'}
        module_dirs = [os.path.join(config.system['paths']['design_root'], config.system['paths']['module_dir'])]
        if 'theme_root' in config.system['paths']:
            module_dirs.insert(0, os.path.join(config.system['paths']['theme_root'], config.system['paths']['module_dir']))
        for module_dir in module_dirs:
            # Check if the module directory exists before processing it
            if not os.path.isdir(module_dir):
                continue
            log.message('DEBUG', 'Processing modules from ' + module_dir)
            module_subdirs = utilities.find_subdirectories(module_dir)
            for module_subdir in module_subdirs:
                log.message('TRACE', 'Found module ' + module_subdir)
                for file_type in file_types_to_copy:
                    log.message('TRACE', 'Looking for ' + file_type + 'files in ' + module_subdir)
                    source_dir = os.path.join(module_dir, module_subdir)
                    target_dir = os.path.join(config.system['paths']['profile_build_dir'], file_type, module_subdir)
                    module_files = utilities.find_files_by_extension(source_dir, file_type)
                    for module_file in module_files:
                        log.message('INFO', os.path.join(source_dir, module_file))
                        # create the target directory if it doesn't exist
                        os.makedirs(target_dir, exist_ok = True)
                        file_processing.process(source_dir, target_dir, module_file)
        
    #---------------------------------------------------------------------------

    @classmethod
    def execute (cls, tag):
        
        cls.process_content()
        cls.process_resources()
        cls.process_modules() 

    #---------------------------------------------------------------------------

handler = Build
