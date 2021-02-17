#coding=utf-8

"""
作者：xjxfly
邮箱：xjxfly@qq.com

申明：
1. 这是爬虫包，调用本包中的接口，将直接从公开网站拿公开数据.

2. 本包作者不对数据的真实性，准确性，时效性等负责，本包接口返回的数据都是来自公开网站的公开数据。
	调用者调用本包接口返回数据用于决策、计算等等，引发的自身经济损失或法律问题由使用者自己承担，和本包作者无关。

3. 本包仅用于学习研究，禁止用来向各接口所指向的网站发起攻击或频繁调用使其不堪重负或瘫痪。
"""

import pandas as pd
import random
import time
import datetime
import math
import json

import requests 		# 好用的爬虫请求库，比下面的 urllib 好用
import selenium 		# 用于浏览器自动化
import bs4 				# 用于解析 html 

from urllib.request import urlopen, Request
from selenium import webdriver 				# 用于浏览器自动化

import jxbase as jxb 						# 引入自定义基础包
import cnstock 								# 引入中国股市规则包

from . import common_config as cf 			# 引入本包的配置文件


#########=====================================================


# ------------------------------------------------
# ------------------------------------------------
# functions start here

# ---------------------------------
# basic and common interface start

# 先从自定义中国股市规则包 cnstock 获取交易规则（以字典形式返回）
stock_default_rule_dict = cnstock.get_rule() 					# 获取中国股市默认交易规则
stock_300_rule_dict = cnstock.get_rule(code_type='sz300') 		# 获取深证300创业板交易规则







def is_trade_date():
	'''
	说明：判断今天是否交易日。该函数通过从获取指数（上证综指）的实时数据中提取日期，以判断今天是否交易日。
		注意：只有在开盘后调用才有用，所以建议在 9：15 后调用本函数，否则不准。
	参数：无 
	返回值：交易日返回 True, 非交易日返回 False. 无法判断返回 None.
	'''
	func_name = jxb.get_current_function_name() + ': '
	if time.time() <= jxb.get_timestamp(xtime=stock_default_rule_dict['OPEN_TIME']):
		print(jxb.get_current_time(),func_name,' 本函数是针对实盘判断是否交易日的，请在 %s 开盘后调用。' % (stock_default_rule_dict['OPEN_TIME']))
		return None
	xtoday = jxb.get_today()
	# shzz = '000001' 			# 这句也是正确的，但为了防止数据分散造成混乱，采用下面这一句，让所有地方的指数都从 cnstock 这个包获取
	shzz = cnstock.get_index_code() 			# 获取上证综指代码（不加参数默认就是返回上证综指代码）
	df = get_sina_realtime_stock_data(code_arr=[shzz],index=True)
	if df is None:
		df = get_netease_realtime_stock_data(code_arr=[shzz],index=True) 
		if df is None:
			print(jxb.get_current_time(),func_name,'由于 get_sina_realtime_stock_data() 和 get_netease_realtime_stock_data() 没有返回实时数据，本函数无法判断今天是否交易日，将返回 None')
			return None

	if str(df.ix[0,'date']) == str(xtoday):
		return True
	else:
		return False






def get_realtime_stock_data(code_arr,index=False,source='sina'):
	"""
	说明：根据传入的股票代码数组，调用相应的实时数据接口获取实时数据，以 df 形式返回
	参数：code_arr, 待取实时数据的股票代码列表，index 表明是否指数；source: 表示从哪个源获取，取值为'sina','SINA','netease','NETEASE'
	返回值：相应股票的实时数据，df 格式
	"""
	if source in ['sina','SINA']:
		df = get_sina_realtime_stock_data(code_arr=code_arr,index=index)

	if source in ['netease','NETEASE']:
		df = get_netease_realtime_stock_data(code_arr=code_arr,index=index)

	return  df








def get_k_data(code,xbegin=None,xend=None,index=False,source='netease'):
	"""
	说明：这是和上述 get_netease_k_data() 函数一样的，是对上述这个函数的封装
	"""
	df = None
	if source in ['netease','NETEASE']:
		df = get_netease_k_data(code=code, xbegin=xbegin, xend=xend, index=index)
	
	return df







def get_stock_fund_flow(code,index=False,source='tencent'):
	"""
	说明：从指定源获取指定股票的主力和散户资金流向
	参数：code: 需要获取资金流行的股票代码; index: 是否指数，一般设为 False；source: 从哪个源获取
	返回值：资金流向数据（df 格式）
	"""
	df = None
	if source in ['tencent','TENCENT','qq','QQ']:
		df = get_tencent_stock_fund_flow(code=code,index=index)

	return df







def get_all_code(source='eastmoney'):
	"""
	说明：到指定的源去取所有股代码，默认到东财爬所有股
	参数：source: 数据源。
	返回值：list, 元素为股票代码
	"""
	if source == 'eastmoney':
		all_code_arr = get_all_code_from_eastmoney()

	return all_code_arr





def make_header():
	"""
	说明：构造一个 http 请求头返回
	"""
	# 构造一个 dict 形式的 http 请求头
	header = {
		'Connection': 'Keep-Alive',
		'Accept': 'text/html, application/xhtml+xml, */*',
		'Accept-Language':'zh-CN,zh;q=0.8',
		#'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
		}
	return header









def get_page_by_urllib(url,header=None):
	"""
	说明：下载（获取）指定 URL 的页面源码。本接口作为候选接口，请优先选用下面的 get_page_by_requests() 接口
	参数：url：目标地址; headers: 请求头，若没有传入，则由本函数自己调用请求头。
	返回值：url 指向的 page_source（本函数已经将取到的 page_source  decode() 成字符串形式（纯文本））
	"""
	if header is None:
		header = make_header()
	req = Request(url,headers=header)
	opener = urlopen(req)
	# charset = opener.info().get_content_charset() 		# 这句和下面这句是一样的，只需用一句即可
	charset = opener.headers.get_content_charset() 			# 从返回的字节流中提取字符编码方式，待会后面要用到
	if charset is not None:
		page_source = opener.read().decode(charset) 		# 用上一句读取到的编码方式不是 None ，则用它进行解码
	else:
		page_source = opener.read().decode() 				# 若 charset 为 None，则用不带参数的 decode() 解码

	return page_source  	







def get_page_by_requests(url,header=None):
	"""
	说明：下载（获取）指定 URL 的页面源码。对于静态 html 或网站能直接提供数据的（包括api形式，string 形式，json形式等），
		请优先使用本接口去获取数据，次选上面的 get_page_by_urllib() 接口；
		若网站的数据没有直接给，而是用 js 方式提供的话，则请调用下面的 get_page_by_browser() 方式去获取，它是模拟浏览器的
	参数：url：目标地址; headers: 请求头，若没有传入，则由本函数自己调用请求头。
	返回值：url 指向的 page_source（本函数已经将取到的 page_source  decode() 成字符串形式（纯文本））
	"""
	if header is None:
		header = make_header()
	response = requests.get(url,headers=header)
	#charset = response.encoding 			# 从返回的字节流中提取字符编码方式，待会后面可能要用到
	page_source = response.text 			# 获取纯文本的网页源码

	return page_source  	








