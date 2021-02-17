"""
本模块定义中国股市的一些常量和规则
"""



# ------------------------------
# 定义中国股市中的各时间点
"""
TIME_0915 = "09:15:00" 			# 早盘集合竞价开始时间
TIME_0920 = "09:20:00" 			# 早盘集合竞价可撤单结束时间
TIME_0925 = "09:25:00" 			# 早盘集合竞价结束时间

TIME_0930 = "09:30:00" 			# 上午盘连续竞价开始时间
TIME_1130 = "11:30:00" 			# 上午盘连续竞价结束时间

TIME_1300 = "13:00:00" 			# 下午盘连续竞价开始时间
TIME_1457 = "14:57:00" 			# 下午盘收前盘3分钟集合竞价开始时间
TIME_1500 = "15:00:00" 			# 下午盘收盘结束时间

OPEN_TIME = TIME_0915 			# 中国股市开盘时间
CLOSE_TIME = TIME_1500 			# 中国股市收盘时间
"""

OPEN_TIME = "09:15:00" 						# 股市开盘时间

STOP_WITHDRAW_TIME = "09:20:00" 			# 早盘集合竞价停止撤单时间
OPEN_PRICE_TIME = "09:25:00" 				# 早盘集合竞价产生开盘价时间

AM_START_TIME = "09:30:00" 					# 上午盘连续竞价开始时间
AM_STOP_TIME = "11:30:00" 					# 上午盘连续竞价结束时间

PM_START_TIME = "13:00:00" 					# 下午盘连续竞价开始时间
PM_STOP_TIME = "14:57:00" 					# 下午盘连续竞价结束时间

CLOSE_TIME = "15:00:00" 					# 下午盘收盘结束时间





# --------------------
ONE_HAND = 100 					# 一手定义为 100 股

# --------------------------
# 定义涨跌停幅度
UP_LIMIT10 = 1.1 				# 涨停幅度类型1（1.1 表示在昨收价基础上乘以 1.1 表示今天涨停价）
DOWN_LIMIT10 = 0.9 				# 跌停幅度类型1（0.9 表示在昨收价基础上乘以 0.9 表示今天跌停价）

UP_LIMIT20 = 1.2 				# 涨停幅度类型1（1.2 表示在昨收价基础上乘以 1.2 表示今天涨停价）
DOWN_LIMIT20 = 0.8 				# 跌停幅度类型1（0.8 表示在昨收价基础上乘以 0.8 表示今天跌停价）


# ---------------------------
# 卖和买必须间隔天数
T0 = 0 				# 0 表示随时可买可卖
T1 = 1 				# 1 表示至少隔 1 天，即今天买进的股明天才能卖

# ----------------------------
# 国家抽税率（仅在回测时用到，实盘会自动扣）
BUY_TAX_RATE = 0 				# 股票买入时向国家交的税率为 0 （即不用交税）
SELL_TAX_RATE = 0.001 			# 股票卖出时向国家交的税率为 0.001（即千分之一）

TAX_RATE = BUY_TAX_RATE + SELL_TAX_RATE

# ----------------------------
# 过户费率（仅在回测时用到，实盘会自动扣）
BUY_TRANSFER_FEE_RATE = 0.00002 		# 买股票的时候要交的过户费率
SELL_TRANSFER_FEE_RATE = 0.00002 		# 卖股票的时候要交的过户费率





# ------------------------------------------
# ------------------------------------------
# 市场和证券（股票）代码分类正则定义
SH_LETTER_PREFIX = 'sh' 				# 字母形式的沪市前缀
SZ_LETTER_PREFIX = 'sz' 				# 字母形式的深市前缀

SH_NUMBER_PREFIX = '0' 					# 数字形式的沪市前缀
SZ_NUMBER_PREFIX = '1' 					# 数字形式的深市前缀

SH_LEAD_CODE_ARR = ['5','6','9'] 			# 沪市股票代码前导数字
SZ_LEAD_CODE_ARR = ['0','3'] 				# 深市股票代码前导数字

