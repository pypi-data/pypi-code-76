from typing import Tuple

from django.conf import settings

__all__ = (
    'REDIRECT_TO_QUERY_PARAMETER',
    'LANGUAGE_QUERY_PARAMETER',
    'REDIRECT_EXCLUDE_PREFIXES',
    'DEFAULT_REDIRECT_LANGUAGE',
    'VISITED_SESSION_KEY'
)


REDIRECT_TO_QUERY_PARAMETER: str = getattr(
    settings,
    'LANGUAGE_TOOLS_REDIRECT_TO_QUERY_PARAMETER',
    'redirect_to'
)


LANGUAGE_QUERY_PARAMETER: str = getattr(
    settings,
    'LANGUAGE_TOOLS_QUERY_PARAMETER',
    'language'
)

REDIRECT_EXCLUDE_PREFIXES: 'Tuple' = getattr(
    settings,
    'LANGUAGE_TOOLS_REDIRECT_EXCLUDE_PREFIXES',
    ()
)

DEFAULT_REDIRECT_LANGUAGE: str = getattr(
    settings,
    'LANGUAGE_TOOLS_DEFAULT_REDIRECT_LANGUAGE',
    settings.LANGUAGE_CODE
)

VISITED_SESSION_KEY: str = getattr(
    settings,
    'LANGUAGE_TOOLS_VISITED_SESSION_KEY',
    'language-tools:visited'
)
