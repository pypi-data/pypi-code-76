"""Unearthed CLI Authentiation."""
import functools
import logging

from unearthed.core.auth.unearthed_auth import UnearthedAuth
from unearthed.core.auth.unearthed_cognito import UnearthedCognito

logger = logging.getLogger(__name__)

# logger.debug("creating cognito session")
cognito_session = UnearthedCognito()

# logger.debug("creating a requests auth handler")
auth_handler = UnearthedAuth(cognito_session)


def authorize(func):
    """Annotation for Click commands to require valid login."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"checking authorization for {func.__name__} command")
        if cognito_session.is_logged_in():
            return func(*args, **kwargs)
        else:
            print(
                "Command not available, not logged in! Please login via `unearthed login`"
            )

    return wrapper
