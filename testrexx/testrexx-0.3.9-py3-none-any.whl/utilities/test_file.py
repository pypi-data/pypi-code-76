import os
import functools
import time
from .test_jcl import TestJcl
from .test_case import TestCase
from .exceptions import ZoweConfigurationNotFound
from .background_colors import BG
from .logger import LOG
from decouple import config
from decouple import UndefinedValueError
from zowe.zos_files_for_zowe_sdk import Files




try:
    ZOWE_CONNECTION = {'plugin_profile': config('ZOWE_ZOSMF_PROFILE')}
except UndefinedValueError:
    try:
        host_url = config('ZOWE_ZOSMF_URL')
        user = config('ZOWE_ZOSMF_USER')
        password = config('ZOWE_ZOSMF_PASSWORD')
        if host_url and user and password:
            ZOWE_CONNECTION = {
                'host_url': host_url,
                'user': user,
                'password': password,
                'ssl_verification': False
            }
    except UndefinedValueError:
        raise ZoweConfigurationNotFound('Missing required environment variable for ZOWE z/OSMF \
                         [ZOWE_ZOSMF_URL,ZOWE_ZOSMF_USER,ZOWE_ZOSMF_PASSWORD] or ZOWE_ZOSMF_PROFILE')

ZOS_FILES = Files(ZOWE_CONNECTION)


def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        test_file_object = args[0]
        setattr(test_file_object, '_run_time', run_time)
        return value
    return wrapper_timer

class TestFile:

    def __init__(self, file_object):
        self.file_object = file_object
        self.code = self.file_object.code
        self.test_definitions = []
        self.test_dataset = config('TREXX_TEST_DATASET')
        self.member_name = 'TEMPREXX'

    @timer
    def run(self):
        self.__setup()
        self.__trigger_test_rexx()
        self.__validate_results()
        self.__teardown()

    def __setup(self):
        LOG.debug(f'Initiating test file "{self.file_object.file_name}" setup process')
        self.__get_test_definitions()
        self.__upload_test_file()

    def __get_test_definitions(self):
        LOG.debug(f'Retrieving definitions from test file "{self.file_object.file_name}"')
        test_id_number = 0
        for docstring in self.code.docstring_statements:
            if docstring.statement == 'TEST':
                LOG.debug(f'Test definition found "{docstring.values}"')
                test_id_number += 1
                test_id = f'TEST{test_id_number}'
                self.test_definitions.append(TestCase(test_id,
                                                      docstring.values))

    def __upload_test_file(self):
        LOG.debug(f'Uploading test rexx file to "{self.test_dataset}({self.member_name})"')
        ZOS_FILES.upload_file_to_dsn(self.file_object.file_path,
                                     f'{self.test_dataset}({self.member_name})')

    def __trigger_test_rexx(self):
        LOG.debug('Executing test rexx file...')
        self.test_jcl = TestJcl(self.test_dataset, ZOWE_CONNECTION)
        self.test_jcl.trigger_rexx(self.member_name)
        self.execution_results = self.test_jcl.result_records

    def __validate_results(self):
        LOG.debug(f'Initiating validation process')
        self.raw_test_results = []
        for record in self.execution_results:
            record = record.strip()
            if record.startswith('%TEST'):
                record_columns = record.split('=')
                test_id = record_columns[0][1:]
                test_result = record_columns[1].split(',')[0]
                self.raw_test_results.append({
                    'test_id': test_id,
                    'test_result': test_result,
                    'raw': record
                })

        if len(self.test_definitions) == len(self.raw_test_results):
            for test_definition in self.test_definitions:
                for test_result in self.raw_test_results:
                    if test_definition.test_id == test_result['test_id']:
                        if test_result['test_result'] == 'SUCCESS':
                            test_definition.passed = True
                        test_definition.raw_test_result = test_result['raw']
        else:
            LOG.error(f'Missing @TEST docstring statement in test file "{BG.FAIL}{self.file_object.file_path}{BG.ENDC}", unable to display results')
            exit(1)

    def __teardown(self):
        LOG.debug("Cleaning up")
        self.test_jcl.delete_from_spool()
