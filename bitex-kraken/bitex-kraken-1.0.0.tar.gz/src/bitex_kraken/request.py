# Home-brew
from bitex.request import BitexPreparedRequest

ENDPOINT_MAPPING = {"trades": "Trades", "book": "Depth", "ticker": "Ticker"}

ASSET_MAPPING = {}


class KrakenPreparedRequest(BitexPreparedRequest):
    def prepare(
        self,
        method=None,
        url=None,
        headers=None,
        files=None,
        data=None,
        params=None,
        auth=None,
        cookies=None,
        hooks=None,
        json=None,
    ):
        """Prepares the entire request with the given parameters."""
        matchdict = self.search_url_for_shorthand(url)
        if matchdict.get("exchange").lower() == "kraken":
            # Convert this to the proper URL
            url = self.build_api_url(**matchdict)

        return super(KrakenPreparedRequest, self).prepare(
            method, url, headers, files, data, params, auth, cookies, hooks, json
        )

    def build_api_url(self, instrument=None, endpoint=None, action=None, **_):
        formatted_instrument = self.format_instrument(instrument)
        path = ENDPOINT_MAPPING[endpoint.lower()]
        return f"https://api.kraken.com/0/public/{path}?pair={formatted_instrument}"

    def format_instrument(self, instrument):
        return instrument.lower().replace("btc", "xbt").strip("//")

    def __repr__(self):
        """Extend original class's __repr__."""
        return f"<{self.__class__.__qualname__} [{self.url}]>"
