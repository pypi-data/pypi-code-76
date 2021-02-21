from qttp.tools.log import setup_custom_logger

logger = setup_custom_logger("Forms")

class Forms:
    def __init__(self, access, secret, market,
                 ratio_to_invest, strategy, df):
        self.trading         = self.exchange(access, secret, market, log=False)
        self.market          = market
        self.ratio_to_invest = ratio_to_invest
        self.strategy        = strategy
        self.df              = df

        self.equity    = self.trading.equity()
        self.signal    = self.__signal()

    def a_01(self):
        # buy at ask market, sell at bid market with form_01
        buy_price = self.trading.ask_price(10)
        sell_price = self.trading.bid_price(10)
        self.__form_01(buy_price, sell_price)

    def a_02(self):
        # buy at ask market, sell at bid market with form_02
        buy_price = self.trading.ask_price(10)
        sell_price = self.trading.bid_price(10)
        self.__form_02(buy_price, sell_price)

    def a_03(self):
        # buy at ask market, sell at bid market, set sub_limit with form_02
        buy_price = self.trading.ask_price(10)
        sell_price = self.trading.bid_price(10)
        self.__form_02(buy_price, sell_price, sub_limit=0.92)

    def a_04(self):
        # buy at bid limit, sell at ask limit with form_02
        buy_price = self.trading.bid_price(0)
        sell_price = self.trading.ask_price(0)
        self.__form_02(buy_price, sell_price)

    def a_05(self):
        # buy at bid limit, sell at bid market with form_02
        buy_price = self.trading.bid_price(0)
        sell_price = self.trading.bid_price(10)
        self.__form_02(buy_price, sell_price)

    def a_06(self):
        # buy at open price, sell at ask limit with form_02
        buy_price = self.__open_price()
        sell_price = self.trading.ask_price(0)
        self.__form_02(buy_price, sell_price)

    def __form_01(self, buy_price, sell_price):
        self.trading.cancel_all()
        size = self.trading.size()
        signal = self.signal

        self.__signal_msg()

        if size > 0:
            # Sell
            self.trading.limit_sell(size, sell_price)
            self.__sell_msg(sell_price, size)

        if signal == 1:
            # Buy
            invest_amount = self.invest_amount(buy_price)
            self.trading.limit_buy(invest_amount, buy_price)
            self.__buy_msg(buy_price, invest_amount)

    def __form_02(self, buy_price, sell_price, sub_limit=None):
        size = self.trading.size()
        signal = self.signal

        self.__signal_msg()

        if signal == 1:
            if size > 0:
                self.__keep_msg()
            else:
                # buy
                invest_amount = self.invest_amount(buy_price)
                self.trading.limit_buy(invest_amount, buy_price)

                if sub_limit:
                    buy_price_02 = round(buy_price * sub_limit, -1)
                    self.trading.limit_buy(invest_amount, buy_price_02)

                self.__buy_msg(buy_price, invest_amount)

        else:
            if size > 0:
                # Sell
                self.trading.limit_sell(size, sell_price)
                self.__sell_msg(sell_price, size)

        print("-" * 110)

    def __basic_msg(self):
        basic_msg = (
            f"{self.trading.exchange_name()} - {self.market} - "
        )
        return basic_msg

    def __signal_msg(self):
        basic_msg  = self.__basic_msg()
        signal_msg = (
            f"{self.strategy.__name__:<13s} -  "
            f"{self.signal}"
        )
        signal_msg = basic_msg + signal_msg
        logger.info(signal_msg)

    def __buy_msg(self, buy_price, buy_quantity):
        basic_msg = self.__basic_msg()
        buy_process = "Buy Process"
        buy_msg   = f"{buy_process: <13s} -  "
        buy_msg = buy_msg + f"price: {buy_price}, amount: {buy_quantity}"
        buy_msg   = basic_msg + buy_msg
        logger.info(buy_msg)

    def __sell_msg(self, sell_price, sell_quantity):
        basic_msg = self.__basic_msg()
        sell_process = "Sell Process"
        sell_msg   = f"{sell_process: <13s} -  "
        sell_msg   = sell_msg + f"price: {sell_price}, amount: {sell_quantity}"
        sell_msg   = basic_msg + sell_msg
        logger.info(sell_msg)

    def __keep_msg(self):
        basic_msg  = self.__basic_msg()
        keep_msg = basic_msg + f"{self.strategy.__name__:<13s} -  Keep Trading"
        logger.info(keep_msg)

    def __signal(self):
        signal = self.strategy(self.df).iloc[-1, -2]
        return signal

    def __open_price(self):
        return self.df.iloc[-1, 0]


class DeribitForm(Forms):
    def __init__(self, *args, **kwargs):
        from qttp.trading_apis import DeribitApi
        self.exchange = DeribitApi
        self.invest_amount = self.__invest_amount
        super().__init__(*args, **kwargs)

    def __invest_amount(self, price):
        invest_amount = round(self.equity * self.ratio_to_invest, 4)
        invest_amount = round(invest_amount * price, -1)
        return invest_amount

class BybitForm(Forms):
    def __init__(self, *args, **kwargs):
        from qttp.trading_apis import BybitApi
        self.exchange = BybitApi
        self.invest_amount = self.__invest_amount
        super().__init__(*args, **kwargs)

    def __invest_amount(self, price):
        invest_amount = round(self.equity * self.ratio_to_invest, 4)
        invest_amount = round(invest_amount * price, -1)
        return invest_amount

class UpbitForm(Forms):
    def __init__(self, *args, **kwargs):
        from qttp.trading_apis import UpbitApi
        self.exchange = UpbitApi
        self.invest_amount = self.__invest_amount
        super().__init__(*args, **kwargs)

    def __invest_amount(self, price):
        invest_amount = self.equity * self.ratio_to_invest
        invest_amount = round(invest_amount / price, 5)
        return invest_amount
