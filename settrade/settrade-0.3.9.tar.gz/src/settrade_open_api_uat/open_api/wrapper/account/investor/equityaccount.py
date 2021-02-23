from ...lib import settrade_open_api as soa
from ...util import send_python_error

class InvestorEquity:
    def __init__(self, context, logger, account_no):
        self._logger = logger
        self._context = context
        self._account_no = account_no

    def get_account_info(self):
        start = self._logger.get_current_time()
        try:
            result = soa.get_investor_equity_account_info(
                self._context, self._account_no
            )
            self._logger.write(start, "PYTHON_INFO", "get_account_info", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "get_account_info", err)
            return send_python_error(err)

    def get_orders(self):
        start = self._logger.get_current_time()
        try:
            result = soa.get_investor_equity_orders(self._context, self._account_no)
            self._logger.write(start, "PYTHON_INFO", "get_orders", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "get_orders", err)
            return send_python_error(err)

    def get_order(self, order_no):
        start = self._logger.get_current_time()
        try:
            result = soa.get_investor_equity_order(
                self._context, self._account_no, order_no
            )
            self._logger.write(start, "PYTHON_INFO", "get_order", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "get_order", err)
            return send_python_error(err)

    def get_portfolio(self):
        start = self._logger.get_current_time()
        try:
            result = soa.get_investor_equity_portfolios(self._context, self._account_no)
            self._logger.write(start, "PYTHON_INFO", "get_portfolio", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "get_portfolio", err)
            return send_python_error(err)

    def get_trades(self):
        start = self._logger.get_current_time()
        try:
            result = soa.get_investor_equity_trades(self._context, self._account_no)
            self._logger.write(start, "PYTHON_INFO", "get_trades", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "get_trades", err)
            return send_python_error(err)

    def place_order(
        self,
        symbol,
        price,
        volume,
        side,
        pin,
        price_type="LIMIT",
        validity_type="DAY",
        trustee_id_type="LOCAL",
        qty_open=0,
        bypass_warning=False,
    ):
        start = self._logger.get_current_time()

        client_type = ""
        price_not_null_when_price_type_is_limit = False
        
        try:
            result = soa.place_investor_equity_order(
                self._context,
                self._account_no,
                symbol,
                price,
                volume,
                side,
                pin,
                price_type,
                validity_type,
                client_type,
                trustee_id_type,
                price_not_null_when_price_type_is_limit,
                qty_open,
                bypass_warning,
            )
            self._logger.write(start, "PYTHON_INFO", "place_order", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "place_order", err)
            return send_python_error(err)

    def cancel_order(self, order_no, pin):
        start = self._logger.get_current_time()
        try:
            result = soa.cancel_investor_equity_order(
                self._context, self._account_no, order_no, pin
            )
            self._logger.write(start, "PYTHON_INFO", "cancel_order", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "cancel_order", err)
            return send_python_error(err)

    def change_order(
        self, order_no, pin, new_price=0, new_volume=0, new_price_type = "LIMIT"
    ):
        new_iceberg_volume = 0
        new_trustee_id_type = ""
        bypass_warning = False
        start = self._logger.get_current_time()
        try:
            result = soa.change_investor_equity_order(
                self._context,
                self._account_no,
                order_no,
                new_price,
                new_volume,
                pin,
                new_price_type,
                new_iceberg_volume,
                new_trustee_id_type,
                bypass_warning,
            )
            self._logger.write(start, "PYTHON_INFO", "change_order", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "change_order", err)
            return send_python_error(err)

    def cancel_orders(self, orders_no, pin):
        start = self._logger.get_current_time()
        try:
            result = soa.cancel_investor_equity_orders(
                self._context, self._account_no, orders_no, pin
            )
            self._logger.write(start, "PYTHON_INFO", "cancel_orders", "success")
            return result
        except Exception as err:
            self._logger.write(start, "PYTHON_EXCEPTION", "cancel_orders", err)
            return send_python_error(err)