def get_page_by_browser(url,browser=None):
	"""
	说明：通过浏览器下载（获取）指定 URL 的页面源码）
	参数：url：目标网页地址; browser: 指定浏览器程序名，可以是包含驱动器的全路径
	返回值： 页面源码 page_source（已经是纯文本形式（即字符串），无需再调用 decode() 解码，要不然要出错）
	"""
	browser_driver = get_browser_driver(browser=browser)
	if browser_driver is None:
		return None

	browser_driver.get(url)
	page_source = browser_driver.page_source

	return page_source






def get_browser_driver(browser="phantomjs.exe"):
	"""
	功能说明：根据传入的浏览器（可以全路径文件名）程序，返回一个 selenium 处理后的 webdriver，用于浏览器自动化
	若用户没有 phantomjs.exe 浏览器，可到以下链接下载（下载后将 phantomjs.exe 解压出来放到 path 所指的一条路径即可）：
	https://phantomjs.org/download.html
	https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip
	"""
	browser_driver = None
	#browser_driver = webdriver.PhantomJS(browser, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any']) 
	try:	
		browser_driver = webdriver.PhantomJS(browser)
	except:
		print("错误！没检测到 PhantomJS 浏览器。如果还没安装可到以下网址下载安装。")
		print("如果已经安装，请将 phantomjs.exe 所在路径添加到系统 path 中。")
		print("phantomjs 下载地址：")
		print("	https://phantomjs.org/download.html")
		print("	https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip")

	return browser_driver





def save_page(page_source,filename,mode='a'):
	"""
	说明：把抓下来的网页源码以utf-8 编码保存到到文件
	参数：page_source: 已经 decode 的网页源码； filename: 文件名（可以是全路径）; mode: 表示打开文件模式（是读，是新建，还是追加内容的写等）
	返回值：无
	"""
	try:
		f = open(filename,mode,encoding='utf-8')
		f.write(page_source)
		f.close()
	except:
		print("错误！保存文件出错。")






def get_prefixed_code_arr(code_arr,by='letter',index=False):
	"""
	说明：该函数对传入的股票代码数组 code_arr 中的每一只股加上市场代码前缀（如'sh'或'0' ）后，以数组形式返回
	参数：code_arr: 待加前缀的6位股票代码（字符串形式）构成的数组； by: 取值'letter' 或 'number'，表示加字母前缀（'sh','sz' 等）还是加数字前缀（'0','1'等）
		index: 表示传入的 code_arr 中的股票代码是否指数，取值 True 或 False
	返回值：加了前缀后的股票代码数组
	"""	
	prefixed_code_arr = []

	for i,code in enumerate(code_arr):
		prefixed_code = None
		# 调用 cnstock 包的 get_prefixed_stock_code() 对股票代码加上市前缀（该函数会自动判断股票代码属于哪个市场）
		prefixed_code = cnstock.get_prefixed_stock_code(code=code,by=by,index=index)
		if prefixed_code is not None:
			prefixed_code_arr.append(prefixed_code)

	return prefixed_code_arr








def get_table_from_webpage(page_source=None, format_df=True):
	"""
	说明：从网页源码中提取表格数据返回
	参数：page_source: 通过 request 或 selenium + phantomjs等爬到的网页源码（必须是已经 decode() 过的纯文本（字符串形式））；
		format_df: 表示将网页源码中包含的 <table> 是转成python 的二维 list 还是转成 pandas 的 DataFrame，默认是 True, 表示转成 DataFrame 格式
	返回值：是一个 list, 其中每个元素是对应网页中一个 <table> 的二维 list 或 df，每个 元素 list 或 df 由网页中的一个 <table> 转换而来
	"""
	if page_source is None:
		print('错误！请传入目标网页源码 page_source（且必须已经 decode）')
		return None
	#soup = bs4.BeautifulSoup(page_source,"html5lib") 			# 准备用 lxml 解析网页源码内容 page_source。注意：即便装了 html5lib 模块，在执行这句时也有问题，好像会卡死。
	soup = bs4.BeautifulSoup(page_source,"lxml") 				# 准备用 lxml 解析网页源码内容 page_source. 注意：这里的 page_source 必须是纯文本的字符串，也就是要已经 decode() 过了的

	table_arr = [] 		# 用于存放网页上的一个个表格，这个 list 的元素对应网页上的一个 <table>
	for table in soup.table:
		temp_table = [] 			# 每一个temp_table ,用于保存网页上的一个 table数据，以二维 list 保存
		for row in table:
			row_str = row.get_text(separator=',')
			row_arr = row_str.split(',')
			temp_table.append(row_arr)

		if len(temp_table) > 0:
			if format_df == True:
				temp_table = pd.DataFrame(temp_table) 			# 将二维 list 转成 DataFrame
			table_arr.append(temp_table)

	return table_arr








# basic and common interface end
# ==================================


# ---------------------------------
# sina data start

def get_sina_realtime_stock_data(code_arr,index = False):
	"""
	说明：根据传入的股票代码数组，到新浪获取实时数据，以 df 形式返回，这个函数只是起一个分包作用，真实到新浪调取行情数据的是下面这个 get_sina_realtime_stock_data2()
	参数：code_arr, 待取实时数据的股票代码列表，index 表明是否指数
	返回值：相应股票的实时数据，df 格式
	"""
	package_size = 800 			# 一次拿几只股的实时数据 (新浪一次性最大支持 800只)
	count1 = math.ceil((len(code_arr) / package_size)) 			# 共需几组才能拿完

	all_df = None 				# all_df 用来保存新浪返回的实时行情数据，预设 None
	for i in range(count1):
		df = get_sina_realtime_stock_data2(code_arr = code_arr[i*package_size:(i+1)*package_size],index = index) 			# 新浪允许的最大包为 800 只左右，超过这个值将出错
		if df is None:
			continue
		else:
			if all_df is None:
				#all_df = df.copy(deep=True)
				all_df = df
			else:
				all_df = pd.concat([all_df,df])

	if all_df is not None:
		all_df = all_df.reset_index(drop=True) 		# 由于 pd.concat() 会拼接重复索引，所以这里要 reset_index() 一下，drop=True 表示删除原来的索引 

	return all_df









