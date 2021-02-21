#!/usr/bin/env python3

# Components
from ..system.platform import Platform
from ..types.paths import Paths

# Volumes class
class Volumes:

    # Constants
    LOCAL_FLAG = '.local:'

    # Members
    __volumes = None

    # Constructor
    def __init__(self):
        self.__volumes = dict()

    # Add
    def add(self, source, target, mode, override):

        # Handle overrides
        if target in [self.__volumes[volume]['bind'] for volume in self.__volumes]:
            if not override:
                return

            duplicates = [
                volume for volume in self.__volumes
                if self.__volumes[volume]['.source'] == source
                and self.__volumes[volume]['bind'] == target
            ]
            if duplicates:
                self.__volumes.pop(duplicates[0])

        # Adapt source to allow duplicates
        while source in self.__volumes:
            if Platform.IS_WINDOWS: # pragma: no cover
                source = source + Platform.PATH_SEPARATOR + '.'
            else:
                source = Platform.PATH_SEPARATOR + '.' + source

        # Add volume binding
        self.__volumes[source] = { #
            'bind': target,
            'mode': mode,
            '.source': source
        }

    # Get
    def get(self):
        return self.__volumes

    # Parse
    @staticmethod
    def parse(volume):

        # Invalid volume
        if not volume:
            raise ValueError('Empty volume parameter cannot be parsed')

        # Relative volume
        if 1 <= len(volume) <= 2:
            return [volume]

        # Variables
        volume_node = ''
        volume_nodes = []

        # Iterate through volume
        for char in volume + '\0':

            # Detect Windows drive
            if char == ':' and len(volume_node) == 1 and volume_node[0].isalpha():
                volume_node += char # pragma: no cover

            # Detect separator or end
            elif char in (':', ';', '\0'):
                volume_nodes += [Paths.translate(volume_node)]
                volume_node = ''

            # Append to volume node
            else:
                volume_node += char

        # Result
        return volume_nodes
