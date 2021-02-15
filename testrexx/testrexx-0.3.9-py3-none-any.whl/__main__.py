import os
import logging
from .utilities import TestFile
from .utilities import BG
from .utilities import LOG
from mkrexx import MakeRexx
from decouple import config

INTERNAL_REXX_LIB = 'rexx_lib'
ASSERTION_LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), INTERNAL_REXX_LIB, 'assertions.rex')

class TRexx():

    def __init__(self):
        self.test_code_path = config('TREXX_TEST_CODE_PATH')
        self.test_lib_path = config('TREXX_TEST_LIB_PATH')
        self.test_files = []
        self.__setup_mkrexx()
        self.__build_tests()
        self.__parse_test_files()

    def __setup_mkrexx(self):
        self.__create_test_build_path()
        self.__load_assertion_lib()

    def __create_test_build_path(self):
        if os.path.isdir(self.test_code_path):
            self.test_build_path = os.path.join(self.test_code_path, 'build')
            try:
                os.mkdir(self.test_build_path)
            except FileExistsError:
                pass
        else:
            # TODO handle this properly
            raise Exception(f'"{self.test_code_path}" is an invalid path and this should be handled properly in the code')    

    def __load_assertion_lib(self):
        with open(ASSERTION_LIB, 'r') as file_object:
            assertion_lib_contents = file_object.read()
        self.assertion_lib_records = [record.rstrip() for record in assertion_lib_contents.split('\n')]

    def __build_tests(self):
        self.mk = MakeRexx(origin_path=self.test_code_path,
                           lib_path=self.test_lib_path,
                           build_path=self.test_build_path)
        self.origin_files = [value for key, value in self.mk.origin_files.items()]
        self.__append_assertion_lib()
        self.mk.build()

    def __append_assertion_lib(self):
        for file in self.origin_files:
            file.code.append_records(self.assertion_lib_records)

    def __parse_test_files(self):
        self.test_files = [TestFile(file_object) for file_name, file_object in self.mk.build_files.items()]

    def __len__(self):
        return len(self.test_files)

    def run(self):
        total_runtime = 0
        LOG.info(f"{BG.OKBLUE}Initiating test run...{BG.ENDC}")
        for test_file in self.test_files:
            test_file.run()
            result_list = [test_case.passed for test_case in test_file.test_definitions]
            LOG.info(f"Display test results...")
            print("\n")
            [test_case.display_test_results() for test_case in test_file.test_definitions]
            total_runtime += test_file._run_time
        print("\n")
        print(f"Total runtime: {BG.OKGREEN}{total_runtime:.3f}{BG.ENDC} secs ⌚")
        if False in result_list:
            print(f"{BG.WARNING}Test completed with failed results.{BG.ENDC}")
            exit(1)
