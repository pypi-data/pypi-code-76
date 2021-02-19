#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/2/1 9:32
@File    : export_strategy_setting.py
@contact : mmmaaaggg@163.com
@desc    : 用于导出 策略设置 生成 json 文件，该文件用于覆盖
.vntrader\cta_strategy_setting.json
.vntrader\portfolio_strategy_setting.json
文件
"""
import json
from collections import OrderedDict
from typing import List

from vnpy_extra.db.orm import StrategyBacktestStats, StrategyBacktestStatusEnum


def generate_strategy_setting_file():
    stats_list: List[StrategyBacktestStats] = StrategyBacktestStats.get_by_status(
        StrategyBacktestStatusEnum.CompareTradeData.value)
    stats_dic = OrderedDict()
    for stats in stats_list:
        stats_dic[stats.short_name] = dic = OrderedDict()
        dic["class_name"] = stats.stg_info.strategy_class_name
        dic["vt_symbol"] = stats.symbols_info.symbols
        dic["setting"] = stats.strategy_settings
        dic["setting"]['class_name'] = stats.stg_info.strategy_class_name

    file_path = "cta_strategy_setting.json"
    with open(file_path, 'w') as f:
        json.dump(stats_dic, f, indent=4)

    return file_path


if __name__ == "__main__":
    pass
