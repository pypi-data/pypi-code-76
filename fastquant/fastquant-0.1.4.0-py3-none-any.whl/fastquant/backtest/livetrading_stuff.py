
from enum import Enum, auto

class FeedStatus(Enum):
    INIT = auto()
    CONNECTED = auto()
    PAUSED = auto()
    CRASHED = auto()

from typing import List
import numpy as np

class CandleConsumer:
    async def next_candle(self, candle: List[float]) -> None:
        print(f'Next candle: {candle}')

    async def preload_candles(self, candles: List[float]) -> None:
        print(f'Preloading: {candles}')

from typing import Dict, Any

from asyncio import get_event_loop

class OHLCVFeed:
    ''' Feed abstraction, for vendor connection implementations. 
        These typically do not require credentials to get current market data.
        
        Also handles some reconnecting logic. Calls back to CandleConsumer on each tick.'''
    def __init__(self, options: Dict[str, Any] = None):
        if not options:
            options = {}

        self._status = FeedStatus.INIT
        self._name = 'OHLCVFeed()'

        self.options = options

        self.frequency_string = options['frequency']
        time_unit = self.frequency_string[-1]
        if time_unit not in ['s', 'm', 'h', 'd']:
            raise ValueError('bad frequency symbol')

        quantity = int(self.frequency_string[:-1])

        if quantity <= 0:
            raise ValueError('bad frequency time quantity')

        v = 1000 * 60 # default minute
        if time_unit == 's':
            v = 1000
        elif time_unit == 'm':
            v = 1000 * 60
        elif time_unit == 'h':
            v = 1000 * 60 * 60
        elif time_unit == 'd':
            v = 1000 * 60 * 60 * 60

        self.frequency_unix_time = v * quantity

        self.symbol_pair = options['symbol_pair']
        self.preload_ticks = 0
        if 'preload_ticks' in options:
            self.preload_ticks = options['preload_ticks']

    async def _connect(self) -> FeedStatus:
        return FeedStatus.CONNECTED

    async def preload(self):
        pass

    async def wait_for_data(self):
        pass

    async def _reconnect(self) -> FeedStatus:
        r = await self._connect()
        if not r == FeedStatus.CONNECTED:
            return FeedStatus.CRASHED

        await self.preload()
        return FeedStatus.CONNECTED

    async def disconnect(self):
        self._status = FeedStatus.INIT

    async def connect(self):
        if self._status is FeedStatus.INIT:
            print(f'{self._name}: Connecting')
            self._status = await self._connect()
        elif self._status is FeedStatus.CRASHED:
            print(f'{self._name}: Reconnecting')
            self._status = await self._reconnect()

        if self.status is not FeedStatus.CONNECTED:
            print(f'{self._name}: Failed to connect')

        print(f'{self._name}: Connected')

    @property
    def status(self) -> FeedStatus:
        return self._status

    def __del__(self):
        get_event_loop().create_task(self.disconnect()) #TODO: Fix cleanup

    def __str__(self):
        return self._name

##########

from typing import Dict, Any, List

import random, time
from aiohttp import ClientSession

class BinanceFeed(OHLCVFeed):
    WEBSOCKET_URL = 'wss://stream.binance.com:9443/ws'
    API_URL = 'https://api.binance.com/api'

    def __init__(self, options: Dict[str, Any] = None):
        super().__init__(options)
        self._name = "BinanceFeed()"
        self.web = ClientSession()
        self.ws = None

        self.last_t = None

    async def _connect(self):
        self.subscription_id = random.randint(0, 1000)
        self.ws = await self.web.ws_connect(BinanceFeed.WEBSOCKET_URL)

        await self.ws.send_json({
            "method": "SUBSCRIBE",
            "params": [
                f'{self.symbol_pair.lower()}@kline_{self.frequency_string}'
            ],
            "id": self.subscription_id
        })

        result = await self.ws.receive_json()

        if 'id' in result and result['id'] == self.subscription_id:
            return FeedStatus.CONNECTED

        return FeedStatus.CRASHED

    def __json_to_candle(self, result) -> List[float]:
        o = result['k']['o']
        h = result['k']['h']
        l = result['k']['l']
        c = result['k']['c']
        v = result['k']['v']

        return [o, h, l, c, v]

    async def wait_for_data(self):
        print('wait for data')
        t = self.last_t
        result = None

        if t:
            last_time = t
            if type(t) is str:
                last_time = int(t)

            curr_time = int(time.time())
            if curr_time > last_time + self.frequency_unix_time:
                await self.preload()
                return

        # binance sends less than given frequency, so we have to keep 
        # track of when the time frequency changes to next interval, to call back to
        # candle consumer
        while True:
            print('loop tick')
            result = await self.ws.receive_json()
            print('result')
            curr_t = result['k']['t']
            if not t:
                print('t init = curr_t')
                t = curr_t
                continue

            if t != curr_t:
                print('t changed')
                break

            print(f'feed ({t}): {self.__json_to_candle(result)}')

        self.last_t = int(t)
        # self.candle_consumer.next_candle(self.__json_to_candle(result))

    async def preload(self):
        if not self.preload_ticks > 0:
            return

        if self.preload_ticks > 1000:
            # TODO: make this paginate if need more ticks -- I doubt we gonna need more though
            raise ValueError('Binance does not allow more than 1000 look-behind window')

        response = await self.web.get(BinanceFeed.API_URL + '/v3/klines', params={
            'symbol': self.symbol_pair,
            'interval': self.frequency_string,
            'limit': self.preload_ticks
        })

        if response.status != 200:
            raise NotImplementedError('/api/v3/klines returned non 200 status code: {}'.format(await response.text()))

        def __ohlcv_from_row(r):
            return [float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5])]

        d = [__ohlcv_from_row(r) for r in await response.json()]

        # self.candle_consumer.preload_candles(d)

    async def disconnect(self):
        if self.ws:
            await self.ws.close()
            self.ws = None
        super().disconnect()
######
from asyncio import get_event_loop

async def main():

    consumer = CandleConsumer()  # this one just prints
    
   
    feed = BinanceFeed( options= {
        'symbol_pair': 'BTCEUR',
        'frequency': '1m',
        'preload_ticks': 3
    } )

    await feed.connect()
    await feed.preload()

    while True:
        await feed.wait_for_data()

if __name__ == '__main__':
    get_event_loop().run_until_complete(main())

    # TODO: figure out how to compare time from ws and time from preload
    # TODO: visualize loss and candlesticks