def get_sina_realtime_stock_data2(code_arr,index = False):
	"""
	说明：根据传入的股票代码数组，到新浪获取实时数据，以 df 形式返回，根据经验最好一次性不超过 800 只
	参数：code_arr, 待取实时数据的股票代码列表，index 表明是否指数
	返回值：df, 相应股票的实时数据，df 格式
	"""
	func_name = jxb.get_current_function_name() + ': '
	if len(code_arr) > 800:
		print(func_name,'错误：请确保单次取新浪实时数据最大不超过 800 只股。')
		return None

	# 构造新浪股票实时行情列头名称。不要更改顺序！				  
	column_arr = [
		'name', 		# 名称
		'code', 		# 代码
		'open', 		# 开盘价（元）
		'last_close', 	# 昨收价（元）
		'price', 		# 市价（元）
		'high', 		# 最高价（元）
		'low', 			# 最低价（元）

		'volume', 		# 成交量（股）
		'amount', 		# 成交额（元）

		'bid1_volume', 	# 买一量（股）
		'bid1_price', 	# 买一价（元）
		'bid2_volume', 	# 买二量（股）
		'bid2_price', 	# 买二价（元）
		'bid3_volume', 	# 买三量（股）
		'bid3_price', 	# 买三价（元）
		'bid4_volume', 	# 买四量（股）
		'bid4_price', 	# 买四价（元）
		'bid5_volume', 	# 买五量（股）
		'bid5_price', 	# 买五价（元）

		'ask1_volume', 	# 卖一量（股）
		'ask1_price', 	# 卖一价（元）
		'ask2_volume', 	# 卖二量（股）
		'ask2_price', 	# 卖二价（元）
		'ask3_volume', 	# 卖三量（股）
		'ask3_price', 	# 卖三价（元）
		'ask4_volume', 	# 卖四量（股）
		'ask4_price', 	# 卖四价（元）
		'ask5_volume', 	# 卖五量（股）
		'ask5_price', 	# 卖五价（元）

		'date', 		# 日期
		'time' 			# 时间
		]

	url = get_sina_realtime_stock_url(code_arr = code_arr, index = index) 		# 把股票 list 串接成符合新浪数据源要求的格式返回
	#xrequest = Request(url) 		# 构造请求格式

	# 设几个初始变量
	data_arr = [] 		# 存放新浪返回的行情数据 
	df = None 			# 存放将上述行情数据转成 dataframe 格式后的数据
	
	retry_count = 20 			# 拉取数据最多尝试次数
	xcount = 1

	while True:
		if xcount > retry_count:
			print(func_name,'错误：拉取数据失败。')
			return None
		try:
			# 下面注释掉的这两句和后面的 get_page_by_requests() 有相同的效果，选用一种就可以了。
			#page_source = urlopen(xrequest,timeout=10).read() 		# 提交请求并读取返回的网页源码
			#page_source = page_source.decode('GBK') 	# 新浪情行返回的数据流要用 GBK 解码
			page_source = get_page_by_requests(url = url) 		# 这个 url 返回的数据已经解码（即已经 decode() 过了）			
		except:
			s = random.randint(1,5)			
			print(func_name,'\n由于发生了错误，或新浪行情服务器未能返回数据，本接口休息 %d 秒后将自动重新尝试拉数据。已尝试 %d / %d 次' % (s, xcount, retry_count))			
			time.sleep(s) 			# 如果被服务器踢，则停止3秒再拉数据
			xcount += 1
			continue
		else:
			# 流程进到这里表示拿到了行情数据，下面对数据进行提取和规范，形成 df 返回
			arr = page_source.split(';')
			for code_str in arr:
				arr2 = code_str.split('"')
				try:
					code = arr2[0][-7:-1] 		# 提取股票代码
					arr2 = arr2[1].split(',')	# 这里是行情各字段数据内容				
				except:
					continue
				if arr2[-1] == '':
					arr2 = arr2[0:-1]
				arr2.insert(1,code) 			# 将股票代码插在第2个元素位置，（第一个为股票名称）
				arr2 = arr2[0:7] + arr2[9:] 	# 将返回的数据去掉重复部分，以适配上面构造的列名称
				if len(arr2) > len(column_arr):
					arr2 = arr2[:len(column_arr)]
				data_arr.append(arr2)

			df = pd.DataFrame(data = data_arr, columns = column_arr) 			# 构造 DF， 并配上列头

			"""
			# 上面得到 df 后，把没有用的一些列去掉，即 temp开头的
			for i,col in enumerate(column_arr):
				if col.startswith('temp') == True:
					df.pop(col)
			"""
			# 股票代码要转成字符串，并补足前导0，所以这里要将其转成字符串，并调用字符串的方法右对齐左侧补数个 char 直到有 width 个: rjust(width,char)
			df['code'] = df['code'].astype(dtype=str).str.rjust(6,'0') 					
			# ------------------------------------------------------
			# 获取市价。这个细节处理要注意，因为 9：25前返回的数据里没有 price, open, high, low ，但有 bid1 价格，就用 bid1填充他们
			# 所以判断当前时间，若已过了 9：25 ，则用 price 本身做市价，否则用 bid1 做市价
			if index == False and  is_trade_date() == True and jxb.get_timestamp(xtime = stock_default_rule_dict['OPEN_TIME']) <= time.time() <= jxb.get_timestamp(xtime = stock_default_rule_dict['OPEN_PRICE_TIME']):
				df['open'] = df['bid1_price'] 			
				df['high'] = df['bid1_price']
				df['low'] = df['bid1_price']
				df['price'] = df['bid1_price'] 			
			# --------------------------------------------
			# 这些数值列转成 float
			float_column_arr = ['last_close','open','high','low','price','amount','bid1_price','bid2_price','bid3_price','bid4_price','bid5_price','ask1_price','ask2_price','ask3_price','ask4_price','ask5_price']
			df = jxb.convert_df_type(df=df, xtype=float, column_arr=float_column_arr)
			# 这些数值列转成 int
			int_column_arr =  ['volume','bid1_volume','bid2_volume','bid3_volume','bid4_volume','bid5_volume','ask1_volume','ask2_volume','ask3_volume','ask4_volume','ask5_volume']
			df = jxb.convert_df_type(df=df, xtype=int, column_arr=int_column_arr)
			# 调整  df 中的列顺序，使之按 STOCK_COLUMN_ORDER_ARR 中的顺序排列
			df = jxb.sort_df_column(df=df, column_arr=cf.STOCK_COLUMN_ORDER_ARR)
			# ==========================
			df = df.sort_values(by = ['code'],ascending = [True])
			df = df.reset_index(drop = True)
			break

	return df








