# -*- coding: utf-8 -*-

# OHLCV
COL_CANDLE_BEGIN_TIME = 'candle_begin_time'
COL_OPEN = 'open'
COL_HIGH = 'high'
COL_LOW = 'low'
COL_CLOSE = 'close'
COL_VOLUME = 'volume'

# 策略通用列，仓位、信号
COL_POS = 'pos'
COL_SIGNAL = 'signal'

# 资金曲线相关
COL_CHANGE = 'change'  # 收盘价格涨跌幅
COL_BUY_AT_OPEN_CHANGE = 'buy_at_open_change'  # 收盘/开盘 - 1
COL_SELL_NEXT_OPEN_CHANGE = 'sell_next_open_change'  # 开盘[-1]/收盘 - 1
COL_POSITION_START_TIME = 'start_time'  # 仓位开始时间
COL_POSITION_START = 'position'  # 建仓仓位
COL_POSITION_MAX_VALUE = 'position_max'  # 仓位最大价值
COL_POSITION_MIN_VALUE = 'position_min'  # 的仓位最小价值
COL_CASH = 'cash'  # 现金量
COL_CASH_MIN = 'cash_min'  # 实际最小现金量
COL_PROFIT = 'profit'  # 持仓盈利
COL_PROFIT_MIN = 'profit_min'  # 实际最小持仓盈利
COL_FORCE_CLOSE_OUT = 'force_close_out'  # 是否有爆仓
COL_FORCE_CLOSE_OUT_CASH = 'force_close_out_cash'  # 爆仓后的现金
COL_EQUITY_CHANGE = 'equity_change'  # 现金涨跌幅
COL_EQUITY_CURVE = 'equity_curve'  # 现金曲线

# 回测相关
COL_LEVERAGE = 'leverage'  # 杠杆
COL_START_DATE = 'bt_start_date'  # 回测起始时间
COL_END_DATE = 'bt_end_date'  # 回测结束时间
COL_PARAMS = 'params'  # 回测参数组合
COL_RULE_TYPE = 'rule_type'  # K 线时长规则
COL_SLICE = 'data_set_slice'  # 回测日期分割数
COL_BT_EQUITY_CURVE = 'equity_curve'  # 回测资金曲线

# 定投
COL_COST = 'cost'
COL_LAST_WORTH = 'last_worth'
COL_CASH_PL = 'cash_pl'

# 交易回测
COL_LOSE_COUNT = 'loss_deals'
COL_PROFIT_COUNT = 'profit_deals'
COL_LOSE_COUNT_PERCENT = 'loss_deals_pct'
COL_PROFIT_COUNT_PERCENT = 'profit_deals_pct'
COL_LOSE_POS_LENGTH_AVG = 'avg_loss_pos_duration'
COL_PROFIT_POS_LENGTH_AVG = 'avg_profit_pos_duration'
COL_LOSE_RATE_AVG = 'avg_loss_pct'
COL_PROFIT_RATE_AVG = 'avg_profit_pct'
COL_PROFIT_LOSE_RATIO = 'profit_loss_ratio'
COL_ANNUALIZED_RETURN_RATE = 'annualized_income_pct'
COL_MDD = 'mdd'
COL_MDD_BEGIN_DATE = 'mdd_begin'
COL_MDD_END_DATE = 'mdd_end'
