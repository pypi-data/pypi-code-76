from ...lib import settrade_open_api as soa
from ...util import send_python_error

class MarketRepDerivatives:
    def __init__(self, context, logger):
        self._context = context
        self._logger = logger

    def get_account_info(self, account_no):
        start = self._logger.get_current_time()
        try:
            result = soa.get_marketrep_derivatives_account_info(self._context, account_no)
            self._logger.write(start, "PYTHON_INFO", "get_account_info", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "get_account_info", err)
            return send_python_error(err)

    def get_orders(self):
        start = self._logger.get_current_time()
        try:
            result = soa.get_marketrep_derivatives_orders(self._context)
            self._logger.write(start, "PYTHON_INFO", "get_orders", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "get_orders", err)
            return send_python_error(err)

    def get_order(self, order_no):
        start = self._logger.get_current_time()
        try:
            result = soa.get_marketrep_derivatives_order(self._context, order_no)
            self._logger.write(start, "PYTHON_INFO", "get_order", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "get_order", err)
            return send_python_error(err)

    def get_orders_by_account_no(self, account_no):
        start = self._logger.get_current_time()
        try:
            result = soa.get_marketrep_derivatives_orders_by_account_no(
                self._context, account_no
            )
            self._logger.write(
                start, "PYTHON_INFO", "get_orders_by_account_no", "success"
            )
            return result
        except Exception as err:
            self._logger.write(
                start, "PYTHON_EXCEPTION", "get_orders_by_account_no", err
            )
            return send_python_error(err)

    def get_portfolio(self, account_no):
        start = self._logger.get_current_time()
        try:
            result = soa.get_marketrep_derivatives_portfolios(self._context, account_no)
            self._logger.write(start, "PYTHON_INFO", "get_portfolio", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "get_portfolio", err)
            return send_python_error(err)

    def get_trades(self, account_no):
        start = self._logger.get_current_time()
        try:
            result = soa.get_marketrep_derivatives_trades(self._context, account_no)
            self._logger.write(start, "PYTHON_INFO", "get_trades", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "get_trades", err)
            return send_python_error(err)

    def place_order(
        self,
        account_no,
        symbol,
        price,
        volume,
        side,
        position,
        price_type="LIMIT",
        validity_type="GOOD_TILL_DAY",
        stop_condition="",
        stop_symbol="",
        stop_price=0,
        bypass_warning=False,
    ):
        start = self._logger.get_current_time()
        try:
            result = soa.place_marketrep_derivatives_order(
                self._context,
                account_no,
                symbol,
                price,
                volume,
                side,
                position,
                price_type,
                validity_type,
                stop_condition,
                stop_symbol,
                stop_price,
                bypass_warning,
            )
            self._logger.write(start, "PYTHON_INFO", "place_order", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "place_order", err)
            return send_python_error(err)

    def cancel_order(self, account_no, order_no):
        start = self._logger.get_current_time()
        try:
            result = soa.cancel_marketrep_derivatives_order(
                self._context, account_no, order_no
            )
            self._logger.write(start, "PYTHON_INFO", "cancel_order", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "cancel_order", err)
            return send_python_error(err)

    def change_order(
        self, account_no, order_no, new_account_no="", new_price=0, new_volume=0,
    ):
        new_position = ""
        new_price_type = ""
        start = self._logger.get_current_time()
        try:
            result = soa.change_marketrep_derivatives_order(
                self._context,
                account_no,
                order_no,
                new_account_no,
                new_price,
                new_volume,
                new_position,
                new_price_type,
            )
            self._logger.write(start, "PYTHON_INFO", "change_order", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "change_order", err)
            return send_python_error(err)

    def cancel_orders(self, account_no, orders_no):
        start = self._logger.get_current_time()
        try:
            result = soa.cancel_marketrep_derivatives_orders(
                self._context, account_no, orders_no
            )
            self._logger.write(start, "PYTHON_INFO", "cancel_orders", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "cancel_orders", err)
            return send_python_error(err)

    def place_trade_report(
        self, symbol, cpm, price, volume, position, tr_type, buyer="", seller=""
    ):
        start = self._logger.get_current_time()
        try:
            result = soa.place_marketrep_derivatives_trade_report(
                self._context,
                symbol,
                cpm,
                price,
                volume,
                position,
                tr_type,
                buyer,
                seller,
            )
            self._logger.write(
                start,
                "PYTHON_INFO",
                "place_trade_report",
                "success",
            )
            return result
        except Exception as err:
            self._logger.write(
                start,
                "PYTHON_EXCEPTION",
                "place_trade_report",
                err,
            )
            return send_python_error(err)
