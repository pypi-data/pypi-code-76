"""

"""


# Built-in

# Libs

# Own modules


# Built-in
import os

# Libraries

# Custom
from .misc_utils import load_file, save_file, make_dir_if_not_exist, verb_print

# Settings


class ProcessBlock(object):
    def __init__(self, process_func, process_dir, process_name=None):
        self.process_func = process_func
        self.process_dir = process_dir
        make_dir_if_not_exist(self.process_dir)
        if process_name is None:
            self.process_name = process_func.__name__
        else:
            self.process_name = process_name

    @staticmethod
    def check_complete(state_file):
        """
        check complete status of running process_func
        :param state_file: file where stores the complete status as True (Complete) or False (Incomplete)
        :return: Complete as True, Incomplete as False
        """
        state = load_file(state_file)[0]
        if state == 'Complete':
            return True
        else:
            return False

    def run(self, force_run=False, verbose=True, **kwargs):
        """
        run the process func, update state_file and save the result value
        :param force_run: force the process_func to run again no matter whether the complete status is incomplete or not
        :param verbose: if True, will print the intermediate messages
        :param kwargs: other parameters used by process_func
        :return: result value of process_func
        """
        state_file = os.path.join(self.process_dir, '{}_state.txt'.format(self.process_name))
        value_file = os.path.join(self.process_dir, '{}.pkl'.format(self.process_name))
        # write state file as incomplete if the state file does not exist
        if not os.path.exists(state_file):
            save_file(state_file, 'Incomplete')

        if not self.check_complete(state_file) or not os.path.exists(value_file) or force_run:
            # run the process
            verb_print('Start running process {}'.format(self.process_name), verbose)
            save_file(state_file, 'Incomplete')

            val = self.process_func(**kwargs)
            save_file(value_file, val)

            save_file(state_file, 'Complete')
            verb_print('Complete!', verbose)
        else:
            # load the data
            verb_print('File already exits, load value', verbose)
            val = load_file(value_file)

        return val