def get_sina_realtime_stock_url(code_arr, index = False):
	"""
	说明：该函数根据传入的股票代码数组，生成新浪实时股票行情的网址返回
	参数：code_arr: 股票代码列表；index： 表示code_arr 里的股票代码是否表示指数
	返回值：指向新浪实时行情的网址。
	"""
	if code_arr is None or len(code_arr)==0:
		print(jxb.get_current_function_name() + ': 错误！传入的股票代码列表 code_arr 不能为空。')
		return None

	base_url = 'http://hq.sinajs.cn/list=%s' 			# 选择 sina 实时数据源

	prefixed_code_arr = get_prefixed_code_arr(code_arr=code_arr,index=index) 	# 对股票代码数组中的每一只股加上市场代码前缀后返回，仍然是数组形式
	prefixed_code_str = ','.join(prefixed_code_arr)
	prefixed_code_str += ','
	url = base_url % (prefixed_code_str) 		# 将实际值（即 % 后面括号里的值）代入到 base_url 中去

	return url













# sina data end
# ==================================

# ---------------------------------
# netease data start

def get_netease_realtime_stock_data(code_arr,index = False):
	"""
	说明：根据传入的股票代码数组，到网易获取实时数据，以 df 形式返回，这个函数只是起一个分包作用，真实到网易调取行情数据的是下面这个 get_netease_realtime_stock_data2()
	参数：code_arr, 待取实时数据的股票代码列表，index 表明是否指数
	返回值：df, 相应股票的实时数据，df 格式
	"""
	package_size = 1000 			# 一次拿几只股的实时数据 (网易一次性最大支持 1000只)
	count1 = math.ceil((len(code_arr) / package_size)) 			# 共需几组才能拿完

	all_df = None 				# all_df 用来保存网易返回的实时行情数据，预设 None
	for i in range(count1):
		df = get_netease_realtime_stock_data2(code_arr = code_arr[i*package_size:(i+1)*package_size],index = index) 			# 允许的最大包为 1000 只左右，超过这个值将出错
		if df is None:
			continue
		else:
			if all_df is None:
				all_df = df.copy(deep=True)
			else:
				all_df = pd.concat([all_df,df])

	if all_df is not None:
		all_df = all_df.reset_index(drop=True) 		# 由于 pd.concat() 会拼接重复索引，所以这里要 reset_index() 一下，drop=True 表示删除原来的索引 

	return all_df








def get_netease_realtime_stock_data2(code_arr,index = False):
	"""
	说明：根据传入的股票代码数组，根据经验最好一次性不超过 1000 只，到网易netease 获取实时数据，以 df 形式返回
	参数：code_arr, 待取实时数据的股票代码列表，index 表示是否是指数，默认 False
	返回值：df, 相应股票的实时数据，df 格式
	"""
	func_name = jxb.get_current_function_name() + ': '
	if len(code_arr) > 1000:
		print(func_name,'错误：请确保单次取实时数据最大不超过 1000 只股。')
		return None

	# 构造网易股票实时行情列头名称，不要更改顺序！				  
	column_arr = [
		'ask1_price', 	# 卖一价（元）
		'ask2_price', 	# 卖二价（元）
		'ask3_price', 	# 卖三价（元）
		'ask4_price', 	# 卖四价（元）
		'ask5_price', 	# 卖五价（元）
		'ask1_volume', 	# 卖一量（股）
		'ask2_volume', 	# 卖二量（股）
		'ask3_volume', 	# 卖三量（股）
		'ask4_volume', 	# 卖四量（股）
		'ask5_volume', 	# 卖五量（股）

		'bid1_price', 	# 买一价（元）
		'bid2_price', 	# 买二价（元）
		'bid3_price', 	# 买三价（元）
		'bid4_price', 	# 买四价（元）
		'bid5_price', 	# 买五价（元）
		'bid1_volume', 	# 买一量（股）
		'bid2_volume', 	# 买二量（股）
		'bid3_volume', 	# 买三量（股）
		'bid4_volume', 	# 买四量（股）
		'bid5_volume', 	# 买五量（股）

		'high', 		# 最高价（元）
		'low', 			# 最低价（元）
		'name', 		# 名称
		'open', 		# 开盘价（元）
		'percent', 		# 涨幅（用小数表示真实涨幅，例：0.02 就表示涨2%）
		'price', 		# 市价（元）
		'code', 		# 代码

		'amount', 		# 成交额（元）
		'change', 		# 涨跌（元）
		'volume', 		# 成交量（股）

		'last_close', 	# 昨收价（元）

		'date', 		# 日期
		'time'			# 时间		
		]

	url = get_netease_realtime_stock_url(code_arr = code_arr,index = index)
	df = None
	retry_count = 20
	xcount = 1
	while True:
		if xcount > retry_count:
			print(func_name,'错误：拉取数据失败。')			
			return None
		try:
			# 这两句都是正确的，随便用哪句都可以。只是用不同的模块来实现相同的功能
			#page_source = get_page_by_urllib(url = url) 		# 这个 url 返回的数据已经解码（即已经 decode() 过了）
			page_source = get_page_by_requests(url = url) 		# 这个 url 返回的数据已经解码（即已经 decode() 过了）
		except:
			s = random.randint(1,5)
			print(func_name,'\n由于发生错误，或网易行情服务器未能返回数据，本线程休息 %d 秒后将自动继续尝试拉数据。已尝试 %d / %d 次' % (s, xcount, retry_count))
			time.sleep(s) 			# 如果被服务器踢，则停止几秒再拉数据
			xcount += 1
			continue
		else:
			#page_source = page_source.decode('utf-8') 		# 将字节流解码为 utf8 字符串，以便后续处理
			# 从网易返回的实时数据看，取这个范围可以得到 json 格式的股票实时数据
			data_json = page_source[21:-2] 		
			df = pd.read_json(data_json, orient='index') 		# orient 取 'index' 也是从上面返回的 json 数据分析而来的，read_json() 的具体参数请查阅pandas
			# 把 time 列按空格拆分成两列形成 df 返回(expand=True 表示形成 df，否则是 list)
			date_time_df = df.time.str.split(' ',expand=True) 	# 将 time列（观察网易返回的数据中的 time 列包含了日期和时间，两者以空格分隔）分成两列，expand=True 表示以 DF 形式返回
			date_time_df.columns=['date','time'] 				# 配上（或叫更改）列名
			# 删除以下这些列
			for col in ['arrow','code','status','type','update','time']:
				df.pop(col)

			#df[date_time_df.columns] = date_time_df 		# 这句也是正确的，但用下面这句更清晰一些
			df = pd.concat([df,date_time_df], axis=1) 		# axis=1 表示拼列（若不指定 axis则其默认值为 0，表示拼行）
			df['date'] = df['date'].str.replace('/','-') 	# 网易实时数据返回的 date 列是 / 分割的，这里将其转成 - 分割
			# 替换 df 的列名到 column_arr 中指定的列名，注意：column_arr 中的顺序不能随意调整，它是事先了解了 df 中的顺序后编排的。
			df.columns = column_arr 		
			# 下面的 code 列就是股票代码。由于 pandas.read_json() 后将股票代码当作了数值并去掉了前导0，
			# 所以这里要将其转成字符串，并调用字符串的方法右对齐左侧补数个 char 直到有 width 个: rjust(width,char)
			df['code'] = df['code'].astype(dtype=str).str.rjust(6,'0') 		
			# ------------------------------------------------------
			# 获取市价。这个细节处理要注意，因为 9：25前返回的数据里没有 price, open, high, low ，但有 bid1 价格，就用 bid1填充他们
			# 所以判断当前时间，若已过了 9：25 ，则用 price 本身做市价，否则用 bid1 做市价
			if index == False and is_trade_date() == True and jxb.get_timestamp(xtime = stock_default_rule_dict['OPEN_TIME']) <= time.time() <= jxb.get_timestamp(xtime = stock_default_rule_dict['OPEN_PRICE_TIME']):
				df['open'] = df['bid1_price'] 			
				df['high'] = df['bid1_price']
				df['low'] = df['bid1_price']
				df['price'] = df['bid1_price'] 			
			# --------------------------------------------
			# 这些数值列转成 float
			float_column_arr = ['last_close','open','high','low','price','amount','bid1_price','bid2_price','bid3_price','bid4_price','bid5_price','ask1_price','ask2_price','ask3_price','ask4_price','ask5_price','change','percent']
			df = jxb.convert_df_type(df=df, xtype=float, column_arr=float_column_arr)
			# 这些数值列转成 int
			int_column_arr =  ['volume','bid1_volume','bid2_volume','bid3_volume','bid4_volume','bid5_volume','ask1_volume','ask2_volume','ask3_volume','ask4_volume','ask5_volume']
			df = jxb.convert_df_type(df=df, xtype=int, column_arr=int_column_arr)
			# 调整  df 中的列顺序，使之按 STOCK_COLUMN_ORDER_ARR 中的顺序排列
			df = jxb.sort_df_column(df=df, column_arr=cf.STOCK_COLUMN_ORDER_ARR)
			# ==========================
			df = df.sort_values(by = ['code'],ascending = [True])
			df = df.reset_index(drop = True)
			break

	return df








