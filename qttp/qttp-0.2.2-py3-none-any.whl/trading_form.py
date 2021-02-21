import ccxt
from pprint import pprint

class Forms:
    def __init__(self, *args, **kwargs):
        self.api.apiKey = access
        self.api.secret = secret
        self.market = market

    def form_01(self, ase):
        print(ase)
        print(self.__ask_price(0))
        print(self.__bid_price(0))
        print(self.__amount(ase))

    def __signal(self):
        signal = self.strategy(self.df).iloc[-1, -2]
        return signal

    def __cancel(self):
        order_ids = self.__order_ids()
        for order_id in order_ids:
            self.api.cancel_order(order_id)

    def __order_ids(self):
        try:
            orders = self.api.fetchOpenOrders()
            order_ids = [order['info']['order_id'] for order in orders]

        except IndexError as e:
            order_ids = []
        return order_ids

    def __ask_price(self, num):
        return self.__orderbook()['asks'][0][num]

    def __bid_price(self, num):
        return self.__orderbook()['bids'][0][num]

    def __orderbook(self):
        if self.market.startswith("KRW-"):
            self.market = self.market[-3:] + "/" + self.market[:3]
        return self.api.fetchOrderBook(self.market)

    def __amount(self, ase, price):
        invest_equity = ase['equity'] * ratio_to_invest
        amount = round(invest_equity / price, 4)
        return amount

    def __open_price(self):
        return self.df.iloc[-1, 1]


class Deribit(Forms):
    def __init__(self, *args, **kwargs):
        self.api = ccxt.deribit()
        super().__init__(*args, **kwargs)
        instrument_name = {'instrument_name' : self.market,}
        currency = {'currency' : self.market[:3]}
        self.position = self.api.private_get_get_position(instrument_name)
        self.account = self.api.private_get_get_account_summary(currency)

    def form_01(self):
        ase = {
            "market" : self.market,
            "avg_price" : self.__avg_price(),
            "size" : self.__size(),
            "equity" : self.__equity()
        }
        super().form_01(ase)

    def __avg_price(self):
        avg_price = self.position['result']['average_price']
        return avg_price

    def __size(self):
        size = self.position['result']['size']
        return size

    def __equity(self):
        return self.account['result']['equity']


class Upbit(Forms):
    def __init__(self, *args, **kwargs):
        self.api = ccxt.upbit()
        super().__init__(*args, **kwargs)
        self.__filter()

    def form_01(self):
        ase = {
            "market" : self.market,
            "avg_price" : self.__avg_price(),
            "size" : self.__size(),
            "equity" : self.__equity()
        }
        super().form_01(ase)

    def __avg_price(self):
        return self.avg_price

    def __size(self):
        return self.size

    def __equity(self):
        return self.equity_total

    def __filter(self):
        account = self.api.private_get_accounts()

        equity_total = 0
        avg_price = 0
        size = 0

        for equity in account:
            if equity['currency'] == 'KRW':
                equity_total = equity_total + float(equity['locked'])
                equity_total = equity_total + float(equity['balance'])
            else:
                avg_buy = float(equity["avg_buy_price"])
                balance = float(equity['balance'])
                equity_total = equity_total + (avg_buy * balance)

            if equity['currency'] == self.market[-3:]:
                avg_price = equity["avg_buy_price"]
                size = equity["balance"]

        self.equity_total = equity_total
        self.avg_price = avg_price
        self.size = size

class Coinbase(Forms):
    def __init__(self, *args, **kwargs):
        self.api = ccxt.coinbase()
        super().__init__(*args, **kwargs)
        self.account = self.api.private_get_accounts()



if __name__ == "__main__":

    coinbase_key = "rQXJ3iFInU1z7K2R"
    coinbase_secret = "VLMNaNvQlPAPZEJR0QdFNDZaxFqdzotF"

    # KD_001_BTC_KEY = "E1qbcbs1"
    #
    # KD_001_BTC_SECRET = "CWp6jruam9s8mJvgjMFqhZZNGAub76QA-TxYdHFkgg0"
    #
    # access          = KD_001_BTC_KEY
    #
    # secret          = KD_001_BTC_SECRET
    #
    # market          = 'BTC-PERPETUAL'
    #
    # ratio_to_invest = 0.20
    #
    # strategy        = 'a'
    #
    # df              = 'b'
    #
    # trading = Deribit(access, secret, market,
    #                 ratio_to_invest, strategy, df)
    #
    # trading.form_01()

    TAEHUN_UPBIT_ACCESS_KEY = "lpeP99y29PyxHNoxBpicfe5VP6dVlpORPyAP7xeV"

    TAEHUN_UPBIT_SECRET_KEY = "ST4sIxEjaXx9Nhz3eUUEInIZWCY103WxkfipiyqR"

    access          = TAEHUN_UPBIT_ACCESS_KEY

    secret          = TAEHUN_UPBIT_SECRET_KEY

    market          = "KRW-BCH"

    ratio_to_invest = 0.20

    strategy        = 'a'

    df              = 'b'

    trading = Upbit(access, secret, market,
                    ratio_to_invest, strategy, df)

    trading.form_01()
