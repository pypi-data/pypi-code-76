#coding=utf-8

"""
作者：xjxfly
邮箱：xjxfly@qq.com

说明：
这是中国股市规则库
调用本模块中的各接口，将返回中国股市中各类别股票的交易规则

"""


from . import common_config as cf

# --------------------------------------------------


def get_rule(code_type=None):
	"""
	说明：根据传入的股票代码类别，返回该类别的交易规则
	参数：code_type：股票代码类别，可取值为 cf.RULE_DICT 中的 key，或接受下面出错提示那些值；若 code_type 为 None，则返回 DEFAULT 所指向的规则
	返回值：该类型交易规则（dict 形式）
	"""
	rule_dict = None 		# 初始化股市规则字典为  None
	if code_type is None:
		rule_dict = cf.DEFAULT_RULE_DICT
	else:
		code_type = str(code_type).upper() 		# 转成小写
		if code_type in cf.SH60_SYMBOL_ARR:
			code_type = cf.SH60

		if code_type in cf.SH688_SYMBOL_ARR:
			code_type = cf.SH688

		if code_type in cf.SZ00_SYMBOL_ARR:
			code_type = cf.SZ00

		if code_type in cf.SZ300_SYMBOL_ARR:
			code_type = cf.SZ300

		# -------------------
		if code_type in cf.RULE_DICT: 		# 这种表达式表示在 cf.RULE_DICT 是否一个键为 code_type , 如果有，下面这行就取这个键对应的值（在这里，值本身又是一个 dict）
			rule_dict = cf.RULE_DICT[code_type]
		else:
			print('错误！请确保传入的参数 code_type 只能取以下值之一，然后本函数将返回对应股票类型的交易规则（字典形式）：')
			print(cf.SH60_SYMBOL_ARR)
			print(cf.SH688_SYMBOL_ARR)
			print(cf.SZ00_SYMBOL_ARR)
			print(cf.SZ300_SYMBOL_ARR)
			#print(list(cf.RULE_DICT.keys()))

	return rule_dict








def get_prefixed_stock_code(code,by='letter',index=False):
	"""
	说明：对传入的股票代码加上市场前缀后返回
	参数：code ，6位数的股票代码（字符串形式）；by 表示加何种前缀，可取值为'letter'和'number'，letter表示加字符前缀，如'sh',number表示加数字前缀，如'0'；
		index 表示传入的 code 是否为指数，默认为 False，表示传入的是普通股票代码
	返回值：加上市场前缀后的股票代码（字符串形式）
	"""
	prefixed_stock_code = None			# 初始化一个变量，用于保存加前缀后的股票代码
	# ------------------------------------
	# 先判断股票代码是否已加了市场前缀'sh' 或 'sz'，如果已经加了市场前缀就不用管他是否是指数，表明用户明确知道自己输入了市场前缀和股票代码
	market_code = code[0:2] 					# 取股票代码的前两位，以判断是否已经加了市场前缀码（'sh','sz'），如果已经加过了就直接返回，无需再添加
	market_code = market_code.lower()
	if market_code == cf.SH_LETTER_PREFIX:
		if by == 'letter':
			prefixed_stock_code = code
		if by == 'number':
			prefixed_stock_code = cf.SH_NUMBER_PREFIX + code[2:] 			# 把股票代码前的字母市场前缀换成数字市场前缀
		return prefixed_stock_code

	if market_code == cf.SZ_LETTER_PREFIX:
		if by == 'letter':
			prefixed_stock_code = code
		if by == 'number':
			prefixed_stock_code = cf.SZ_NUMBER_PREFIX + code[2:] 			# 把股票代码前的字母市场前缀换成数字市场前缀
		return prefixed_stock_code

	# -----------------------------
	# 普通股票代码进入这个 if	
	if index == False:
		market_code = code[0:1]
		if market_code in cf.SH_LEAD_CODE_ARR:
			if by == 'letter':
				prefixed_stock_code = cf.SH_LETTER_PREFIX + code
			if by == 'number':
				prefixed_stock_code = cf.SH_NUMBER_PREFIX + code

		if market_code in cf.SZ_LEAD_CODE_ARR:
			if by == 'letter':
				prefixed_stock_code = cf.SZ_LETTER_PREFIX + code
			if by == 'number':
				prefixed_stock_code = cf.SZ_NUMBER_PREFIX + code
	# -----------------
	# 沪深两市指数代码进入这个 if
	if index == True:
		market_code = code[0:2] 		# 这里取2个字符，沪市各种指数代码前两个字符一般为00，所以提取2个字符来判断
		if market_code in cf.SH_INDEX_LEAD_CODE_ARR:
			if by == 'letter':
				prefixed_stock_code = cf.SH_LETTER_PREFIX + code
			if by == 'number':
				prefixed_stock_code = cf.SH_NUMBER_PREFIX + code

		market_code = code[0:3] 		# 这里取3个字符，深市各种指数代码前3个字符一般为399，所以提取3个字符来判断
		if market_code in cf.SZ_INDEX_LEAD_CODE_ARR:
			if by == 'letter':
				prefixed_stock_code = cf.SZ_LETTER_PREFIX + code
			if by == 'number':
				prefixed_stock_code = cf.SZ_NUMBER_PREFIX + code

	return prefixed_stock_code








def get_index_code(index_name = 'shzz'):
	"""
	说明：根据输入的指数名称，返回相应的指数代码
	参数：index_name, 指数名称，可取值是：'shzz'(上证综指)，'szcz'(深证成指)等 
	返回值：6位数的上证综指代码（字符串形式）
	"""
	if index_name == 'shzz':
		return cf.SH_INDEX_DICT['SHZZ']

	if index_name == 'szcz':
		return cf.SZ_INDEX_DICT['SZCZ']




