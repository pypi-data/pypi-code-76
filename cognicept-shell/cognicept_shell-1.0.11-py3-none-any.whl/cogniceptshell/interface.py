# Copyright 2020 Cognicept Systems
# Author: Jakub Tomasek (jakub@cognicept.systems)
# --> Main executable file to handle input arguments

import argparse
import os
import sys
import pkg_resources

from cogniceptshell.configuration import Configuration
from cogniceptshell.agent_life_cycle import AgentLifeCycle
from cogniceptshell.rosbag_record import RosbagRecord
from cogniceptshell.pusher import Pusher


def main():

    # Create the parser
    parser = argparse.ArgumentParser(
        description='Shell utility to configure Cognicept tools.')

    parser.add_argument('--version', action='version',
                        version=pkg_resources.require("cognicept-shell")[0].version)

    subparsers = parser.add_subparsers(help='', title="Commands")

    parser_config = subparsers.add_parser(
        'config', help='Configure Cognicept tools')
    parser_status = subparsers.add_parser(
        'status', help='Get status of Cognicept agents')
    parser_lastevent = subparsers.add_parser(
        'lastevent', help='Display last event log reported by Cognicept agent')
    parser_update = subparsers.add_parser(
        'update', help='Update Cognicept tools')
    parser_keyrotate = subparsers.add_parser(
        'keyrotate', help='Rotate Cognicept cloud keys')
    parser_restart = subparsers.add_parser(
        'restart', help='Restart Cognicept agents')
    parser_start = subparsers.add_parser(
        'start', help='Start Cognicept agents')
    parser_stop = subparsers.add_parser('stop', help='Stops Cognicept agents')
    parser_orbitty = subparsers.add_parser('orbitty', help='Run Orbitty')
    parser_record = subparsers.add_parser(
        'record', help='Manages rosbag recording')
    parser_push = subparsers.add_parser(
        'push', help='Pushes stuff to Cognicept cloud')

    local_cfg = Configuration()
    DEFAULT_PATH = "~/.cognicept/"
    parser_config.set_defaults(func=local_cfg.configure)
    parser_config.add_argument(
        '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
    parser_config.add_argument(
        '--add',  help='Add new environmental variable in config file', action='store_true')
    parser_config.add_argument(
        '--ssh',  help='Configure ssh access during remote intervention', action='store_true')
    parser_config.add_argument(
        '--read',  help='Prints Cognicept configuration', action='store_true')

    parser_keyrotate.set_defaults(func=local_cfg.cognicept_key_rotate)
    parser_keyrotate.add_argument(
        '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)

    agent_lifetime = AgentLifeCycle()
    parser_status.set_defaults(func=agent_lifetime.status)
    parser_status.add_argument(
        '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)

    parser_lastevent.set_defaults(func=agent_lifetime.get_last_event)
    parser_lastevent.add_argument(
        '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)

    parser_restart.set_defaults(func=agent_lifetime.restart)
    parser_restart.add_argument(
        '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
    parser_restart.add_argument(
        'list', help='List of agents to restart', metavar='list', type=str, nargs='*')
    parser_restart.add_argument(
        '--datadog', help='Restart only datadog agent', action='store_true')
    parser_restart.add_argument(
        '--agents', help='Restart only cognicept agents', action='store_true')

    parser_start.set_defaults(func=agent_lifetime.start)
    parser_start.add_argument(
        '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
    parser_start.add_argument(
        'list', help='List of agents to start', metavar='list', type=str, nargs='*')
    parser_start.add_argument(
        '--datadog', help='Restart only datadog agent', action='store_true')
    parser_start.add_argument(
        '--agents', help='Restart only cognicept agents', action='store_true')

    parser_stop.set_defaults(func=agent_lifetime.stop)
    parser_stop.add_argument(
        '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
    parser_stop.add_argument(
        'list', help='List of agents to stop', metavar='list', type=str, nargs='*')
    parser_stop.add_argument(
        '--datadog', help='Stop only datadog agent', action='store_true')
    parser_stop.add_argument(
        '--agents', help='Stop only cognicept agents', action='store_true')

    parser_update.set_defaults(func=agent_lifetime.update)
    parser_update.add_argument(
        '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
    parser_update.add_argument(
        '--reset', help='Triggers new login before update', action='store_true')

    parser_orbitty.set_defaults(func=agent_lifetime.run_orbitty)
    parser_orbitty.add_argument(
        '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)

    record_session = RosbagRecord()
    parser_record.set_defaults(func=record_session.record)
    parser_record.add_argument(
        '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
    parser_record.add_argument(
        '--start', help='Start rosbag recording session. Provide topics to record separated by spaces. e.g. cognicept record --start rosout odom', nargs='+')
    parser_record.add_argument(
        '--stop', help='Stop rosbag recording session', action='store_true')
    parser_record.add_argument(
        '--pause', help='Pause rosbag recording session', action='store_true')
    parser_record.add_argument(
        '--resume', help='Resume rosbag recording session', action='store_true')
    parser_record.add_argument(
        '--status', help='Get current recording session status', action='store_true')

    pusher_instance = Pusher()
    parser_push.set_defaults(func=pusher_instance.push)
    parser_push.add_argument(
        '--path', help='Cognicept configuration directory (default: `' + DEFAULT_PATH + '`)', default=DEFAULT_PATH)
    parser_push.add_argument(
        '--bag', help='Pushes rosbag to the configured S3 bucket. Set to BAG to latest to upload latest bag')
    # Parse the arguments
    args = parser.parse_args()

    if("path" not in args):
        parser.print_help()
    else:
        local_cfg.load_config(args.path)
        agent_lifetime.configure_containers(local_cfg)
        args.config = local_cfg

        if(hasattr(args, 'func')):
            args.func(args)


if __name__ == "__main__":
    main()
