from ..lib import settrade_open_api as soa
from ..mqtt import MQTTWebsocket
from ..market_data import MarketData

class User:
    def __init__(self, app_id, app_secret, app_code, broker_id, is_auto_queue=False):
        self._context = soa.login(app_id, app_secret, app_code, broker_id, is_auto_queue)

    def RealtimeDataConnection(self):
        return MQTTWebsocket(self._context)

    def MQTTWebsocket(self):
        return MQTTWebsocket(self._context)
    
    def MarketData(self):
        return MarketData(self._context, self._logger)
