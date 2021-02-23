# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------
    File Name:              var
    Description:            
    Author:                 hzy
    date:                   2019/8/23
------------------------------------------------------------------
    Change Activity:
                            2019/8/23
------------------------------------------------------------------
"""
__author__ = 'hzy'

import time
import re


class Permission:
    VIEW_DATA = 2 ** 0
    VIEW_DATA_PAD = 2 ** 1

    WRITE_ARTICLE = 2 ** 2

    PUBLISH_DRAFT_ARTICLE = 2 ** 3
    PUBLISH_WITHDRAWN_ARTICLE = 2 ** 4

    EDIT_PUBLISHED_ARTICLE = 2 ** 5
    EDIT_DRAFT_ARTICLE = 2 ** 6
    EDIT_WITHDRAWN_ARTICLE = 2 ** 7
    EDIT_TO_BE_PUBLISHED_ARTICLE = 2 ** 8

    WITHDRAWN_PUBLISHED_ARTICLE = 2 ** 9
    WITHDRAWN_TO_BE_PUBLISHED_ARTICLE = 2 ** 10

    DELETE_PUBLISHED_ARTICLE = 2 ** 11
    DELETE_TO_BE_PUBLISHED_ARTICLE = 2 ** 12
    DELETE_DRAFT_ARTICLE = 2 ** 13
    DELETE_WITHDRAWN_ARTICLE = 2 ** 14

    RECOMMEND_ARTICLE = 2 ** 15

    ADD_USER = 2 ** 16
    DELETE_USER = 2 ** 17
    EDIT_USER = 2 ** 18
    # RESET_USER_PASSWORD = 2 ** 19

    ADD_ROLE = 2 ** 19
    UPDATE_ROLE_PERMISSION = 2 ** 20
    DELETE_ROLE = 2 ** 21

    # USER_STATISTIC = 2 ** 23  # 后台首页用户数据统计
    # ARTICLE_STATISTIC = 2 ** 24  # 后台首页文章统计
    # ARTICLE_WRITE_RANK = 2 ** 25  # 后台首页文章编写排行榜
    # ARTICLE_PUBLISH_RANK = 2 ** 26  # 后台首页文章发表排行榜
    # USER_PUBLISH_ARTICLE = 2 ** 27  # 后台首页用户发表文章
    # USER_WITHDRAWN_ARTICLE = 2 ** 28  # 后台首页用户撤回文章
    # USER_WRITE_ARTICLE = 2 ** 29  # 后台首页用户撰写文章

class ErrorCode:
    SYSTEM_BUG_ERROR = -500
    PARAM_INCORRECT_ERROR = -405
    PARAM_LOST_ERROR = -404
    TOKEN_LOST_ERROR = -403
    NOT_FOUND_ERROR = -407
    DUPLICATE_ERROR = -409
    AUTH_ERROR = -406
    RANGE_ERROR = -400
    VALIDATION_ERROR = -420
    COUNTI_FEIGN_ERROR = -501
    BANK_FEIGN_ERROR = -502
    EXCEED_LIMIT_ERROR = -411
    PERMISSION_FORBIDDEN_ERROR = -410
    DB_ERROR = -408
    ACCOUNT_ERROR = -412
    COUNTI_VALIDATION_ERROR = -499


# 描述
INNER_ERROR_STRING = 'inner_error 💀'

# blueprint prefix_path
API_PREFIX_PATH = '/api'
POINT_PREFIX_PATH = '/point'

# param
TOKEN_PARAM_NAME = 'token'
USER_ID = 'user_id'
CHARACTER_PARAM_NAME = 'character'
VISITOR_ID = 'visitor_id'

# date format
DEFAULT_YEAR_INTERVAL = 365
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# cache prefix
ANALYSIS_RESULT = "analysis_result"
ANALYSIS_SRC = "analysis_src"
RISK_KEY = 'risk'
EF_LINES = 'ef_lines'
BENCHMARK_INFO = 'benchmark_info'
ASSET_INFO = 'asset_info'
PRODUCT_INFO = 'product_info'
PRE_ASSET_SECURITY = 'pre_asset_security'
PRE_AVAILABLE_ASSET_SECURITY = 'pre_available_asset_security'
RISK_PREDICT = 'risk_predict'
ASSET_PRICE_LATEST = 'asset_price_latest'
MC_PREDICT_RETURNS = 'mc_predict_returns'
CODE_SCORE = 'code_score'
CODE_INFO = 'code_info'
CODE_PERFORMANCE = 'code_performance'
CODE_RISK = 'code_risk'
CODE_TREND = 'code_trend'
CODE_QUOTE = 'code_quote'
CODE_PENETRATE = 'code_penetrate'
CODE_INDICATOR = 'code_indicator'
PORTFOLIO_TEMPLATES = 'portfolio_templates'
PORTFOLIOS_INDICATOR = 'portfolios_indicator'
CODE_TAG = 'code_tag'
CODE_COMPONENT = 'code_component'
CODE_TRANSFORM = 'code_transform'
FUND_INFO = 'fund_info'
# 前端字段映射
# 埋点映射
BURYING_POINT_DICT = {
    "service_id": 'sid',
    "page_id": 'pid',
    "stay_time": 'stm',
    "enter_time": 'etm',
    "addition": 'ad',
    "operation": 'o',
    "operation_action": 'oat',
    "operation_target": 'ota',
    "operation_time": 'otm',
    "operation_addition": 'oad'
}


if __name__ == "__main__":
    start_t = time.time()

    print("use time: %s" % (time.time() - start_t))
