from broker.base import Request


class BrokerV3Client(Request):

    API_VERSION = 'v3'
    QUOTE_API_VERSION = 'v3'

    def ping(self):
        return self._get('ping', version='v3')

    def time(self):
        return self._get('time', version='v3')

    def depth(self, symbol, limit=100):
        """
        Market Data endpoints
        """
        params = {
            'symbol': symbol,
            'limit': limit,
        }
        return self._quote_get('depth', params=params)

    def trades(self, symbol, limit=100):
        """
        Recent trades list
        """
        params = {
            'symbol': symbol,
            'limit': limit,
        }
        return self._quote_get('trades', params=params)

    def klines(self, symbol, interval='1m', start_time='', end_time='', limit=100):
        """
        Kline/Candlestick data
        """
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_time,
            'endTime': end_time,
            'limit': limit,
        }
        return self._quote_get('klines', params=params)

    def ticker_24hr(self, symbol=''):
        """
        24hr ticker price change statistics
        """
        params = {
            'symbol': symbol,
        }
        return self._quote_get('ticker/24hr', params=params)

    def ticker_price(self, symbol=''):
        """
        Symbol price ticker
        """
        params = {
            'symbol': symbol,
        }
        return self._quote_get('ticker/price', params=params)

    # def book_ticker(self, symbol=''):
    #     """
    #     Symbol order book ticker
    #     """
    #     params = {
    #         'symbol': symbol,
    #     }
    #     return self._quote_get('ticker/bookTicker', params=params)

    def order_new(self, symbol, quantity, order_type, order_side, time_in_force='GTC', price='', client_order_id='',
                  trigger_price='', trigger_condition=''):
        """
        New order  (TRADE)
        :param symbol: symbol name
        :param quantity: order quantity
        :param order_type: order type. `LIMIT` `MARKET` `LIMIT_MAKER` `CONDITION_LIMIT` `CONDITION_MARKET`
        :param order_side: order side. `BUY` `SELL`
        :param time_in_force: `GTC` `FOK`
        :param price: order price
        :param client_order_id: client order id
        :param trigger_price: trigger price for condition order
        :param trigger_condition: `GTE` `LTE`
        :return:
        """
        params = {
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'orderType': order_type,
            'orderSide': order_side,
            'timeInForce': time_in_force,
            'clientOrderId': client_order_id,
            'triggerPrice': trigger_price,
            'triggerCondition': trigger_condition,
        }
        return self._post('order', signed=True, version='v3', data=params)

    def order_get(self, order_id='', client_order_id=''):
        """
        Query order (USER_DATA)
        :param order_id: order id
        :param client_order_id: client order id
        """
        params = {
            'orderId': order_id,
            'clientOrderId': client_order_id
        }
        return self._get('order', signed=True, version='v3', params=params)

    def order_cancel(self, order_id='', client_order_id=''):
        """
        Cancel order (TRADE)
        :param order_id: order id
        :param client_order_id: client order id
        """
        params = {
            'orderId': order_id,
            'clientOrderId': client_order_id
        }
        return self._delete('order', signed=True, version='v3', params=params)

    def open_orders(self, symbol):
        """
        Current open orders (USER_DATA)
        :param symbol: symbol id
        """
        params = {
            'symbol': symbol
        }
        return self._get('openOrders', signed=True, version='v3', params=params)

    def history_orders(self, symbol):
        """
        History open orders (USER_DATA)
        :param symbol: symbol id
        """
        params = {
            'symbol': symbol
        }
        return self._get('historyOrders', signed=True, version='v3', params=params)

    def account(self):
        """
        Account information (USER_DATA)
        """
        return self._get('account', version='v3', signed=True)

    def my_trades(self, symbol):
        """
        Account trade list (USER_DATA)
        """
        params = {
            'symbol': symbol
        }
        return self._get('myTrades', signed=True, version='v3', params=params)