def get_netease_realtime_stock_url(code_arr,index=False):
	"""
	说明：该函数根据传入的股票代码数组，生成网易 netease 实时股票行情的网址返回
	参数：code_arr: 股票代码列表；index： 表示code_arr 里的股票代码是否表示指数
	返回值：指向网易 netease 实时行情的网址。
	"""
	if code_arr is None or len(code_arr)==0:
		print(jxb.get_current_function_name() + ': 错误！传入的股票代码列表 code_arr 不能为空。')
		return None

	base_url='http://api.money.126.net/data/feed/%smoney.api' 			# 选择 netease 实时数据源	

	prefixed_code_arr = get_prefixed_code_arr(code_arr=code_arr,by='number',index=index) 	# 对股票代码数组中的每一只股加上市场代码前缀后返回，仍然是数组形式
	prefixed_code_str = ','.join(prefixed_code_arr)
	prefixed_code_str += ',' 
	url = base_url % (prefixed_code_str) 		# 将实际值（即 % 后面括号里的值）代入到 base_url 中去

	return url









def get_netease_k_data(code,xbegin=None,xend=None,index=False):
	"""
	说明：该函数从网易获取K线数据
	参数：code: 股票代码；xbegin: 起始日期；xend: 结束日期； index: 是否指数
	返回值：K线数据（df 格式）
	"""
	func_name = jxb.get_current_function_name() + ': '
	if str(xbegin) > str(xend):
		print(func_name + '错误！请确保起始日期小于或等于结束日期')
		return None
	
	print(func_name, "注意：网易返回的 K线数据可能不是十分准确，请小心使用！")

	# 要从网易拉取历史K线数据的各列名称（不要改变顺序）：
	k_col_arr = [
		'date', 			# 日期
		'code', 			# 股票代码
		'name', 			# 股票名称
		'open', 			# 开盘价（元）
		'high', 			# 最高价（元）
		'low', 				# 最低价（元）
		'close', 			# 收盘价（元）
		'last_close', 		# 昨收价（元）
		'change', 			# 涨跌额（元）
		'percent', 			# 涨幅（用小数表示真实涨幅）
		'volume', 			# 成交量（股）
		'amount', 			# 成交额（元）
		'turnover', 		# 换手率（用小数表示真实换手率）
		'total_value', 		# 总市值（元）
		'circulation_value' # 流通值（元）
		]

	k_df = None 			# 该变量用于存放K线数据（dataframe 格式），赋初值 None
	url = get_netease_k_data_url(code=code,xbegin=xbegin,xend=xend,index=index) 		# 根据指定的股票代码和日期范围，生成网易K线数据源 url 
	retry_count = 10 			# 计数器，表示尝试几次
	xcount = 0
	# 用循环和异常拉数据，因为拉数据时太频繁经常要被服务器踢
	while True:
		if xcount > retry_count:
			return None
		try:
			# 下面两句是一样的，随便用哪句都可以，他们只是用不同的模块来实现相同的功能
			#page_source = get_page_by_urllib(url=url) 				# 到指定的数据源网址下载数据（这里下载下来是包含数据的页面源码，已解码，已经是纯文本格式）
			#page_source=page_source.decode('gbk')
			page_source = get_page_by_requests(url=url) 				# 到指定的数据源网址下载数据（这里下载下来是包含数据的页面源码，已解码，已经是纯文本格式）
		except:
			s = random.randint(1,5)
			print(func_name,'\n可能节假日休息，没能从网易取到 K 线数据，休息 %s 秒后将自动继续尝试拉数据。' % (str(s)))
			time.sleep(s) 			# 如果被服务器踢，则停止3秒再拉数据
			xcount += 1
			continue
		else:
			break

	page_arr = page_source.split('\r\n') 		# 返回的 page是一条长长的字符，以分割符 \r\n 将这长长的字符串切断，并把每段字符串保存到数组 page_arr 中
	col_arr = page_arr[0].split(',') 			# page_arr 中第一个元素（即字符串）为中文列名串接，提取这些列名到数组 col_arr 中
	if len(page_arr) >= 2:
		k_data_arr = page_arr[1:] 			# 从 page_arr 中的第2个元素开始为真正的 k 线数据，但这里他们仍是字符串形式的，需要转化成数组

		k_data_arr = [x.replace("'",'') for x in k_data_arr] 		# 把上述 k_data_arr 中的所有 K线数据中的 ' 号替换为空，即去掉 ' 号
		k_data_arr = [x.split(',') for x in k_data_arr] 			# 将 k_data_arr 中每一行字符串形式的K线数据，转换成 list 形式，这样转换后， k_data_arr 中的每一个元素都成了数组
		k_data_arr = k_data_arr[:len(k_data_arr)-1] 				# 因为网易返回的数据最后一行全是 None ，所以要去掉

		k_df = pd.DataFrame(data=k_data_arr,columns=k_col_arr)  	# 把数组形式的K线数据，转换成 DataFrame 形式，以便进一步操作
		k_df.code = code 			# 加这一句的目的是因为传入的指数代码与网易数据源所需的指数代码形式不同所致，从网易拿回数据后，将指数代码恢复成我们自己传入的指数代码形式

		if len(k_df)>0:
			k_df = k_df.sort_values(by=['date'],ascending=True)
			k_df = k_df.reset_index(drop=True) 					# 用自然数行索引去替换原行索引
			#k_df = wash_data(df=k_df,ds=ds,index=index) 		# 再调用自定义函数清洗
			k_df = wash_netease_k_data(df=k_df, index=index) 	# 调用网易K线处理函数
			# --------------------------------------------
			# 这些数值列转成 float
			float_column_arr = ['open','high','low','close','last_close','change','percent','amount','turnover','total_value','circulation_value']
			k_df = jxb.convert_df_type(df=k_df, xtype=float, column_arr=float_column_arr)
			# 这些数值列转成 int
			int_column_arr =  ['volume']
			k_df = jxb.convert_df_type(df=k_df, xtype=int, column_arr=int_column_arr)
			for col in ['percent','turnover']:
				k_df[col] /= 100 				# 将涨幅和换手率转成小数
			# 调整  df 中的列顺序，使之按 STOCK_COLUMN_ORDER_ARR 中的顺序排列
			k_df = jxb.sort_df_column(df=k_df, column_arr=cf.STOCK_COLUMN_ORDER_ARR)
			# ==========================
			k_df = k_df.sort_values(by=['date'], ascending=[True]) 
			k_df = k_df.reset_index(drop=True)
		
	return k_df









