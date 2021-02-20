# Built-in
from typing import Any, Dict, Mapping, Tuple, Type, Union

# Third-party
import pluggy
from requests import PreparedRequest, Response
from requests.auth import HTTPBasicAuth

# Home-brew
from bitex_kraken.auth import KrakenAuth
from bitex_kraken.request import KrakenPreparedRequest
from bitex_kraken.response import KrakenResponse

hookimpl = pluggy.HookimplMarker("bitex")


@hookimpl
def announce_plugin() -> Union[
    Tuple[str, Type[HTTPBasicAuth], Type[PreparedRequest], Type[Response]], None
]:
    """Register a plugin's custom classes to :mod:`bitex-framework`.

    By default we return a tuple of :class:`str("base")`, :class:`.HTTPBasicBase`,
    :class:`.PreparedRequest` and :class:`.Response`.
    """
    return "kraken", KrakenAuth, KrakenPreparedRequest, KrakenResponse


@hookimpl
def construct_url_from_shorthand(
    match_dict: Mapping[str, str]
) -> Union[str, Tuple[str, Dict[str, Any]], None]:
    """Attempt to translate the given short-hand to a valid kraken API url.

    If we fail to translate the shorthand, we return None; this will tell the bitex-framework to look elsewhere.
    """
    assert match_dict.get("exchange") == "kraken"
    # instrument = match_dict.get("instrument")
    # endpoint = match_dict.get("endpoint")
    action = match_dict.get("action")

    # Convert Instrument to exchange notation

    # Lookup exchange endpoint for short-hand endpoint/action combination
    if action:
        pass
    else:
        # Lookup exchange endpoint for short-hand endpoint
        pass

    return None


@hookimpl
def format_instrument_for():
    pass


@hookimpl
def format_instrument_from():
    pass
