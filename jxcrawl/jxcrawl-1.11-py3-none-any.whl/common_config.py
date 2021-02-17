#coding=utf-8

# 全局常量全部放这里

#from common_import import *

"""
作者：xjxfly
邮箱：xjxfly@qq.com
说明：
此脚本为自定义的全局常量

"""
###########################

# 爬虫要访问的网站
DOMAIN_DICT = {
	"EASTMONEY":"http://quote.eastmoney.com"
	}

# 爬虫要访问的网站的路径
EASTMONEY_PATH_DICT = {
	"PATH1":"/center/gridlist.html",
	"PATH2":"/center/gridlist2.html"
	}

# ---------------------------------------

# 定义股票列名顺序，为了使所有行情源返回的数据其字段保持相同的顺序排列，请不要改变下面 list 中的元素顺序，所有行情返回的数据最终都将参照下面这个 list 对列进行排序。（下列中的元素可随意增减或添加程序中不存在的元素，或调整顺序等，都不会导致程序出错）
STOCK_COLUMN_ORDER_ARR =  ['date','time','code','name','last_close','open','high','low','price','volume','amount','ask5_price','ask5_volume','ask4_price','ask4_volume','ask3_price','ask3_volume','ask2_price','ask2_volume','ask1_price','ask1_volume','bid1_price','bid1_volume','bid2_price','bid2_volume','bid3_price','bid3_volume','bid4_price','bid4_volume','bid5_price','bid5_volume']



# ==============================

# -----------------------
# 下面这几个数组都是各种不同类型的垃圾股，在选股时程序会把他们去掉


# ---------------

BAD_WORD_ARR = ['退','ST','st'] 			# 把股票名称中包含这些字符的股都去掉不要

KCB_TYPE_STR = '^688' 			# 科创板股票代码，688 开头

CYB_TYPE_STR = '^300' 			# 创业板股票代码，300 开头



# ------------------