SH_INDEX_LEAD_CODE_ARR = ['00','95'] 			# 沪市指数代码前导数字
SZ_INDEX_LEAD_CODE_ARR = ['399'] 				# 深市指数代码前导数字
# ------------------------------
# 股票各类别名称定义，值如果含字母一定要大写，因为后面有引用为键，并且主模块 cnstock_lib 中都是将输入的类型进行 upper() 跟这里比较的
SH60 = 'SH60' 			# 表示沪市 60 开头的股票类别名称
SH688 = 'SH688' 		# 表示沪市 688 开头（科创板）的股票类别名称
SZ00 = 'SZ00' 			# 表示深市 00 开头的股票类别名称
SZ300 = 'SZ300' 		# 表示深市 300 开头（创业板）的股票类别名称

KCB = SH688
CYB = SZ300

# --------------------
"""
SHZZ_INDEX_CODE = '000001' 		# 单独定义一个上证综指代码
SH50_INDEX_CODE = '000016' 		# 上证50指数


SZCZ_INDEX_CODE = '399001' 		# 深证成指
SZZZ_INDEX_CODE = '399106' 		# 深证综指
CYB_INDEX_CODE = '399006' 		# 创业板指数
"""

# --------------------------------
# 指数 dict ，前面都加市场前缀，sh 表示上证指数， sz 表示深证指数
# 上海方面的指数dict，由于上证综指 000001 与深证市场平安银行代码 000001 冲突，故用 sh000001 代表上证综证，在向数据源拉数据时请自行转换
SH_INDEX_DICT = {
	'SHZZ':'sh000001', 			# 上证综指
	'SH50':'sh000016' 			# 上证50指数
	}

# 深圳方面的指数，399001 是深证成指
SZ_INDEX_DICT = {
	'SZCZ':'sz399001',			# 深证成指
	'ZXBZ':'sz399005', 			# 中小板指（小票集中度次于创业板）
	'CYBZ':'sz399006', 			# 创业板指
	'SZZZ':'sz399106' 			# 深证综指
	}

# 这个数组存放大盘指数代码，包括上海和深圳的
# INDEX_DICT=dict(list(SH_INDEX_DICT.items()) + list(SZ_INDEX_DICT.items())) 	# 两市指数DICT
INDEX_DICT = dict(**SH_INDEX_DICT,**SZ_INDEX_DICT)

# 指数数组
INDEX_ARR = list(set(INDEX_DICT.values()))

# ---------------
# 沪市证券代码正则分类
SH60_RE = '^60' 		# 沪市 60 开头的代码（代表A股主板股票），实际上是上面那个子集
SH688_RE = '^688' 		# 沪市 688 开头的代码（代表A股科创板股票）
#SH5_RE = '^5' 			# 沪市 5 开头的代码（代表基金）
#SH6_RE = '^6' 			# 沪市 6 开头的代码（代表A股）
#SH9_RE = '^9' 			# 沪市 9 开头的代码（代表B股股票）

# -------------
# 深市证券代码正则分类
#SZ002_RE = '^002' 		# 深市 002 开头的代码（代表中小板）
#SZ200_RE = '^200' 		# 深市 200 开头的代码（代表B股）
SZ00_RE ='^00' 			# 深市 00 开头的代码（代表A股）
SZ300_RE = '^300' 		# 深市 300 开头的代码（代表创业板）

# ---------------------
KCB_RE = SH688_RE 			# 科创板
CYB_RE = SZ300_RE 			# 创业板
#ZXB_RE = SZ002_RE 			# 中小板

# -------------------------
DEFAULT_CODE_RE = '.*' 		# 默认正则，匹配任意个任意字符（即表示任何股票代码都符合条件）

