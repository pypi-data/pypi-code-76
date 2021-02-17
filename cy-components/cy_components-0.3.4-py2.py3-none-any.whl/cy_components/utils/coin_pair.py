# -*- coding: utf-8 -*-


class CoinPair:
    """ 币对处理类 """

    @classmethod
    def coin_pair_with(cls, cp_str, sep='/'):
        comps = cp_str.split(sep)
        if len(comps) < 2:
            return None
        return CoinPair(comps[0], comps[1])

    def __init__(self, trade_coin='', base_coin='', custom_min_cost=None):
        self.trade_coin = trade_coin.upper()
        self.base_coin = base_coin.upper()
        self.custom_min_cost = custom_min_cost  # 自定义最小下单金额

    def formatted(self, sep='/'):
        """获取格式化的币对

        Parameters
        ----------
        sep : str, optional
            分割符, by default '/'
        """
        return "{}{}{}".format(self.trade_coin, sep, self.base_coin)

    @property
    def estimated_value_of_base_coin(self):
        """ 以粗略的价格估算本位币价格 """
        base_coin = self.base_coin.upper()
        if base_coin in ['USDT', 'USD']:
            return 1
        if base_coin in ['ETH']:
            return 200
        if base_coin in ['BTC']:
            return 9000

        # default
        return 1


class ContractCoinPair(CoinPair):

    sep = None

    """合约币对"""
    @classmethod
    def coin_pair_with(cls, cp_str, sep='/'):
        comps = cp_str.split(sep, cp_str.count(sep))

        def safe_list_get(l, idx, default=None):
            try:
                return l[idx]
            except IndexError:
                return default
        if len(comps) < 2:
            return None

        cp = ContractCoinPair(comps[0], comps[1], safe_list_get(comps, 2))
        cp.sep = sep
        return cp

    def __init__(self, trade_coin='', base_coin='', tail_str='', custom_min_cost=None):
        super().__init__(trade_coin, base_coin, custom_min_cost)
        self.tail = tail_str.upper() if tail_str is not None else None

    def formatted(self, sep=None):
        """获取格式化的币对

        Parameters
        ----------
        sep : str, optional
            分割符, by default '/'
        """
        sep = sep if sep is not None else self.sep if self.sep is not None else '/'
        base_str = "{}{}{}".format(self.trade_coin, sep, self.base_coin)
        if self.tail is not None:
            base_str = "{}{}{}".format(base_str, sep, self.tail)
        return base_str
