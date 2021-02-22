"""
    Main app components definition.
"""
import signal
import sys

from pkg_resources import get_distribution
from cliff.app import App
from cliff.commandmanager import CommandManager

from digicloud.cli import signal_handler
from .managers import ConfigManager, Session


class DigicloudApp(App):
    """Overwrite ``cliff.app.App`` class.

    Make possibility to further extension and overwrite methods.
    """

    def __init__(self):
        command_manager = CommandManager('digicloud.cli')
        super(DigicloudApp, self).__init__(
            description='Digicloud CLI',
            version=get_distribution('digicloud').version,
            command_manager=command_manager,
            deferred_help=True
        )
        self.config = ConfigManager(self.LOG)
        # Http session from requests.Session.
        base_url = self.config['BASE_URL']
        self.session = self.config.get('SESSION', Session(base_url))

    def initialize_app(self, argv):
        signal.signal(signal.SIGINT, signal_handler.interrupt_handler)
        self.LOG.debug('Initialize session')
        self.setup_session()

    def setup_session(self):
        self.session.base_url = self.config['BASE_URL']

        if self.config.get('AUTH_HEADERS'):
            auth_headers = self.config['AUTH_HEADERS']
            self.session.headers.update(auth_headers)
            self.config['SESSION'] = self.session
        else:
            self.config['AUTH_HEADERS'] = {}
        self.config.save()

    def clean_up(self, cmd, result, err):
        """Is invoked after a command runs."""
        self.config.save()
        self.LOG.debug('Configuration saved.')
        if err:
            self.LOG.debug(err)


def main(argv=None):
    """Initialize main ``cliff.app.App`` instance and run.

    Cliff look for this function as a console script entry point.
    """
    if not argv:
        argv = sys.argv[1:]
    if len(argv) == 0:  # Disable interactive mode
        argv = ['--help']  # display --help instead of interactive mode
    return DigicloudApp().run(argv)


if __name__ == '__main__':
    sys.exit(main())
