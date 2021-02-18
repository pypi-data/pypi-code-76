#!/usr/bin/env python3

# Set up IP tunnel through SSM-enabled instance.
#
# See https://aws.nz/aws-utils/ssm-tunnel for more info.
#
# Author: Michael Ludvig (https://aws.nz)

import os
import sys
import time
import copy
import multiprocessing
import argparse

import botocore.exceptions

from .common import *
from .resolver import InstanceResolver

logger_name = "ssm-ssh-tunnel"
tunnel_cidr = "100.64.0.0/16"

def parse_args():
    """
    Parse command line arguments.
    """

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)

    group_general = add_general_parameters(parser)

    group_instance = parser.add_argument_group('Instance Selection')
    group_instance.add_argument('INSTANCE', nargs='?', help='Instance ID, Name, Host name or IP address')
    group_instance.add_argument('--list', '-l', dest='list', action="store_true", help='List instances registered in SSM.')

    group_network = parser.add_argument_group('Networking Options')
    group_network.add_argument('--route', '-r', metavar="ROUTE", dest="routes", type=str, action="append",
        help='CIDR(s) to route through this tunnel. May be used multiple times.')
    group_network.add_argument('--tunnel-cidr', metavar="CIDR", type=str, default=tunnel_cidr, help=f'''By default
        the tunnel endpoint IPs are randomly assigned from the reserved {tunnel_cidr} block (RFC6598).
        This should be ok for most users.''')
    group_network.add_argument('--up-down', metavar="SCRIPT", dest='updown_script', type=str, help='''Script to call
        during tunnel start up and close down. Check out 'ssm-tunnel-updown.dns-example' that
        supports setting a custom DNS server when the tunnel goes up.''')

    parser.description = 'Start IP tunnel to a given SSM instance'
    parser.epilog = f'''
IMPORTANT: instances must be registered in AWS Systems Manager (SSM)
before you can copy files to/from them! Instances not registered in SSM
will not be recognised by {parser.prog} nor show up in --list output.

Visit https://aws.nz/aws-utils/ssm-tunnel for more info and usage examples.

Author: Michael Ludvig
'''

    # Parse supplied arguments
    args = parser.parse_args()

    # If --version do it now and exit
    if args.show_version:
        show_version(args)

    # Require exactly one of INSTANCE or --list
    if bool(args.INSTANCE) + bool(args.list) != 1:
        parser.error("Specify either INSTANCE or --list")

    return args

