"""Setup inversion-of-control through entrypoints."""
import pkg_resources

from . import provider


IOC_ENTRYPOINT_NAME = 'ioc.providers'

IS_CONFIGURED = False


def get_providers():
    """Return the mapping of inversion-of-control providers and their
    entrypoints.
    """
    return [
        (entry_point.name, entry_point.load())
        for entry_point
        in pkg_resources.iter_entry_points('ioc.providers')
    ]


def setup():
    """Load all :term:`Dependency Providers` and start setting up the
    dependencies container.
    """
    global IS_CONFIGURED
    if IS_CONFIGURED:
        return

    for name, module in get_providers():
        if not hasattr(module, 'setup_ioc'):
            continue
        module.setup_ioc()

    IS_CONFIGURED = True


def teardown():
    """Tear down the configured dependencies."""
    global IS_CONFIGURED
    provider.teardown()
    IS_CONFIGURED = False
