from .user import User
from ..account.investor.derivativesaccount import InvestorDerivatives
from ..account.investor.equityaccount import InvestorEquity
from ..logger import Logger

class Investor(User):
    def __init__(self, app_id, app_secret, app_code, broker_id, is_auto_queue=False):
        self._logger = Logger("settrade_log")
        self._logger.create_log_dir()
        
        start = self._logger.get_current_time()
        
        try:
            super().__init__(app_id, app_secret, app_code, broker_id, is_auto_queue)
            self._logger.remove_expired_log()
            self._logger.write(start, "PYTHON_INFO", "Login_Investor", self._context)
        except Exception as e:
            self._logger.write(start, "PYTHON_EXCEPTION", "Login_Investor", e)
            raise Exception(e)

    def Derivatives(self, account_no):
        return InvestorDerivatives(self._context, self._logger, account_no)

    def Equity(self, account_no):
        return InvestorEquity(self._context, self._logger, account_no)