def get_netease_k_data_url(code,xbegin=None,xend=None,index=False):
	"""
	说明：构造网易历史 K线数据源 url
	参数：code: 6位股票代码；xbegin: 开始日期（可以是字符串形式或 python日期格式）；xend: 结束日期； index: 是否指数；
	返回值：url
	"""

	func_name = jxb.get_current_function_name() + ': '	 			# 获取函数名
	xtoday = jxb.get_today()
	if xbegin is None:
		xbegin = datetime.date(xtoday.year,1,1) 					# 构造本年第1天
	if xend is None:
		xend = xtoday

	url = ''
	base_url = 'http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s&fields=TOPEN;HIGH;LOW;TCLOSE;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER;TURNOVER;TCAP;MCAP' 		# 网易历史数据源

	if (not jxb.is_valid_date(str(xbegin))) or (not jxb.is_valid_date(str(xend))):
		print(func_name + '输入的日期或格式有误')
		return None

	d1 = ''.join(str(xbegin).split('-')) 		# 调整日期格式，以适应163接口
	d2 = ''.join(str(xend).split('-'))
	#prefixed_code_arr = get_prefixed_code_arr(code_arr=[code],by='number',index=index) 	# 对股票代码数组中的每一只股加上市场代码前缀后返回，仍然是数组形式
	#prefixed_code = prefixed_code_arr[0]
	prefixed_code = cnstock.get_prefixed_stock_code(code=code,by='number',index=index)

	if prefixed_code is not None:
		url = base_url % (prefixed_code,d1,d2) 		# 将实际值（即 % 后面括号里的值）代入到 base_url 中去

	return url









def wash_netease_k_data(df,index=False):
	"""
	说明：对网易K线数据进行处理
	参数：df: 网易K线数据；index: 是否指数
	返回值：处理后的K线数据（df格式）
	"""
	if len(df) == 0:
		return df

	index1_arr = list(df.index)
	code = df.ix[index1_arr[0],'code']

	# 先遍历所有行，去掉 涨跌额为 'None' 的行
	for i in index1_arr:
		if index == True:
			# 指数进入这里
			if df.ix[i,'change'] == 'None':
				if df.ix[i,'last_close'] == 'None':
					df.ix[i,'last_close'] = df.ix[i,'open'] 			# 如果昨收价不存在，一般是首个交易日，则令其昨收价等于今天开盘价，方便程序处理
				df.ix[i,'change']=str(float(df.ix[i,'close']) - float(df.ix[i,'last_close']))
				df.ix[i,'percent']=str((float(df.ix[i,'close']) - float(df.ix[i,'last_close'])) / float(df.ix[i,'last_close']))	
			# 发现中小板指在早期时，即2008-06-27 日及以前的成交额都是 'None', 故用 0 去替换
			if df.ix[i,'amount'] == 'None':
				df.ix[i,'amount'] = 0
		else:
			# 普通股进入这里，因为网易返回的普通股当 change 为'None' 时，则当天的 open,high,low.close等全为0 了，所以这行数据就不要了，直接 drop 掉
			if df.ix[i,'change'] == 'None':
				df = df.drop(i,axis=0)

	df = df.replace(['None'],[0]) 			# 把 raw 数据中剩余的所有'None' 都替换为 0

	if len(df) == 0:
		return df

	# 下面这个 if 是判断指数的，由于指数没有换手率，总市值，流通值等概率，所以给他们置0
	if index == True:
		df['turnover'] = 0
		df['total_value'] = 0
		df['circulation_value'] = 0

	index1_arr=list(df.index)

	# -------------------------------------
	# 这一节是特殊情况特殊处理
	# 1. 对于000046 这只股，在 1994/9/19，1994/9/16，1994/9/15，1994/9/14，1994/9/13，1994/9/12 这6 个交易日里，其换手率数据为 None，流通值也为 0，所以需要补全
	# 好在该股在这些天有总市值数据，并且根据上述日期附近的总市值和流通值之比（大概4倍），可以近似推算出上述6个交易日的，流通值，再利用成交额数据可近似算出换手率
	if code == '000046':
		temp_index_arr = [] 		# 临时数组，用于存放换手率为 None 的那些行标
		for i in index1_arr:
			if df.ix[i,'turnover'] == 'None':
				df.ix[i,'turnover'] = 0
				temp_index_arr.append(i)
		# 把这三列的数据类型先转换成 float （原先是 string 类型，这是网易返回的默认类型），以便下面进行数学计算
		df.amount = df.amount.astype(dtype=float)
		df.turnover = df.turnover.astype(dtype=float)
		df.total_value = df.total_value.astype(dtype=float)
		df.circulation_value = df.circulation_value.astype(dtype=float)
		# 下面计算缺失的换手率和流通值
		for i in temp_index_arr:
			df.ix[i,'circulation_value'] = df.ix[i,'total_value'] * 0.25 			# 先计算出流通值
			df.ix[i,'turnover'] = df.ix[i,'amount'] * 100 / df.ix[i,'circulation_value'] 		# 再计算出换手率

	if code == '600653':
		temp_index_arr = [] 		# 临时数组，用于存放换手率为 None 的那些行标
		for i in index1_arr:
			if df.ix[i,'turnover'] == 'None':
				df.ix[i,'turnover'] = 0
				temp_index_arr.append(i)
		# 把这三列的数据类型先转换成 float （原先是 string 类型，这是网易返回的默认类型），以便下面进行数学计算
		df.amount = df.amount.astype(dtype=float)
		df.turnover = df.turnover.astype(dtype=float)
		df.total_value = df.total_value.astype(dtype=float)
		df.circulation_value = df.circulation_value.astype(dtype=float)
		# 下面计算缺失的换手率和流通值
		for i in temp_index_arr:
			df.ix[i,'circulation_value'] = df.ix[i,'total_value'] * 0.682 			# 先计算出流通值
			df.ix[i,'turnover'] = df.ix[i,'amount'] * 100 / df.ix[i,'circulation_value'] 		# 再计算出换手率

	# 特殊处理到这里结束
	# =====================================

	return df

