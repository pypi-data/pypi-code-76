# Built-in
import time
import uuid
from typing import List

# Home-brew
from bitex.response import BitexResponse, KeyValuePairs, Triple


class KrakenResponse(BitexResponse):
    """Customized BitEx Response for Kraken."""

    @property
    def dtype(self):
        requested_url = self.request.url.lower()
        if "public/depth" in requested_url:
            return "book"
        elif "public/trades" in requested_url:
            return "trades"
        elif "public/ticker" in requested_url:
            return "ticker"

    def select_kv_wrangler(self):
        return getattr(self, f"wrangle_{self.dtype}_kv")

    def select_triples_wrangler(self):
        return getattr(self, f"wrangle_{self.dtype}_triples")

    def key_value_dict(self) -> List[KeyValuePairs]:
        """Return the data of the response as a list dictionaries.

        This provides the data as a dict of key-value pairs, which is ready for
        consumption by libraries such as pandas::

            [
                {
                <key>: <value>,
                <key>: <value>,
                ...
                },
                ...
            }

        There are certain keys which will always be present:

            - `pair`: denotes the crytpo pair this kv dict belongs to
            - `received`: denotes the timestamp at the time of creation of this Response, specifically, when
                    the instance's :meth:`BitexResponse.__init__` method was first called.
        """
        kv_data = []
        kv_wrangler_method = self.select_kv_wrangler()
        for pair, data in self.json()["result"].items():
            kv_data.extend(kv_wrangler_method(pair, data))
        return kv_data

    def triples(self) -> List[Triple]:
        """Return the data of the response in three-column layout.

        Data is returned as a list of 3-item tuples::

            [
                (<timestamp>, <key>, <value>),
                (<timestamp>, <key>, <value>),
                ...
            ]

        ..note::

            The `timestamp` field in the above example corresponds to the timestamp of the data as given by Kraken. For
            the time of reception, check the `received` key, which is always delivered as well.

        """
        triples = []
        triples_wrangler_method = self.select_triples_wrangler()
        for pair, data in self.json()["result"].items():
            triples.extend(triples_wrangler_method(pair, data))
        return triples

    def wrangle_ticker_kv(self, pair, d) -> List[KeyValuePairs]:
        """Wrangle ticker data into triples or TKV format.

        From the `ticker endpoint documentation`_, the data layout is as follows::

            <pair_name> = pair name
                a = ask array(<price>, <whole lot volume>, <lot volume>),
                b = bid array(<price>, <whole lot volume>, <lot volume>),
                c = last trade closed array(<price>, <lot volume>),
                v = volume array(<today>, <last 24 hours>),
                p = volume weighted average price array(<today>, <last 24 hours>),
                t = number of trades array(<today>, <last 24 hours>),
                l = low array(<today>, <last 24 hours>),
                h = high array(<today>, <last 24 hours>),
                o = today's opening price

        .. _ticker endpoint documentation: https://www.kraken.com/features/api#get-ticker-info
        """
        open_price = d["o"]
        high, high_24 = d["h"]
        low, low_24h = d["l"]
        trades, trades_24h = d["t"]
        vwap, vwap_24h = d["p"]
        vol, vol_24h = d["v"]
        last_price, last_size = d["c"]
        bid_price, _, bid_size = d["b"]
        ask_price, _, ask_size = d["a"]
        return [
            {
                "uid": uuid.uuid4(),
                "received": self.received,
                "pair": pair,
                "open": open_price,
                "high": high,
                "high_24h": high_24,
                "low": low,
                "low_24h": low_24h,
                "trades": trades,
                "trades_24h": trades_24h,
                "vwap": vwap,
                "vwap_24h": vwap_24h,
                "vol": vol,
                "vol_24h": vol_24h,
                "last_price": last_price,
                "last_size": last_size,
                "bid_price": bid_price,
                "bid_size": bid_size,
                "ask_price": ask_price,
                "ask_size": ask_size,
            }
        ]

    def wrangle_trades_kv(self, pair, d) -> List[KeyValuePairs]:
        """Wrangle pair trade data into kv dict.

        From the `trades endpoint documentation`_, the data layout is as follows::

            <pair_name> = pair name
                array of array entries(<price>, <volume>, <time>, <buy/sell>, <market/limit>, <miscellaneous>)
            last = id to be used as since when polling for new trade data

        .. _trades endpoint documentation: https://www.kraken.com/features/api#get-recent-trades
        """
        keys = ["price", "size", "ts", "side", "type", "misc"]
        kv_data = []
        meta_data = {"received": self.received, "pair": pair}
        for trade in d:
            wrangled = {k: str(v) for k, v in zip(keys, trade)}
            wrangled.update(meta_data)
            wrangled.update({"uid": uuid.uuid4()})
            kv_data.append(wrangled)
        return kv_data

    def wrangle_book_kv(self, pair, d) -> List[KeyValuePairs]:
        """Wrangle pair trade data into kv dict.

        From the `book endpoint documentation`_, the data layout is as follows::

            <pair_name> = pair name
                asks = ask side array of array entries(<price>, <volume>, <timestamp>)
                bids = bid side array of array entries(<price>, <volume>, <timestamp>)

        .. _book endpoint documentation: https://www.kraken.com/features/api#get-order-book
        """
        keys = ["price", "size", "ts"]
        kv_data = []
        for side in ("bids", "asks"):
            meta_data = {"side": side[:-1], "received": self.received}  # Strip trailing 's'
            for i, order in enumerate(d[side]):
                wrangled = {k: str(v) for k, v in zip(keys, order)}
                wrangled.update(meta_data)
                wrangled.update({"uid": uuid.uuid4()})
            kv_data.append(wrangled)
        return kv_data

    def wrangle_ticker_triples(self, pair, d) -> List[Triple]:
        """Wrangle ticker data for a specific crypto pair into triples."""
        triples = []
        processed_data, *_ = self.wrangle_ticker_kv(pair, d)
        uid = processed_data.pop("uid")
        for k, v in processed_data.items():
            triples.append([uid, k, v])
        return triples

    def wrangle_book_or_trades_triples(self, preprocessed: List[KeyValuePairs]):
        """Wrangle trades or book data for a specific crypto pair into triples."""
        triples = []
        for kv_dict in preprocessed:
            uid = kv_dict.pop("uid")
            kv_dict_as_triples = [[uid, k, v] for k, v in kv_dict.items()]
            triples.extend(kv_dict_as_triples)
        return triples

    def wrangle_trades_triples(self, pair, d) -> List[Triple]:
        """Wrangle trades data for a specific crypto pair into triples."""
        trade_kvs: List[KeyValuePairs] = self.wrangle_trades_kv(pair, d)
        return self.wrangle_book_or_trades_triples(trade_kvs)

    def wrangle_book_triples(self, pair, d) -> List[Triple]:
        """Wrangle book data for a specific crypto pair into triples."""
        book_kvs: List[KeyValuePairs] = self.wrangle_book_kv(pair, d)
        return self.wrangle_book_or_trades_triples(book_kvs)
