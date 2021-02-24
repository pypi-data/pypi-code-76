"""Utility Luigi object for Queenbee local execution.

QueenbeeTask is a wrapper around luigi.Task which is used by queenbee-local to
execute Queenbee-specific task. You probably don't need to use this module in your code.
"""
import pathlib
import logging
import subprocess
import shlex
import re
import socket
import os
import shutil
import tempfile
import platform
import json

import luigi

# importing all the methods to make it easy for the extensions to grab them all from here
from .helper import parse_input_args, to_snake_case, update_params, _change_permission, \
    _copy_artifacts, to_camel_case, tab_forward


SYSTEM = platform.system()


class QueenbeeTask(luigi.Task):

    """
    A Luigi task to run a single command as a subprocess.

    Luigi has a subclass for running external programs

    https://luigi.readthedocs.io/en/stable/api/luigi.contrib.external_program.html
    https://github.com/spotify/luigi/blob/master/luigi/contrib/external_program.py

    But:
        * It doesn't allow setting up the environment for the command
        * It doesn't support piping
        * It doesn't support progress reporting

    QueenbeeTask:

        * simplifies the process of writing commands
        * captures stdin / stdout
        * supports piping
    """

    @property
    def input_artifacts(self):
        """Task's input artifacts.

        These artifacts will be copied to execution folder before executing the command.
        """
        return []

    @property
    def output_artifacts(self):
        """Task's output artifacts.

        These artifacts will be copied to study folder from execution folder after the
        task is done.
        """
        return []

    @property
    def output_parameters(self):
        """Task's output parameters.

        These parameters will be copied to study folder from execution folder after the
        task is done.
        """
        return []

    def command(self):
        """An executable command which will be passed to subprocess.Popen

        Overwrite this method.
        """
        raise NotImplementedError(
            'Command method must be overwritten in every subclass.'
        )

    def _copy_input_artifacts(self, dst):
        """Copy input artifacts to destination folder.

        Args:
            dst: Execution folder.
        """
        logger = logging.getLogger('luigi-interface')
        for art in self.input_artifacts:
            logger.info(f"copying input artifact: {art['name']}...")
            _copy_artifacts(art['from'], os.path.join(dst, art['to']))

    def _copy_output_artifacts(self, src):
        """Copy output artifacts to project folder.

        Args:
            src: Execution folder.
        """
        logger = logging.getLogger('luigi-interface')
        for art in self.output_artifacts:
            logger.info(f"copying output artifact: {art['name']}...")
            _copy_artifacts(os.path.join(src, art['from']), art['to'])

    def _copy_output_parameters(self, src):
        """Copy output parameters to project folder.

        Args:
            src: Execution folder.
        """
        logger = logging.getLogger('luigi-interface')
        for art in self.output_parameters:
            logger.info(f"copying output parameters: {art['name']}...")
            _copy_artifacts(os.path.join(src, art['from']), art['to'])

    @staticmethod
    def _pre_process_command(input_command):
        """Process input command before execution.

        This method:
            1. separates output file if the output is redirected to a file using >
            2. breaks-down the command into several commands if piping is happening |
        """
        def _raw(text):
            """Raw string representation.

            This is useful to handle edge cases in Windows.
            """

            escape_dict = {
                '\a': r'\a', '\b': r'\b', '\c': r'\c', '\f': r'\f', '\n': r'\n',
                '\r': r'\r', '\t': r'\t', '\v': r'\v', '\'': r'\'', '\"': r'\"',
                '\0': r'\0', '\1': r'\1', '\2': r'\2', '\3': r'\3', '\4': r'\4',
                '\5': r'\5', '\6': r'\6', '\7': r'\7', '\8': r'\8', '\9': r'\9'
            }

            new_string = ''
            for char in text:
                try:
                    new_string += escape_dict[char]
                except KeyError:
                    new_string += char
            return new_string

        output_cmd = []
        input_command = pathlib.Path(input_command).as_posix()
        commands = ' '.join(input_command.split()).split('|')
        STDOUT = (-1, '')  # -1 is PIPE

        for count, command in enumerate(commands[:-1]):

            assert '>' not in command.split('&&')[-1], \
                'You cannot redirect stdout with > and pipe the' \
                ' outputs at the same time:\n\t%s' % command

            # check for stdin
            # -1 means use of stdout from the command before this command
            stdin = -1 if count != 0 else ''
            if '<' in command:
                if count == 0:
                    stdin = _raw(shlex.split(command.split('<')[-1])[0])
                    # replace stdin from the original command
                    command = re.sub(r"\s<+\s\S+", '', command)
                else:
                    raise ValueError(
                        'You cannot use < for stdin and pipe data to command '
                        'at the same time:\n\t%s' % command
                    )

            output_cmd.append(
                {
                    'cmd': command.strip(),
                    'stdin': stdin.strip() if stdin != -1 else stdin,
                    'stdout': STDOUT
                }
            )

        # set-up stdout for the last command
        last_command = commands[-1]
        mode = None
        if '>>' in last_command:
            mode = 'a'
            stdout = _raw(shlex.split(last_command.split('>>')[-1])[0])
        elif '>' in last_command:
            mode = 'w'
            stdout = _raw(shlex.split(last_command.split('>')[-1])[0])
        else:
            stdout = subprocess.PIPE

        command = re.sub(r"\s>+\s\S+", '', last_command)

        stdin = None if len(commands) == 1 else -1
        if '<' in command:
            # now check for stdin
            stdin = _raw(shlex.split(command.split('<')[-1])[0])
            # replace stdin from the original command
            command = re.sub(r"\s<+\s\S+", '', command)

        output_cmd.append(
            {
                'cmd': command.strip(),
                'stdin': stdin,
                'stdout': (stdout, mode)
            }
        )
        return output_cmd

    def _stream_file_content(self, file_object):
        """Return contents of a file like object as a single string."""
        try:
            file_object.seek(0)
        except AttributeError:
            return str(file_object)
        else:
            return ''.join(map(lambda s: s.decode('utf-8'), file_object.readlines())).split('\n')

    @property
    def _is_debug_mode(self):
        if '__debug__' not in self._input_params:
            return False
        return self._input_params['__debug__']

    def _get_dst_folder(self, command):
        debug_folder = self._is_debug_mode
        dst_dir = tempfile.TemporaryDirectory()
        dst = dst_dir.name
        if debug_folder:
            dst_dir = os.path.join(debug_folder, os.path.split(dst_dir.name)[-1])
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir, exist_ok=True)

            if SYSTEM == 'Windows':
                file_name = 'command.bat'
                content = '%s\npause' % command
            else:
                file_name = 'command.sh'
                content = '#!/bin/bash\nfunction pause(){\n\tread -p "$*"\n}' \
                    '\n%s\npause \'Press [Enter] key to continue...\'\n' % command

            command_file = os.path.join(dst_dir, file_name)
            with open(command_file, 'w') as outf:
                outf.write(content)

            os.chmod(command_file, 0o777)
            dst = dst_dir
        return dst_dir, dst

    def run(self):
        logger = logging.getLogger('luigi-interface')

        # replace ' with " for Windows systems and vise versa for unix systems
        command = self.command()
        if SYSTEM == 'Windows':
            command = command.replace('\'', '"')
        else:
            command = command.replace('"', '\'')

        cur_dir = os.getcwd()
        dst_dir, dst = self._get_dst_folder(command)
        os.chdir(dst)

        self._copy_input_artifacts(dst)

        p = subprocess.Popen(
            command, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True, env=os.environ
        )

        stdout, stderr = p.communicate()

        if p.returncode != 0 and stderr != b'':
            errors = self._stream_file_content(stderr)
            logger.error(errors)
            raise RuntimeError(errors)

        if stderr is not None:
            # this is a rare case but happens with Radiance commands where it print
            # to stderr for verbose reporting
            out_info = self._stream_file_content(stderr)
            logger.info(out_info)

        if stdout is not None:
            stdout = self._stream_file_content(stdout)
            logger.info(stdout)

        # copy the results file back
        self._copy_output_artifacts(dst)
        self._copy_output_parameters(dst)
        # change back to initial directory
        os.chdir(cur_dir)
        # delete the temp folder content
        try:
            dst_dir.cleanup()
            shutil.rmtree(dst_dir.name)
        except Exception:
            # folder is in use or running in debug mode
            # this is a temp folder so not deleting is not a major issue
            pass

    @staticmethod
    def load_input_param(input_param):
        """This function tries to import the values from a file as a Task input
            parameter.

        It first tries to import the content as a dictionary assuming the input file is
        a JSON file. If the import as JSON fails it will import the content as string and
        split them by next line. If there are several items it will return a list,
        otherwise it will return a single item.
        """
        content = ''
        with open(input_param, 'r') as param:
            try:
                content = json.load(param)
            except json.decoder.JSONDecodeError:
                # not a JSON file
                pass
            else:
                return content
        with open(input_param, 'r') as param:
            content = param.read().splitlines()
            if len(content) == 1:
                content = content[0]
        return content


def local_scheduler():
    """Check if luigi Daemon is running.

    If it does then return False otherwise return True.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', 8082))
    except Exception:
        # luigi is running
        local_schedule = False
    else:
        # print('Using local scheduler')
        local_schedule = True
    finally:
        sock.close()
        return local_schedule
