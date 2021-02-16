#!/usr/bin/env python3

import argparse
import os
import signal
import subprocess
from shutil import which
from pyWebCamWebServerMonitor.api.user import reset_admin_password
from pyWebCamWebServerMonitor import main_dir
import re
pkg_dir = main_dir[:main_dir.rindex("/")]

def install_as_sys_service(args):

    port = args.port
    is_local = (str(args.local_listening).lower() == 'true')
    ip_serve = ('', '--host=127.0.0.1')[is_local]
    is_root = (str(args.user_root).lower() == 'true')
    user = (os.getlogin(), 'root')[is_root]
    isPath = 'PATH' in os.environ
    path_var = ''
    if isPath:
        path_var = os.environ['PATH']


    cwd = pkg_dir
    waitress_bin = which('waitress-serve')
    if waitress_bin is None:
        print('Cound not install service, waitress-serve was not found on system')
        return
    start_cmd = "{} --port={} {} --threads=6 --call 'pyWebCamWebServerMonitor:create_app'".format(
        waitress_bin, str(port), ip_serve)
    service_path = '/etc/systemd/system/pyWebCamWebServerMonitor.service'

    if(os.getuid() == 0):

        serviceFileLines = []
        serviceFileLines.append('[Unit]\n')
        serviceFileLines.append('Description=WebCam Web control application\n')
        serviceFileLines.append('After=network.target\n')
        serviceFileLines.append('\n')
        serviceFileLines.append('[Service]\n')
        serviceFileLines.append('User={}\n'.format(user))
        if isPath:
            serviceFileLines.append('Environment="PATH={}"\n'.format(path_var))
        serviceFileLines.append('WorkingDirectory={}\n'.format(cwd))
        serviceFileLines.append('ExecStart={}\n'.format(start_cmd))
        serviceFileLines.append('ExecReload=/bin/kill -HUP $MAINPID\n')
        serviceFileLines.append('Restart=always\n')
        serviceFileLines.append('RestartSec=2\n')
        serviceFileLines.append('SyslogIdentifier=pyWebCamWebServerMonitor\n')
        serviceFileLines.append('\n')
        serviceFileLines.append('[Install]\n')
        serviceFileLines.append('WantedBy=multi-user.target\n')

        file = open(service_path, 'w')
        file.writelines(serviceFileLines)
        file.close()
        print('\033[92m OK\033[00m: Service File Was written in {}'.format(service_path))
        subprocess.run("systemctl daemon-reload", shell=True,
                       capture_output=False, close_fds=True)
        print('\033[92m OK\033[00m: Service Reloaded')
        subprocess.run("systemctl enable pyWebCamWebServerMonitor",
                       shell=True, capture_output=False, close_fds=True)
        print('\033[92m OK\033[00m: Service Enabled')
        subprocess.run("systemctl start pyWebCamWebServerMonitor",
                       shell=True, capture_output=False, close_fds=True)
        if is_local:
             print('\033[92m OK\033[00m: Service Started, listening local only on http://127.0.0.1:{}'.format(port))
        else:
            print('\033[92m OK\033[00m: Service Started, listening on 0.0.0.0:{} visit http://127.0.0.1:{} or http://<HOST-IP>:{}'.format(port, port, port))
        return
    else:
        print('\033[91m ERROR\033[00m: You are not an Admin, you need admin rights to install a service try using  \'sudo -E env "PATH=$PATH" pyWebCamMonitorCtl install-service\' ')


def rest_admin_pass():
    reset_admin_password()


def get_help():

    optional_for_service_start = 'optional arguments are --port=<PORRT>, and --local-listening=true (in case you want to access only on 127.0.0.1 and not globaly on 0.0.0.0)'

    print('')
    print('')
    print('-------------')
    print('use \'pyWebCamMonitorCtl install-service\' to install the app as a service')
    print(optional_for_service_start)
    print('Another optional is --user-root=true in case you want the service user to run under root otherwise it will run under the user executing the command')
    print('You can reuse this command to install the service with different optional arguments like --port , --local-listening, --user')
    print('-------------')
    print('use \'pyWebCamMonitorCtl reset-admin-password\' to reset the admin password of the App, use admin:admin to login afterwards')
    print('-------------')
    print('use \'pyWebCamMonitorCtl start\' to start the application if you don\'t want to install it as a service')
    print(optional_for_service_start)
    print('-------------')
    print('use \'pyWebCamMonitorCtl stop\' to stop the application if you don\'t want to install it as a service')
    print('')
    print('')


