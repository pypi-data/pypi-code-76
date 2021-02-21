#!/usr/bin/env python3

# Standard libraries
from datetime import datetime
from os import access, environ, W_OK
from time import localtime, strftime, time

# Modules libraries
from update_checker import pretty_date, UpdateChecker

# Components
from ..package.bundle import Bundle
from ..prints.boxes import Boxes
from ..prints.colors import Colors
from ..system.platform import Platform
from .version import Version

# Updates class
class Updates:

    # Members
    __enabled = False
    __name = None
    __settings = None

    # Constructor
    def __init__(self, name, settings):

        # Initialize members
        self.__name = name
        self.__settings = settings

        # Acquire enabled
        enabled = self.__settings.get('updates', 'enabled')
        if not enabled:
            enabled = 1
            self.__settings.set('updates', 'enabled', enabled)

        # Check enabled
        self.__enabled = int(enabled) == 1 and (Bundle.ENV_UPDATES_DISABLE not in environ
                                                or
                                                not environ[Bundle.ENV_UPDATES_DISABLE])

    # Message
    def __message(self, offline=False, older=False, available=None, date=None):

        # Create message box
        box = Boxes()

        # Acquire current version
        version = Version.get()

        # Evaluate same version
        same = available == version

        # Version message prefix
        version_prefix = '%sVersion: %s%s %s%s' % (
            Colors.YELLOW_LIGHT, Colors.BOLD, self.__name, Colors.RED if not offline
            and available and not older and not same else Colors.GREEN, version)

        # Offline version message
        if offline:
            box.add('%s %snot found, network might be down' % ( #
                version_prefix, Colors.BOLD))

        # Updated version message
        elif same:
            box.add('%s %swas released %s%s!' % ( #
                version_prefix, Colors.BOLD, pretty_date(date), Colors.BOLD))

        # Older version message
        elif older:
            box.add('%s %snewer than %s%s %sfrom %s%s!' % ( #
                version_prefix, Colors.BOLD, Colors.RED, available, Colors.BOLD,
                pretty_date(date), Colors.BOLD))

        # Newer version message
        else:
            box.add('%s %supdated %s to %s%s%s!' % ( #
                version_prefix, Colors.BOLD, pretty_date(date), Colors.GREEN, available,
                Colors.BOLD))

        # Changelog message
        box.add('%sChangelog: %s%s/-/tags' % ( #
            Colors.YELLOW_LIGHT, Colors.CYAN, Bundle.REPOSITORY))

        # Update message
        if available:
            writable = access(__file__, W_OK)
            box.add('%sUpdate: %sRun %s%spip3 install -U %s' % ( #
                Colors.YELLOW_LIGHT, Colors.BOLD, Colors.GREEN,
                'sudo ' if Platform.IS_USER_SUDO or not writable else '', self.__name))

        # Print message box
        box.print()

    # Checker
    def check(self, older=False):

        # Reference version
        version = '0.0.0' if older else Version.get()

        # Fake test updates
        if Bundle.ENV_UPDATES_FAKE in environ:
            available = environ[Bundle.ENV_UPDATES_FAKE]
            if available >= version:

                # Show updates message
                release_date = datetime.utcfromtimestamp(Bundle.RELEASE_FIRST_TIMESTAMP)
                self.__message(older=older, available=available, date=release_date)
                return True

        # Check if not offline
        if not Bundle.ENV_UPDATES_OFFLINE in environ:

            # Check for updates
            check = UpdateChecker(bypass_cache=True).check(self.__name, version)
            if check:

                # Show updates message
                self.__message(older=older, available=check.available_version,
                               date=check.release_date)
                return True

        # Older offline failure
        if older:

            # Show offline message
            self.__message(offline=True)
            return True

        # Result
        return False

    # Daily
    @property
    def daily(self):

        # Acquire updates check last timestamp
        last = self.__settings.get('updates', 'last_timestamp')

        # Fake test updates
        if Bundle.ENV_UPDATES_DAILY in environ:
            last = None

        # Handle daily checks
        current = int(time())
        if not last or strftime('%Y-%m-%d', localtime(current)) != strftime(
                '%Y-%m-%d', localtime(int(last))):
            self.__settings.set('updates', 'last_timestamp', current)
            return True

        # Default fallback
        return False

    # Enabled
    @property
    def enabled(self):
        return self.__enabled
