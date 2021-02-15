# coding=utf8
# Copyright 2020 Cognicept Systems
# Author: Swarooph Seshadri (swarooph@cognicept.systems)
# --> RosbagRecord class handles on demand rosbag recording for cognicept-shell

from dotenv import dotenv_values
from pathlib import Path
import os
import sys
import time
import docker
from cogniceptshell.common import bcolors


class RosbagRecord:
    """
    TODO
    ...

    Parameters
    ----------
    TODO

    Methods
    -------
    TODO
    """
    config_path = os.path.expanduser("~/.cognicept/")
    env_path = config_path + "runtime.env"

    def record(self, args):
        """
        TODO

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        TODO
        """
        # Entry point method to decide which mode to call
        if((args.start is None) and (args.stop is False)
           and (args.pause is False) and (args.resume is False)
           and (args.status is False)):
            # start or stop must be provided
            print(bcolors.FAIL +
                  ("Required command is missing."
                   " Check `cognicept record --help` "
                   "for more commands available.") +
                  bcolors.ENDC)
        elif args.start:
            # to start recording
            print(bcolors.OKBLUE + "Starting recording" + bcolors.ENDC)
            self.start_record(args)
        elif args.stop:
            # to stop recording
            print(bcolors.OKBLUE + "Stopping recording" + bcolors.ENDC)
            self.stop_record(args)
        elif args.pause:
            # to pause recording
            print(bcolors.OKBLUE + "Pausing recording" + bcolors.ENDC)
            self.pause_record(args)
        elif args.resume:
            # to resume recording
            print(bcolors.OKBLUE + "Resuming recording" + bcolors.ENDC)
            self.resume_record(args)
        elif args.status:
            # query recording status
            print(bcolors.OKBLUE + "Getting recording status" + bcolors.ENDC)
            self.get_record_status(args)
        else:
            # This should never execute
            print(bcolors.FAIL +
                  ("Required command is missing."
                   " Check `cognicept record --help` "
                   "for more commands available.") +
                  bcolors.ENDC)

    def start_record(self, args):
        """
        TODO

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        TODO
        """
        rosbag_start_cmd = "record_cmd.bash start "
        selected_topics = ','.join(args.start)
        rosbag_start_cmd = rosbag_start_cmd + "'" + selected_topics + "'"
        client = docker.from_env()
        try:
            container = client.containers.get('cgs_bagger_server')
            container_response = container.exec_run(
                rosbag_start_cmd, stream=True, stdout=True)
            self.print_status(container_response)
            print(bcolors.OKBLUE +
                  ("Use `cognicept record --status` "
                   "for detailed progress.\n"
                   "Use `cognicept record --stop` "
                   "to stop recording.") +
                  bcolors.ENDC)
        except docker.errors.APIError as e:
            print(bcolors.FAIL + "DOCKER ERROR" + bcolors.ENDC)
            print("What error: ", str(e))

    def stop_record(self, args):
        """
        TODO

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        TODO
        """
        rosbag_stop_cmd = "record_cmd.bash stop"
        client = docker.from_env()
        try:
            container = client.containers.get('cgs_bagger_server')
            container_response = container.exec_run(
                rosbag_stop_cmd, stream=True, stdout=True)
            self.print_status(container_response)
            print(bcolors.OKBLUE + "Recording has stopped." + bcolors.ENDC)
        except docker.errors.APIError as e:
            print(bcolors.FAIL + "DOCKER ERROR" + bcolors.ENDC)
            print("What error: ", str(e))

    def pause_record(self, args):
        """
        TODO

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        TODO
        """
        rosbag_pause_cmd = "record_cmd.bash pause"
        client = docker.from_env()
        try:
            container = client.containers.get('cgs_bagger_server')
            container_response = container.exec_run(
                rosbag_pause_cmd, stream=True, stdout=True)
            self.print_status(container_response)
            print(bcolors.OKBLUE + "DONE." + bcolors.ENDC)
        except docker.errors.APIError as e:
            print(bcolors.FAIL + "DOCKER ERROR" + bcolors.ENDC)
            print("What error: ", str(e))

    def resume_record(self, args):
        """
        TODO

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        TODO
        """
        rosbag_resume_cmd = "record_cmd.bash resume"
        client = docker.from_env()
        try:
            container = client.containers.get('cgs_bagger_server')
            container_response = container.exec_run(
                rosbag_resume_cmd, stream=True, stdout=True)
            self.print_status(container_response)
            print(bcolors.OKBLUE + "DONE." + bcolors.ENDC)
        except docker.errors.APIError as e:
            print(bcolors.FAIL + "DOCKER ERROR" + bcolors.ENDC)
            print("What error: ", str(e))

    def get_record_status(self, args):
        """
        TODO

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
                Returns:
                        TODO
        """
        rosbag_status_cmd = "record_cmd.bash status"
        client = docker.from_env()
        try:
            container = client.containers.get('cgs_bagger_server')
            container_response = container.exec_run(
                rosbag_status_cmd, stream=True, stdout=True)
            self.print_status(container_response)
        except docker.errors.APIError as e:
            print(bcolors.FAIL + "DOCKER ERROR" + bcolors.ENDC)
            print("What error: ", str(e))

    def print_status(self, container_response):
        """
        TODO

                Parameters:
                        TODO
                Returns:
                        TODO
        """
        output_response_str = str(next(container_response.output))
        str_beg = output_response_str.rfind('Recording state:')
        str_end = output_response_str.rfind('Goal Succeeded')
        print(output_response_str[str_beg:str_end-2])
