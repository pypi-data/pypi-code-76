"""
Copied from raven-python. Used for
`DjangoIntegration(transaction_fron="raven_legacy")`.
"""

from __future__ import absolute_import

import re

from sentry_sdk._types import MYPY

if MYPY:
    from django.urls.resolvers import URLResolver
    from typing import Dict
    from typing import List
    from typing import Optional
    from django.urls.resolvers import URLPattern
    from typing import Tuple
    from typing import Union
    from re import Pattern

try:
    from django.urls import get_resolver
except ImportError:
    from django.core.urlresolvers import get_resolver


def get_regex(resolver_or_pattern):
    # type: (Union[URLPattern, URLResolver]) -> Pattern[str]
    """Utility method for django's deprecated resolver.regex"""
    try:
        regex = resolver_or_pattern.regex
    except AttributeError:
        regex = resolver_or_pattern.pattern.regex
    return regex


class RavenResolver(object):
    _optional_group_matcher = re.compile(r"\(\?\:([^\)]+)\)")
    _named_group_matcher = re.compile(r"\(\?P<(\w+)>[^\)]+\)+")
    _non_named_group_matcher = re.compile(r"\([^\)]+\)")
    # [foo|bar|baz]
    _either_option_matcher = re.compile(r"\[([^\]]+)\|([^\]]+)\]")
    _camel_re = re.compile(r"([A-Z]+)([a-z])")

    _cache = {}  # type: Dict[URLPattern, str]

    def _simplify(self, pattern):
        # type: (str) -> str
        r"""
        Clean up urlpattern regexes into something readable by humans:

        From:
        > "^(?P<sport_slug>\w+)/athletes/(?P<athlete_slug>\w+)/$"

        To:
        > "{sport_slug}/athletes/{athlete_slug}/"
        """
        # remove optional params
        # TODO(dcramer): it'd be nice to change these into [%s] but it currently
        # conflicts with the other rules because we're doing regexp matches
        # rather than parsing tokens
        result = self._optional_group_matcher.sub(lambda m: "%s" % m.group(1), pattern)

        # handle named groups first
        result = self._named_group_matcher.sub(lambda m: "{%s}" % m.group(1), result)

        # handle non-named groups
        result = self._non_named_group_matcher.sub("{var}", result)

        # handle optional params
        result = self._either_option_matcher.sub(lambda m: m.group(1), result)

        # clean up any outstanding regex-y characters.
        result = (
            result.replace("^", "")
            .replace("$", "")
            .replace("?", "")
            .replace("//", "/")
            .replace("\\", "")
        )

        return result

    def _resolve(self, resolver, path, parents=None):
        # type: (URLResolver, str, Optional[List[URLResolver]]) -> Optional[str]

        match = get_regex(resolver).search(path)  # Django < 2.0

        if not match:
            return None

        if parents is None:
            parents = [resolver]
        elif resolver not in parents:
            parents = parents + [resolver]

        new_path = path[match.end() :]
        for pattern in resolver.url_patterns:
            # this is an include()
            if not pattern.callback:
                match_ = self._resolve(pattern, new_path, parents)
                if match_:
                    return match_
                continue
            elif not get_regex(pattern).search(new_path):
                continue

            try:
                return self._cache[pattern]
            except KeyError:
                pass

            prefix = "".join(self._simplify(get_regex(p).pattern) for p in parents)
            result = prefix + self._simplify(get_regex(pattern).pattern)
            if not result.startswith("/"):
                result = "/" + result
            self._cache[pattern] = result
            return result

        return None

    def resolve(
        self,
        path,  # type: str
        urlconf=None,  # type: Union[None, Tuple[URLPattern, URLPattern, URLResolver], Tuple[URLPattern]]
    ):
        # type: (...) -> str
        resolver = get_resolver(urlconf)
        match = self._resolve(resolver, path)
        return match or path


LEGACY_RESOLVER = RavenResolver()