def _find_prog():
    pyWebCamWebServerMonitor_bin = subprocess.run(
        "ps -ef | grep python  | grep pyWebCamWebServerMonitor | grep -v grep", shell=True, capture_output=True, close_fds=True)
    output = str(pyWebCamWebServerMonitor_bin.stdout.decode("utf-8"))
    return output


def start_prog(args):
    port = args.port
    is_local = (str(args.local_listening).lower() == 'true')
    ip_serve = ('', '--host=127.0.0.1')[is_local]
    find_output = _find_prog()
    if 'pyWebCamWebServerMonitor' in find_output:
        print('pyWebCamWebServerMonitor is already started')
        return
    waitress_bin = which('waitress-serve')
    if waitress_bin is None:
        print('Cound not start pyWebCamWebServerMonitor, waitress-serve was not found on system')
        return
    start_cmd = "{} --port={} {} --threads=6 --call 'pyWebCamWebServerMonitor:create_app'".format(
        waitress_bin, str(port), ip_serve)
    prog_bin = subprocess.Popen('exec ' + start_cmd, shell=True, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=None, close_fds=True)
    if prog_bin is None:
        print(
            '\033[91m ERROR\033[00m: Application process command [ {} ] failed to start'.format(start_cmd))
    else:
        if is_local:
            print('\033[94m INFO\033[00m: Application has started, lisetning only local on http://127.0.0.1:{} '.format(port))
        else:
            print('\033[94m INFO\033[00m: Application has started, listening on 0.0.0.0:{} visit http://127.0.0.1:{} or http://<HOST-IP>:{}'.format(port, port, port))
        return


def stop_prog():

    find_output = _find_prog()
    if 'pyWebCamWebServerMonitor' in find_output:
        try:
            bin_pid = int(
                re.search(r'( [0-9]+ )', find_output).group(0).rstrip().lstrip())
            os.kill(bin_pid, signal.SIGTERM)
            print('\033[92m OK\033[00m: pyWebCamWebServerMonitor has recived the signal to terminate')
        except Exception:
            print(find_output)
            print(re.search(r'( [0-9]+ )', find_output, re.M))
            print('\033[91m ERROR\033[00m: Could not kill pyWebCamWebServerMonitor')
    else:
        print('\033[94m INFO\033[00m: pyWebCamWebServerMonitor is not started')
        return


def commands_main():
    parser = argparse.ArgumentParser(prog='pyWebCamWebServerMonitor')
    parser.add_argument(
        "command", nargs='?', help="command to execute use \'pyWebCamMonitorCtl help\' to see all comands")
    parser.add_argument(
        '--port', type=int, help="Optional argument to set port when starting the program or installing the service")
    parser.add_argument('--local-listening', type=str,
                        help="Optional argument to set if the listening is only on 127.0.0.1 when starting the program or installing the service, --local-listening=true")
    parser.add_argument('--user-root', type=str,
                        help="Optional argument to set the user of the installed service as root, --user-root=true, if it's not specified the service will run under the user who executes the install command")
    parser.set_defaults(command='help', port=6345,
                        local_listening='false', user_root='false')

    args = parser.parse_args()
    if args.command == 'help':
        get_help()
    elif(args.command == 'install-service'):
        install_as_sys_service(args)
    elif(args.command == 'reset-admin-password'):
        rest_admin_pass()
    elif(args.command == 'start'):
        start_prog(args)
    elif(args.command == 'stop'):
        stop_prog()
    else:
        print('No valid commands found type \'pyWebCamMonitorCtl help\' for available commands!')
