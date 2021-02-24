import hmac
import pkg_resources
import re
from configparser import ConfigParser
from hashlib import md5, sha256
from time import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

from requests import request


api = ConfigParser()
api.read_string(pkg_resources.resource_string(__name__, 'config/api.cfg').decode())


class TradingAPI:
    def __init__(self, api_key: str, api_secret: str) -> None:
        self._api_key = api_key
        self._api_secret = api_secret

    @staticmethod
    def _get_url(path: str, path_params: Dict[str, str], get_params: Dict[str, Any]) -> str:
        def replace_path_params(match):
            key = match.group()[2:]
            return '' if path_params.get(key, None) is None else '/' + path_params[key]
        get_params = {k + '[]' if isinstance(v, list) else k: v for k, v in get_params.items()}
        return (api['DEFAULT']['url']
                + re.sub('(/):[^/]+', replace_path_params, path)
                + ('?' + urlencode(sorted(get_params.items()), True) if len(get_params) else ''))

    def _get_headers(self, method: str, url: str,
                     post_params: Dict[str, Any] = {}) -> Dict[str, str]:
        nonce = str(int(time()))
        hashed_post_params = md5(urlencode(sorted(post_params.items())).encode()).hexdigest()
        msg = '#'.join([method, url, self._api_key, nonce, hashed_post_params]).encode()
        return {
            'X-API-KEY': self._api_key,
            'X-API-NONCE': nonce,
            'X-API-SIGNATURE': hmac.new(self._api_secret.encode(), msg, sha256).hexdigest()
        }

    def _make_request(self, method: str, path: str, path_params: Dict[str, str] = {},
                      get_params: Dict[str, Any] = {},
                      post_params: Dict[str, Any] = {}) -> Dict[str, Any]:
        url = self._get_url(path, path_params, get_params)
        headers = self._get_headers(method, url, post_params)
        return request(method, url, headers=headers).json()

    def show_orderbook(self, trading_pair: str, type: str, **get_params: Any) -> Dict[str, Any]:
        return self._make_request(method=api['showOrderbook']['method'],
                                  path=api['showOrderbook']['path'],
                                  path_params={'trading_pair': trading_pair},
                                  get_params={'type': type, **get_params})

    def show_order_details(self, trading_pair: str, order_id: str) -> Dict[str, Any]:
        return self._make_request(method=api['showOrderDetails']['method'],
                                  path=api['showOrderDetails']['path'],
                                  path_params={'trading_pair': trading_pair, 'order_id': order_id})

    def show_my_orders(self, trading_pair: Optional[str] = None,
                       **get_params: Any) -> Dict[str, Any]:
        return self._make_request(method=api['showMyOrders']['method'],
                                  path=api['showMyOrders']['path'],
                                  path_params={'trading_pair': trading_pair},
                                  get_params=get_params)

    def show_my_order_details(self, trading_pair: str, order_id: str) -> Dict[str, Any]:
        return self._make_request(method=api['showMyOrderDetails']['method'],
                                  path=api['showMyOrderDetails']['path'],
                                  path_params={'trading_pair': trading_pair, 'order_id': order_id})

    def show_orderbook_compact(self, trading_pair: str) -> Dict[str, Any]:
        return self._make_request(method=api['showOrderbookCompact']['method'],
                                  path=api['showOrderbookCompact']['path'],
                                  path_params={'trading_pair': trading_pair})

    def show_my_trade_details(self, trading_pair: str, trade_id: str) -> Dict[str, Any]:
        return self._make_request(method=api['showMyTradeDetails']['method'],
                                  path=api['showMyTradeDetails']['path'],
                                  path_params={'trading_pair': trading_pair, 'trade_id': trade_id})

    def show_my_trades(self, trading_pair: Optional[str] = None,
                       **get_params: Any) -> Dict[str, Any]:
        return self._make_request(method=api['showMyTrades']['method'],
                                  path=api['showMyTrades']['path'],
                                  path_params={'trading_pair': trading_pair},
                                  get_params=get_params)

    def show_public_trade_history(self, trading_pair: str, **get_params: Any) -> Dict[str, Any]:
        return self._make_request(method=api['showPublicTradeHistory']['method'],
                                  path=api['showPublicTradeHistory']['path'],
                                  path_params={'trading_pair': trading_pair},
                                  get_params=get_params)

    def show_account_info(self) -> Dict[str, Any]:
        return self._make_request(method=api['showAccountInfo']['method'],
                                  path=api['showAccountInfo']['path'])

    def show_rates(self, trading_pair: str) -> Dict[str, Any]:
        return self._make_request(method=api['showRates']['method'],
                                  path=api['showRates']['path'],
                                  path_params={'trading_pair': trading_pair})

    def show_account_ledger(self, currency: str, **get_params: Any) -> Dict[str, Any]:
        return self._make_request(method=api['showAccountLedger']['method'],
                                  path=api['showAccountLedger']['path'],
                                  path_params={'currency': currency},
                                  get_params=get_params)

    def show_permissions(self) -> Dict[str, Any]:
        return self._make_request(method=api['showPermissions']['method'],
                                  path=api['showPermissions']['path'])

    def show_deposit(self, currency: str, deposit_id: str) -> Dict[str, Any]:
        return self._make_request(method=api['showDeposit']['method'],
                                  path=api['showDeposit']['path'],
                                  path_params={'currency': currency, 'deposit_id': deposit_id})

    def show_deposits(self, currency: str, **get_params: Any) -> Dict[str, Any]:
        return self._make_request(method=api['showDeposits']['method'],
                                  path=api['showDeposits']['path'],
                                  path_params={'currency': currency},
                                  get_params=get_params)

    def show_withdrawal(self, currency: str, withdrawal_id: str) -> Dict[str, Any]:
        return self._make_request(method=api['showWithdrawal']['method'],
                                  path=api['showWithdrawal']['path'],
                                  path_params={'currency': currency,
                                               'withdrawal_id': withdrawal_id})

    def show_withdrawal_min_network_fee(self, currency: str) -> Dict[str, Any]:
        return self._make_request(method=api['showWithdrawalMinNetworkFee']['method'],
                                  path=api['showWithdrawalMinNetworkFee']['path'],
                                  path_params={'currency': currency})

    def show_withdrawals(self, currency: str, **get_params: Any) -> Dict[str, Any]:
        return self._make_request(method=api['showWithdrawals']['method'],
                                  path=api['showWithdrawals']['path'],
                                  path_params={'currency': currency},
                                  get_params=get_params)
