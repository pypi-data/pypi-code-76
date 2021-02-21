#!/usr/bin/env python3

# Standard libraries
from enum import Enum

# Components
from . import docker, podman

# Backend enumeration
class Backend(Enum):
    DOCKER = 1
    PODMAN = 2
    UNKNOWN = 3

# Names enumeration
class Names:

    # Constants
    AUTO = 'auto'
    DOCKER = 'docker'
    PODMAN = 'podman'

    # Defaults
    DEFAULTS = [
        PODMAN,
        DOCKER,
    ]

    # Getter
    @staticmethod
    def get(override):

        # Adapt override
        override = override.lower() if override else None

        # Handle engine overrides
        if override:
            auto = False
            names = []
            overrides = override.split(',')
            for item in overrides:
                if item:
                    if Names.AUTO.startswith(item):
                        auto = True
                    else:
                        names += [
                            name for name in Names.DEFAULTS if name.startswith(item)
                        ]
            if auto or override[-1] == ',':
                names = names + Names.DEFAULTS
            names = list(dict.fromkeys(names))

        # Use engine defaults
        else:
            names = Names.DEFAULTS

        # Result
        return names

# Supported engines
def supported():
    return [Names.AUTO] + Names.DEFAULTS

# Engine class
class Engine:

    # Members
    __engine = None
    __name = None

    # Constructor
    def __init__(self, options):

        # Acquire engine names
        names = Names.get(options.engine)

        # Iterate through names
        for name in names:

            # Podman engine detection
            if name == Names.PODMAN:
                try:
                    self.__engine = podman.Podman()
                    self.__name = Names.PODMAN
                    break
                except (KeyboardInterrupt, ModuleNotFoundError):
                    self.__engine = None

            # Docker engine detection
            elif name == Names.DOCKER:
                try:
                    self.__engine = docker.Docker()
                    self.__name = Names.DOCKER
                    break
                except (KeyboardInterrupt, ModuleNotFoundError):
                    self.__engine = None

        # Unknown engine fallback
        if not self.__engine:
            raise NotImplementedError('Unknown or unsupported container engine...')

    # Command exec
    def cmd_exec(self):
        return self.__engine.cmd_exec()

    # Exec
    def exec(self, container, command): # pragma: no cover
        return self.__engine.exec(container, command)

    # Get
    def get(self, image):
        self.__engine.get(image)

    # Logs
    def logs(self, container):
        return self.__engine.logs(container)

    # Name
    def name(self, container=None):

        # Container name
        if container:
            return self.__engine.name(container)

        # Engine name
        return self.__name

    # Pull
    def pull(self, image, force=False):
        self.__engine.pull(image, force=force)

    # Remove
    def remove(self, container):
        self.__engine.remove(container)

    # Remove image
    def rmi(self, image):
        self.__engine.rmi(image)

    # Run
    def run(self, image, command, entrypoint, variables, network, volumes, directory):
        return self.__engine.run(image, command, entrypoint, variables, network, volumes,
                                 directory)

    # Sockets
    def sockets(self, variables, volumes):
        self.__engine.sockets(variables, volumes)

    # Stop
    def stop(self, container, timeout):
        self.__engine.stop(container, timeout)

    # Supports
    def supports(self, container, binary):
        return self.__engine.supports(container, binary)

    # Wait
    def wait(self, container):
        return self.__engine.wait(container)