class SsmSshTunnel:
    def __init__(self, *args, **kwargs):
        # Stats structure
        self.stats = { 'ts': 0, 'l2r': 0, 'r2l': 0 }
        self.stats_lock = threading.Lock()
        self.stats_secs = 10
        self.stats_refresh = 0.5        # Print stats every this many seconds

        self._exiting = False

        self.local_ip = self.remote_ip = self.routes = None
        self.updown_script = self.updown_up_success = None

    def run_command(self, command, assert_0=True):
        self._logger.debug("command: %s", command)
        ret = os.system(command)
        if assert_0:
            assert ret == 0

    def prepare_addrs(self, tunnel_sidr):
        # Pick random local port for the tunnel
        self.local_ip, self.remote_ip = random_ips(tunnel_cidr)

        # Pick random tunnel addresses from the range
        # Create Tunnel device name
        tun_suffix = ".".join(self.local_ip.split(".")[2:])
        self.tun_name = f"tunSSM.{tun_suffix}"

        #self._logger.debug(f"# Local device {self.tun_name} is ready")
        #self._logger.info(f"Local IP: {self.local_ip} / Remote IP: {self.remote_ip}")

    def open_remote_end(self):
        self._logger.debug('Creating tunnel')

        # Start a new Process()
        # SSH to remote side and start 'socat'.
        # Wait for its output.
        # Return the process PID

    def open_local_end(self):
        # Start a new Process()
        # Run 'socat' that talks to the local SSH port
        # Set up routes [if required]
        # Call up-down script [if required]
        # Return the socat PID

        # Configure routes
        #for route in self.routes:
        #    self.run_command(f"sudo ip route add {route} via {self.remote_ip}")
        pass

    def close_tunnel(self):
        # Kill local 'socat' process
        # - that should kill the remote end automatically
        # Wait some time and kill the 'ssh' / 'remote socat' process
        # Call updown script
        pass

    def process_traffic(self):
        tr_l2r = threading.Thread(target=self.local_to_remote, args=[])
        tr_l2r.daemon = True
        tr_l2r.start()

        tr_r2l = threading.Thread(target=self.remote_to_local, args=[])
        tr_r2l.daemon = True
        tr_r2l.start()

        try:
            self.display_stats()

        except KeyboardInterrupt:
            print("")   # Just to avoid "^C" at the end of line

    def run_updown(self, status):
        if not self.updown_script:
            return

        if status == "down" and not self.updown_up_success:
            # If 'up' failed we are immediately called with 'down' - don't do anything.
            return

        routes = " ".join(self.routes)
        try:
            cmd = f"{self.updown_script} {status} {self.tun_name} {self.local_ip} {self.remote_ip} {routes}"
            self._logger.info(f"Running --up-down script: {cmd}")
            self.run_command(cmd)
            self.updown_up_success = True
        except AssertionError:
            self._logger.error(f'Updown script {self.updown_script} exitted with error.')
            sys.exit(1)

    def start(self, tunnel_cidr, routes, updown_script):
        self.routes = routes
        self.updown_script = updown_script

        self.prepare_addrs(tunnel_cidr)

        try:
            self.open_remote_tunnel()
            self.open_local_tunnel()
            self.run_updown("up")
            self.process_traffic()

        finally:
            self._logger.info('Closing tunnel, please wait...')
            self.run_updown("down")
            self.exit()
            self._exiting = True
            self.delete_tun()


    def display_stats(self):
        def _erase_line():
            print('\r\x1B[K', end="")   # Erase line

        stat_history = [self.stats]
        stat_history_len = int(self.stats_secs / self.stats_refresh)
        start_ts = time.time()

        while True:
            time.sleep(self.stats_refresh)

            # Take another 'stat' snapshot
            self.stats_lock.acquire()
            stat_history.insert(1, copy.copy(self.stats))
            self.stats_lock.release()
            stat_history[1]['ts'] = time.time()

            # Calculate sliding window average
            if stat_history[1]['ts'] > stat_history[-1]['ts']:
                l2r_avg = (stat_history[1]['l2r'] - stat_history[-1]['l2r'])/(stat_history[1]['ts'] - stat_history[-1]['ts'])
                r2l_avg = (stat_history[1]['r2l'] - stat_history[-1]['r2l'])/(stat_history[1]['ts'] - stat_history[-1]['ts'])
            else:
                l2r_avg = r2l_avg = 0.0

            # Trim the oldest points
            del(stat_history[stat_history_len+1:])

            uptime = seconds_to_human(time.time()-start_ts, decimal=0)
            l2r_t_h, l2r_t_u = bytes_to_human(stat_history[1]['l2r'])
            r2l_t_h, r2l_t_u = bytes_to_human(stat_history[1]['r2l'])
            l2r_a_h, l2r_a_u = bytes_to_human(l2r_avg)
            r2l_a_h, r2l_a_u = bytes_to_human(r2l_avg)

            _erase_line()
            print(f"{uptime} | In: {r2l_t_h:6.1f}{r2l_t_u:>2s} @ {r2l_a_h:6.1f}{r2l_a_u:>2s}/s | Out: {l2r_t_h:6.1f}{l2r_t_u:>2s} @ {l2r_a_h:6.1f}{l2r_a_u:>2s}/s", end="", flush=True)

def main():
    if sys.platform != "linux":
        print("The 'ssm-tunnel' program only works on Linux at the moment!", file=sys.stderr)
        print("In other systems you are welcome to install it in VirtualBox or in a similar virtual environment running Linux.", file=sys.stderr)
        quit(1)

    ## Split command line args
    args = parse_args()

    logger = configure_logging(logger_name, args.log_level)

    tunnel = None
    try:
        if args.list:
            # --list
            InstanceResolver(args).print_list()
            quit(0)

        instance_id = InstanceResolver(args).resolve_instance(args.INSTANCE)
        if not instance_id:
            logger.warning("Could not resolve Instance ID for '%s'", args.INSTANCE)
            logger.warning("Perhaps the '%s' is not registered in SSM?", args.INSTANCE)
            quit(1)

        start_ssh_session(logger, ssh_args=ssh_args, profile=args.profile, region=args.region)

    except (botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError) as e:
        logger.error(e)
        quit(1)

    #finally:
    #    if tunnel:
    #        tunnel.delete_tun()

if __name__ == "__main__":
    main()