# netease data end
# ==================================





# ---------------------------------
# tencent data start

def get_tencent_stock_fund_flow(code,index=False):
	"""
	说明：从腾讯源获取指定股票的主力和散户资金流向
	参数：code: 需要获取资金流行的股票代码
	返回值：资金流向数据（df 格式）
	"""
	column_arr = [
		'code', 			# 股票代码
		'main_in', 			# 主力资金流入（元）
		'main_out',			# 主力资金流出（元）
		'main_net_in',		# 流力资金净流入（元）
		'temp1',			# 主力资金流入流出总和
		'personal_in',		# 散户资金流入（元）
		'personal_out', 	# 散户资金流出（元）
		'personal_net_in', 	# 散户资金净流入（元）
		'temp2', 			# 散户资金流入流出总和
		'total_fund_in',		# 资金流入总和（元）
		'temp3',			# 未知1
		'temp4', 			# 未知2
		'name',				# 股票名称
		'date',				# 日期
		]
	
	# 腾讯资金流向数据接口
	base_url = "http://qt.gtimg.cn/q=ff_%s"
	prefixed_code = cnstock.get_prefixed_stock_code(code=code,index=index)
	url = base_url % (prefixed_code)

	page_source = get_page_by_requests(url=url)
	arr = page_source.split('"')
	arr = arr[1].split('~')
	arr = arr[:14]
	# 构造 df
	df = pd.DataFrame(data=[arr],columns=column_arr)
	# 去除无用列（即 temp 开头的列）
	for col in column_arr:
		if col.startswith('temp') == True:
			df.pop(col)
	# ------------------
	# 将数值列(字符串型)转成数值 
	float_column_arr = ['main_in','main_out','main_net_in','personal_in','personal_out','personal_net_in','total_fund_in']
	df = jxb.convert_df_type(df=df, xtype=float, column_arr=float_column_arr)
	# -------------------
	# 将单位转成标准单位
	for col in float_column_arr:
		df[col] *= 10000 			# 将万元为单位的转化成元为单位

	# 列按指定顺序排列
	df = jxb.sort_df_column(df=df,column_arr=cf.STOCK_COLUMN_ORDER_ARR)
	df = df.reset_index(drop=True)

	return df







# tencent data end
# ====================================





# -------------------------------------
# ifeng data start

def get_ifeng_k_data(code,index=False):
	"""
	说明：从凤凰网获取股票K线数据
	参数：code: 股票代码
	返回值：K线数据（df 格式）
	"""
	column_arr = [
		'date',				# 日期
		'open',				# 开盘价（元）
		'high', 			# 最高价（元）
		'close',			# 收盘价（元）
		'low', 				# 最低价（元）
		'volume', 			# 成交量（股）
		'change', 			# 涨跌额（元）
		'percent', 			# 涨跌幅（小数形式）
		'mean_price_5d', 	# 5 日均价（元）
		'mean_price_10d', 	# 10日均价（元）
		'mean_price_20d', 	# 20日均价（元）
		'mean_volume_5d', 	# 5日均量（股）
		'mean_volume_10d', 	# 10日均量（股）
		'mean_volume_20d', 	# 20日均量（股）
		'turnover', 		# 换手率（小数形式）
		]

	base_url = "http://api.finance.ifeng.com/akdaily/?code=%s&type=last"
	prefixed_code = cnstock.get_prefixed_stock_code(code=code,index=index)
	url = base_url % (prefixed_code)
	page_source = get_page_by_requests(url=url)	 		

	s = json.loads(page_source) 		# 凤凰网返回的数据是 json 格式
	data_arr = s['record'] 				# 这是二维 list
	df = pd.DataFrame(data=data_arr,columns=column_arr)
	df['code'] = [code] * len(df) 		# 添加 code 列
	# 将这些列中的逗号替换为空，即去掉。否则这些列无法参与下面的类型转换
	for col in ['volume','mean_volume_5d','mean_volume_10d','mean_volume_20d']:
		df[col] = df[col].str.replace(',','') 			# 注意中间有个 str ，对于非 str 列必须转 str 才能成功执行 replace()
	# ------------------------------------	
	# 这些列的数据类型需要转成 float
	float_column_arr = ['open','high','close','low','volume','change','percent','mean_price_5d','mean_price_10d','mean_price_20d','mean_volume_5d','mean_volume_10d','mean_volume_20d','turnover']
	df = jxb.convert_df_type(df=df, xtype=float, column_arr=float_column_arr)
	# ------------------------------
	# 下面统一单位
	for col in ['percent','turnover']:
		df[col] /= 100 				# 将各类幅度转成小数，即真实幅度
	for col in ['volume','mean_volume_5d','mean_volume_10d','mean_volume_20d']:
		df[col] *= 100 				# 将各类成交量从手转成股
	# ----------------------------
	# 下面调整列和行顺序
	# 列排序
	df = jxb.sort_df_column(df=df,column_arr=cf.STOCK_COLUMN_ORDER_ARR)
	# 行排序
	df = df.sort_values(by=['date'],ascending=[True])
	df = df.reset_index(drop=True)

	return df







# ifeng data end
# =====================================






