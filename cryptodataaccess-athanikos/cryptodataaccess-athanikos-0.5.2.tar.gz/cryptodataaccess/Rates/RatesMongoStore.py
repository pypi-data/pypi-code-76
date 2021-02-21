from datetime import datetime
from cryptomodel.coinmarket import prices
from cryptomodel.fixer import exchange_rates, Q
from cryptomodel.readonly import SymbolRates
from cryptodataaccess.Rates.RatesStore import RatesStore
from cryptodataaccess.helpers import server_time_out_wrapper, do_connect, convert_to_int_timestamp
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class RatesMongoStore(RatesStore):

    def __init__(self, config, log_error):
        self.configuration = config
        self.log_error = log_error

    def fetch_symbols(self):
        symbols = {}
        latest_prices = self.fetch_latest_prices_to_date( convert_to_int_timestamp(datetime.today()))
        for coin in latest_prices[0].coins:
            symbols.update({coin.symbol: coin.name})
        return symbols

    def fetch_symbol_rates(self):
        dt_now = convert_to_int_timestamp(datetime.today())
        return self.fetch_symbol_rates_for_date(dt_now)

    def fetch_symbol_rates_for_date(self, dt):
        srs = SymbolRates(dt)
        latest_prices = self.fetch_latest_prices_to_date(dt)
        for coin in latest_prices[0].coins:
            srs.add_rate(coin.symbol, coin.quote.eur)
        return srs

    def fetch_latest_prices_to_date(self, before_date):
        return server_time_out_wrapper(self, self.do_fetch_latest_prices_to_date, before_date)

    def fetch_latest_exchange_rates_to_date(self, before_date):
        return server_time_out_wrapper(self, self.do_fetch_latest_exchange_rates_to_date, before_date)

    def do_fetch_latest_prices_to_date(self, before_date):
        do_connect(self.configuration)
        return prices.objects(Q(status__timestamp__lte=before_date)).order_by(
            '-status__timestamp')[:10]

    def do_fetch_latest_exchange_rates_to_date(self, before_date):
        do_connect(self.configuration)
        return exchange_rates.objects(Q(date__lte=before_date)).order_by(
            'date-')[:1]