# ---------------------------------------
# 为方便用户输入，定义一些各种可接受并表示某一类股票的标志，只要用户输入 list 内任一标志，就表示该类股票
SH60_SYMBOL_ARR = [SH60,SH60_RE,'6','60',6,60] 				# 定义一个各种可表示上证 60 开头的股票的识别标志
SH688_SYMBOL_ARR = [SH688,SH688_RE,'688',688,'KCB'] 		# 定义一个各种可表示科创板（688开头的股票）股票的识别标志
SZ00_SYMBOL_ARR = [SZ00,SZ00_RE,'00',0] 					# 定义一个各种可表示深证 00 开头的股票的识别标志
SZ300_SYMBOL_ARR = [SZ300,SZ300_RE,'300',300,'CYB'] 		# 定义一个各种可表示深证 创业板（即300开头的股票）股票的识别标志
# ------------------------------------
# -------------------------------
# 各类规则

# 基本时间字典
BASIC_TIME_DICT = {
	'OPEN_TIME': OPEN_TIME,

	'STOP_WITHDRAW_TIME': STOP_WITHDRAW_TIME,
	'OPEN_PRICE_TIME': OPEN_PRICE_TIME,

	'AM_START_TIME': AM_START_TIME,
	'AM_STOP_TIME': AM_STOP_TIME,

	'PM_START_TIME': PM_START_TIME,
	'PM_STOP_TIME': PM_STOP_TIME,

	'CLOSE_TIME': CLOSE_TIME
	}

BASIC_ONE_HAND_DICT = {
	'ONE_HAND': ONE_HAND
	}

BASIC_UP_DOWN_LIMIT10_DICT = {
	'UP_LIMIT': UP_LIMIT10,
	'DOWN_LIMIT': DOWN_LIMIT10
	}

BASIC_UP_DOWN_LIMIT20_DICT = {
	'UP_LIMIT': UP_LIMIT20,
	'DOWN_LIMIT': DOWN_LIMIT20
	}

BASIC_T0_DICT = {
	'T': T0
	}

BASIC_T1_DICT = {
	'T': T1
	}

BASIC_FEE_DICT = {
	'BUY_TAX_RATE': BUY_TAX_RATE,
	'SELL_TAX_RATE': SELL_TAX_RATE,
	'BUY_TRANSFER_FEE_RATE': BUY_TRANSFER_FEE_RATE,
	'SELL_TRANSFER_FEE_RATE': SELL_TRANSFER_FEE_RATE
	}




# --------------------------------
RULE_DICT = {
	"DEFAULT": dict(**{'CODE_RE':DEFAULT_CODE_RE},**BASIC_TIME_DICT,**BASIC_ONE_HAND_DICT,**BASIC_UP_DOWN_LIMIT10_DICT,**BASIC_T1_DICT,**BASIC_FEE_DICT), 		# 默认交易规则
	
	SH60: dict(**{'CODE_RE':SH60_RE},**BASIC_TIME_DICT,**BASIC_ONE_HAND_DICT,**BASIC_UP_DOWN_LIMIT10_DICT,**BASIC_T1_DICT,**BASIC_FEE_DICT), 		# 沪市 60 开头股票代码交易规则
	SH688: dict(**{'CODE_RE':SH688_RE},**BASIC_TIME_DICT,**BASIC_ONE_HAND_DICT,**BASIC_UP_DOWN_LIMIT20_DICT,**BASIC_T1_DICT,**BASIC_FEE_DICT),		# 沪市 688 开头股票代码交易规则

	SZ00: dict(**{'CODE_RE':SZ00_RE},**BASIC_TIME_DICT,**BASIC_ONE_HAND_DICT,**BASIC_UP_DOWN_LIMIT10_DICT,**BASIC_T1_DICT,**BASIC_FEE_DICT), 		# 深市 00 开头股票代码交易规则
	SZ300: dict(**{'CODE_RE':SZ300_RE},**BASIC_TIME_DICT,**BASIC_ONE_HAND_DICT,**BASIC_UP_DOWN_LIMIT20_DICT,**BASIC_T1_DICT,**BASIC_FEE_DICT) 		# 深市 300 开头股票代码交易规则
	}



DEFAULT_RULE_DICT = RULE_DICT['DEFAULT']