# ---------------------------------
# eastmoney data start
def eastmoney_table2df(table = None,column_arr = None):
	"""
	说明：本函数的作用是将来自eastmoney.com 的 <table> 行情数据转成 df
	参数：table: 爬自东财的数据表，必须是个二维表，每个元素是一维 list，代表一行数据; column_arr: 是用于构造 df 的列头
	返回值：df
	"""
	if table is None:
		print('请传入来自东财（http://quote.eastmoney.com/center/gridlist.html#hs_a_board）的二维数据表，每个元素是一维 list，代表一行数据')
		return None

	if column_arr is None:
		column_arr = ['code','name','price','percent','change','volume','amount','amplitude','high','low','open','last_close','liangbi','turnover','pe','pb']

	table_arr = []
	for row_arr in table:		
		row_arr = row_arr[1:3] + row_arr[8:] 		# 东财有几个数据列是没用的，必须去掉
		table_arr.append(row_arr)

	table_df = None
	if len(table_arr) > 0:
		table_df = pd.DataFrame(data=table_arr, columns=column_arr)
		# -------------------------
		# 下面开始处理 table 中的一些列
		# 1. 先去除这几列的百分号，转化成纯数字，方便计算
		for col in ['percent','amplitude','turnover']:
			table_df[col] = table_df[col].replace('[%]','',regex = True) 						# 把这 3 列中的 % 去掉，并且除以100
			table_df= jxb.convert_df_type(df=table_df, xtype=float, column_arr=[col]) 			# 注意：这个函数会将数字列中非数字的域填 0 处理！！！
			#table_df[col] = table_df[col].astype(dtype=float) 									# 把字符串转成 float 才能做数学运算
			table_df[col] /= 100

		# -------------------------------------
		# 2. 再去除 volume 列的中文单位（万手或亿手），转化成股
		for col in ['volume','amount']:
			# 分拣
			df1 = table_df[(table_df[col].str.contains('万|亿') == False)] 			# 表示在 table_df.volume列中选取不包含“万”字且不包含“亿”字的记录
			df2 = table_df[(table_df[col].str.contains('万') == True)]  			# 表示在 table_df.volume列中选取只包含“万”字的记录
			df3 = table_df[(table_df[col].str.contains('亿') == True)]  			# 表示在 table_df.volume列中选取只包含“亿”字的记录
			# 替换
			df2[col] = df2[col].replace('[万]','',regex = True) 		
			df3[col] = df3[col].replace('[亿]','',regex = True) 		
			# 转化成数值
			df1 = jxb.convert_df_type(df=df1, column_arr=[col])
			df2 = jxb.convert_df_type(df=df2, column_arr=[col])
			df3 = jxb.convert_df_type(df=df3, column_arr=[col])
			# 转成常规单位
			df1[col] *= 1
			df2[col] *= 10000
			df3[col] *= 100000000

			table_df = pd.concat([df1,df2,df3])

		table_df['volume'] = table_df['volume'].astype(dtype=float) * 100 			# 把以手为单位的成交量转换成股
		# ---------------------------------------
		# 下面对 table_df 的数值列明确转换为数值
		number_column_arr = column_arr[2:]
		table_df = jxb.convert_df_type(df=table_df, xtype=float, column_arr=number_column_arr) 	# 注意：这个函数会将数字列中非数字的域填 0 处理！！！

	return table_df












def get_eastmoney_realtime_stock_data():
	"""
	说明：从东方财富网爬取所有股的实时数据。注意：本接口拿数据比较耗时，不建议用它做实时行情。
	返回值：df 格式的所有股的实时数据
	"""
	# 指定用 phantomjs 浏览器去打开网页
	#browser_driver = webdriver.PhantomJS(browser, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any']) 		
	#browser_driver = webdriver.PhantomJS(browser) 	
	# 东财行情 URL 
	print(jxb.get_current_function_name(),' 请注意，每次调用本函数约需 90 秒才能返回所有股票代码。建议不要频繁调用本函数，以免给网站造成压力。')
	anchor = "#hs_a_board"				# 网页中的锚点
	url = cf.DOMAIN_DICT['EASTMONEY'] + cf.EASTMONEY_PATH_DICT['PATH1'] + anchor

	browser_driver = get_browser_driver()
	if browser_driver is None:
		return None
	# 打开 url 所指页面，返回的页面html代码（含数据）在 browser_driver 这个对象中，并且已经解码过了（浏览器自动解码）是纯文本（字符串）形式
	browser_driver.get(url)

	page_count = 1 			# 页码计数器
	all_df = None
	while True:
		print('正在爬第 %d 页...' % (page_count))
		#print('#',end='') 		# 爬虫进度符
		# 调用 driver 对象的属性 page_source 来提取网页源码及数据（注：浏览器返回的对象已经解码成纯文本（字符串）数据了）
		page_source = browser_driver.page_source
		#page_source = page_source.decode('utf-8') 				# 这句要注释掉， 因为用模拟浏览器方式返回的数据已经是用 utf-8 decode 过了，成了 str 形式，不能重复做 decode()
		soup = bs4.BeautifulSoup(page_source,"lxml") 			# 准备用 lxml 解析网页源码内容 page_source

		table_arr = get_table_from_webpage(page_source=page_source, format_df=False) 		# 东财网返回的数据有两个 <table>，第1个 table 是表头，第2个table 才是真正的数据。
		if table_arr is not None and len(table_arr) >= 2:
			table = table_arr[1]
			df = eastmoney_table2df(table = table)
	
		if all_df is None:
			all_df = df
		else:
			if df is not None:
				all_df = pd.concat([all_df,df])
		# ------------
		# 抓几页
		if page_count >= 5:
			pass
			#break 			# 如果测试的话，打开这个 break，这样只爬5页就停下来，防止爬200多页耗费很多时间
		page_count += 1
		# ------------------
		# soup.find_all() 将返回一个 list,  list 中的元素都是 soup 对象，可以用 .get_text() 方法提取 html 首尾标记之间的内容
		if len(soup.find_all(name='a', attrs='next paginate_button')) > 0 and len(soup.find_all(name='a', attrs='next paginate_button disabled')) == 0:
			browser_driver.find_element_by_xpath("//a[@class='next paginate_button']").click() 		# 点击“下一页”。由于每一页需要在上一页基础上点击下一页才能继续，所以很难用异步方式爬取
		else:
			break

	if all_df is not None:
		all_df = all_df.sort_values(by = ['code'],ascending = True)
		all_df = all_df.reset_index(drop = True)

	# -------------------
	# 使用结束要关闭和退出 browser_driver 对象
	browser_driver.close()
	browser_driver.quit()

	return all_df









def get_all_code_from_eastmoney():
	"""
	说明：从东方财富网爬取所有股票代码
	参数：url 指向数据源网址；browser_pathfile 指向 PhantomJS 浏览器（若其路径没有设置在环境变量 path 中的话，该参数必须用全路径方式）
	返回值：list 形式的股票代码
	"""
	pass
	
	all_df = get_eastmoney_realtime_stock_data()
	all_code_arr = list(set(list(all_df.code)))
	all_code_arr.sort(reverse=False)

	return all_code_arr











# eastmoney data end
# ==================================




# functions end here
# ===========================================
# ==========================================




