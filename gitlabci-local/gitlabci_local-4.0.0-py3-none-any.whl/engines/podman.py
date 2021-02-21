#!/usr/bin/env python3

# Standard libraries
from os import environ
from subprocess import DEVNULL, PIPE, Popen, run

# Components
from ..package.bundle import Bundle
from ..system.platform import Platform

# Podman class
class Podman:

    # Members
    __binary = 'podman'

    # Constructor
    def __init__(self):

        # Configure binary
        if Bundle.ENV_PODMAN_BINARY_PATH in environ:
            self.__binary = environ[Bundle.ENV_PODMAN_BINARY_PATH]

        # Check engine support
        try:
            result = self.__exec(['system', 'info'], True)
            if result.returncode != 0:
                raise ModuleNotFoundError()
        except FileNotFoundError:
            raise ModuleNotFoundError() from None

    # Internal execution
    def __exec(self, arguments, quiet=False):
        if quiet:
            return run([self.__binary] + arguments, check=False, stdout=DEVNULL,
                       stderr=DEVNULL)
        return run([self.__binary] + arguments, check=False, stdout=PIPE, stderr=PIPE)

    # Internal watcher
    def __watch(self, arguments):
        return iter(Popen([self.__binary] + arguments, stdout=PIPE).stdout.readline, b'')

    # Command exec
    def cmd_exec(self):

        # Result
        if Platform.IS_USER_SUDO:
            return 'sudo podman exec -it'
        return 'podman exec -it'

    # Exec
    def exec(self, container, command):

        # Adapt command
        if isinstance(command, str): # pragma: no cover
            command = [command]

        # Execute command in container
        return self.__exec(['exec', container] + command)

    # Get
    def get(self, image):

        # Validate image exists
        result = self.__exec([
            'inspect',
            '--type',
            'image',
            '--format',
            'exists',
            image,
        ], True)

        # Pull missing image
        if result.returncode != 0:
            self.pull(image)

    # Logs
    def logs(self, container):

        # Return logs stream
        return self.__watch(['logs', '--follow', container])

    # Name
    def name(self, container):

        # Result
        result = self.__exec(
            ['inspect', '--type', 'container', '--format', '{{.Name}}', container])
        return result.stdout.strip().decode('utf-8') if result.returncode == 0 else ''

    # Pull
    def pull(self, image, force=False):

        # Header
        print('Pulling from %s' % (image))
        Platform.flush()

        # Force image removal
        if force:
            self.rmi(image)

        # Pull image with logs stream
        result = self.__exec(['pull', image])

        # Layer completion logs
        if result.returncode == 0:
            result = self.__exec([
                'inspect',
                '--type',
                'image',
                '--format',
                '{{.Id}}',
                image,
            ])
            print('Digest: %s' % (result.stdout.strip().decode('utf-8')))
            print('Status: Image is up to date for %s' % (image))
        else:
            print('Status: Image not found for %s' % (image))
            Platform.flush()
            raise FileNotFoundError(result.stderr.decode('utf-8').replace('\\n', '\n'))

        # Footer
        print(' ')
        Platform.flush()

    # Remove
    def remove(self, container):

        # Remove container
        self.__exec(['rm', '--force', container])

    # Remove image
    def rmi(self, image):

        # Remove image
        result = self.__exec([
            'inspect',
            '--type',
            'image',
            '--format',
            'exists',
            image,
        ], True)
        if result.returncode == 0:
            self.__exec([
                'rmi',
                image,
            ])

    # Run
    def run(self, image, command, entrypoint, variables, network, volumes, directory):

        # Variables
        args_command = []
        args_entrypoint = []
        args_env = []
        args_run = []
        args_volumes = []

        # Adapt command
        if isinstance(command, list): # pragma: no cover
            args_command = command
        elif isinstance(command, str):
            args_command = [command]

        # Adapt entrypoint
        if isinstance(entrypoint, list):
            if len(entrypoint) > 1:
                args_command = [' '.join(args_command)]
                args_command[0:0] = entrypoint[1:]
            entrypoint = entrypoint[0]
        if isinstance(entrypoint, str):
            args_entrypoint = ['--entrypoint', entrypoint]

        # Adapt mounts
        if volumes and isinstance(volumes.get(), dict):
            for volume in volumes.get().items():
                options = ''
                if volume[1]['mode'] == 'ro':
                    options += ':ro'
                elif volume[1]['mode'] == 'rw':
                    options += ':rw'
                args_volumes += [
                    '--volume',
                    '%s:%s%s' % (volume[0], volume[1]['bind'], options)
                ]

        # Adapt variables
        for variable in variables:
            args_env.extend(['--env', '%s=%s' % (variable, variables[variable])])

        # Prepare arguments
        args_run += ['create']
        args_run += args_entrypoint
        args_run += args_env
        args_run += ['--tty']
        args_run += args_volumes
        if network:
            args_run += ['--network', network]
        args_run += ['--privileged']
        args_run += ['--security-opt', 'label=disable']
        args_run += ['--workdir', directory]
        args_run += [image]
        args_run += args_command

        # Create container image
        result = self.__exec(args_run)
        if result.returncode == 0:
            container = result.stdout.strip().decode('utf-8')

        # Handle failures
        else:
            raise NotImplementedError(result.stderr.decode('utf-8').replace('\\n', '\n'))

        # Start container
        self.__exec(['start', container])

        # Result
        return container

    # Sockets
    def sockets(self, variables, volumes):
        pass

    # Stop
    def stop(self, container, timeout):

        # Stop container
        self.__exec(['stop', '--time', str(timeout), container])

    # Supports
    def supports(self, container, binary):

        # Validate binary support
        result = self.exec(container, ['whereis', binary])

        # Result
        return result.returncode == 0

    # Wait
    def wait(self, container):

        # Wait container
        result = self.__exec(['wait', container])

        # Result
        return int(result.stdout.strip()) == 0 if result.returncode == 0 else False
