from .user import User
from ..account.marketrep.derivativesaccount import MarketRepDerivatives
from ..account.marketrep.equityaccount import MarketRepEquity
from ..logger import Logger

class MarketRep(User):
    def __init__(self, app_id, app_secret, app_code, broker_id, is_auto_queue=False):
        self._logger = Logger("settrade_log")
        self._logger.create_log_dir()
        
        start = self._logger.get_current_time()
        
        try:
            super().__init__(app_id, app_secret, app_code, broker_id, is_auto_queue)
            self._logger.remove_expired_log()
            self._logger.write(start, "PYTHON_INFO", "Login_MarketRep", self._context)
        except Exception as e:
            self._logger.write(start, "PYTHON_EXCEPTION", "Login_MarketRep", e)
            raise Exception(e)

    def Derivatives(self):
        return MarketRepDerivatives(self._context, self._logger)

    def Equity(self):
        return MarketRepEquity(self._context, self._logger)
