#coding=utf-8

"""
作者：xjxfly
邮箱：xjxfly@qq.com

说明：
这是通用自定义函数形成的基础库
本模块中出现的 arr 字样，通常是指 list

"""
import time
import datetime
import os
import math
#import itertools 			# 引入支持排列组合的模块
#import copy

from configobj import ConfigObj
#from fractions import Fraction 		# 从分数模块中引入分数函数

import hashlib
import logging

import numpy as np
import pandas as pd

import random
import re
import smtplib
import sys
import tempfile

from urllib.request import urlopen

import uuid

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage  
from email.utils import formataddr

from ftplib import FTP 
from PIL import Image

import pytesseract

from pywinauto import application

import socket
import ctypes
import win32gui

# --------------
from . import common_config as cf 		# 引入自定义常量








#########=====================================================



date_step = datetime.timedelta(days=1)
one_day_step = datetime.timedelta(days=1)



def get_system_encoding():
	"""
	功能说明：获取操作系统的编码字符集
	"""
	#获取系统字符集
	system_encoding = sys.getfilesystemencoding()

	return system_encoding









def get_current_path(script_name,style='UNIX'):
	"""
	功能说明：根据传入的脚本文件名，返回其所在的当前路径（LINUX 风格），并以 '/' 结尾
	参数：script_name, 脚本文件名
	返回值：当前脚本所在的路径名
	"""
	try:
		cur_path = os.path.split(os.path.realpath(script_name))[0] 		# 这句返回 当前脚本文件 所在路径（不含最后的文件名），路径分割符为 DOS 风格
	except:
		print('请传入脚本文件名 script_name = "脚本文件名"')
		return None

	if style in cf.DOS_STYLE_ARR:
		cur_path = cur_path + '\\'
	if style in cf.UNIX_STYLE_ARR:
		cur_path = cur_path.replace('\\','/') + '/' 				# 把 DOS 风格的路径分割符 \ 转换成Unix 风格的分割符 /，既然叫路径，那就要求以 '/'  结尾

	return cur_path








def change_path_style(xpath = None,style = 'DOS'):
	"""
	说明：改变路径风格
	参数：xpath 为待转换的路径, style 为目标风格，
	返回值：转换风格后的路径
	"""
	if xpath is None:
		print('没有输入路径')
		return None

	# -------------
	new_path = None 		# 预设返回路径值为 None

	if style in cf.DOS_STYLE_ARR:
		new_path = xpath.replace('/','\\')

	if style in cf.UNIX_STYLE_ARR:
		new_path = xpath.replace('\\','/')

	return new_path








 
 
def get_mydocument_path():
	"""
	说明：获取系统提供的“我的文档”路径
	参数：无
	返回值：“我的文档”所在路径
	"""
	mydocument_path = None
	dll = ctypes.windll.shell32
	buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH  + 1)
	if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
		mydocument_path =  buf.value + '\\'
		mydocument_path = change_path_style(xpath = mydocument_path,style = 'UNIX')

	return mydocument_path









def convert_df_type(df, xtype=float, column_arr=None):
	"""
	功能说明：对传入的 df ，根据传入的字段 column_arr （如果有的话，要是没有的话，则对 df 中所有字段转换），从 df 中找到对应的列，将其数据类型转换为 xtype 指定的类型；
		无法转换的数据值将用0填充，请调用者自己注意填 0 后返回去是否符合要求！  若不符合要求就不要调用本函数。
	参数：df, 待转换字段类型的 df; xtype, 目标数据类型；column_arr，需要转换哪些列
	返回值：转换数据类型后的 df
	"""	
	all_df = df.reset_index(drop=True)
	row_arr = list(all_df.index)

	if column_arr is None:
		column_arr = list(df.columns)
	# 先把所有数值型的列转成数值表示（原先是字符串形式的），以便参与数学计算
	#for k,col in enumerate(list(set(list(all_df.columns)) - set(['code','name','date','time']))):
	for col in column_arr:
		try:
			all_df[col] = all_df[col].astype(dtype=xtype)
		except:
			for row in row_arr:
				if is_number(all_df.ix[row,col]) == False:
					#all_df = all_df.drop(v,axis=0) 			# axis=0 表示行操作，这里是删除一行
					all_df.ix[row,col] = 0 					# 非数值单元域，全部填上 0
			try:
				all_df[col] = all_df[col].astype(dtype = xtype)
			except:	
				continue		
	all_df = all_df.reset_index(drop=True)

	return all_df














def get_percent(value1,value2):
	"""
	说明：计算 value2 相对于 value1 的增长幅度
	返回值：增长幅度
	"""
	func_name = get_current_function_name() + ': '
	if value1 == 0:
		print(func_name,'错误：请确保 value1 不为 0')
		return None

	xresult = (value2 - value1) / value1

	return xresult















def is_number(n):
	"""
	功能说明：测试输入的参数是否为数值型或数值型字符串，如是则返回 True，否则返回 False
	返回值：如是数字则返回 True，否则返回 False
	"""
	if n is None:
		return False
		
	try:
		float(n)
		return True
	except ValueError:
		return False








def is_weekday(xdate = None):
	"""
	功能说明：该函数用于判断传入的日期（若没传入，则判断今天）是否为周一到周五
	返回值：如果是周一到周五，则返回True，否则返回 False
	"""
	if xdate is None:
		xdate = get_today()

	# 若是字符串形的日期，则先转化成python格式日期
	if type(xdate) == str:
		year = get_year(xdate=xdate)
		month = get_month(xdate=xdate)
		day = get_day(xdate=xdate)

		xdate = datetime.date(year,month,day)

	n = xdate.weekday()
	if n >=0 and n <=4:
		return True
	else:
		return False








def is_weekend(xdate = None):
	"""
	功能说明：该函数用于判断传入的日期（若没传入，则判断今天）是否为双休日
	返回值：若是双休日，则返回True，否则返回 False
	"""
	if xdate is None:
		xdate = get_today()

	# 若是字符串形的日期，则先转化成python格式日期
	if type(xdate) == str:
		year = get_year(xdate=xdate)
		month = get_month(xdate=xdate)
		day = get_day(xdate=xdate)

		xdate = datetime.date(year,month,day)

	n = xdate.weekday()
	if n == 5 or n == 6:
		return True
	else:
		return False








def get_year(xdate):
	"""
	功能说明：对传入的日期取年份以数值型返回，
	参数：xdate，表示传入日期，必须是YYYY-mm-dd格式，或用 python 构造的日期型，
	返回值：整型年份

	"""
	xyear = None
	xdate = str(xdate)
	date_arr = xdate.split('-')
	if len(date_arr)>=1:
		try:
			xyear = int(date_arr[0])
		except:
			pass

	return xyear







def get_month(xdate):
	"""
	功能说明：对传入的日期取月份以数值型返回，
	参数：xdate，表示传入日期，必须是YYYY-mm-dd格式，或用 python 构造的日期型，
	返回值：整型月份

	"""
	xmonth = None
	xdate = str(xdate)
	date_arr = xdate.split('-')
	if len(date_arr)>=2:
		try:
			xmonth = int(date_arr[1])
		except:
			pass

	return xmonth












def get_day(xdate):
	"""
	功能说明：对传入的日期取日份以数值型返回，
	参数：xdate，表示传入日期，必须是YYYY-mm-dd格式，或用 python 构造的日期型，
	返回值：整型日

	"""
	xday = None
	xdate = str(xdate)
	date_arr = xdate.split('-')
	if len(date_arr)>=3:
		try:
			xday = int(date_arr[2])
		except:
			pass

	return xday













def get_today():
	"""
	功能说明：获取今天日期

	"""
	#today=time.strftime(date_format,time.localtime(time.time()))
	today = datetime.date.today()
	return today







def get_yesterday():
	"""
	功能说明：获取明天
	"""
	#xstep=datetime.timedelta(days=1)
	yesterday = get_today() - one_day_step
	return yesterday





def get_tomorrow():
	"""
	功能说明：获取明天
	"""
	#xstep=datetime.timedelta(days=1)
	tomorrow = get_today() + one_day_step
	return tomorrow









def get_time(xtime=None,time_format=cf.TIME_FORMAT):
	"""
	功能说明：根据传入的时间戳，取出时间返回
	参数：xtime: 是时间戳，如time.time() 返回的结果
	返回值：返回该时间戳指向的时间部分，以HH：MM：SS字符串格式返回。
	"""
	if xtime is None:
		xtime = time.time()
	current_time = time.strftime(time_format,time.localtime(xtime))

	return str(current_time)







def get_date(xtime=None):
	"""
	功能说明：根据传入的时间戳，取出日期返回
	参数：xtime: 是时间戳，如time.time() 返回的结果
	返回值：返回该时间戳指向的日期部分，以YYYY-MM-DD字符串格式返回。
	"""
	xdate = get_time(xtime=xtime, time_format=cf.DATE_FORMAT)

	return str(xdate)





def get_current_time(xtime=None,time_format=cf.DATE_TIME_FORMAT2):
	"""
	功能说明：根据传入的时间戳，取出时间返回
	参数：xtime: 是时间戳，如time.time() 返回的结果
	返回值：返回该时间戳指向的时间部分，以HH：MM：SS字符串格式返回。
	"""
	current_time = get_time(xtime=xtime,time_format=time_format)
	return current_time






def get_date_time(xtime=None,time_format=cf.DATE_TIME_FORMAT2):
	"""
	功能说明：根据传入的时间戳，取出日期时间返回
	参数：xtime: 是时间戳，如time.time() 返回的结果
	返回值：返回该时间戳指向的日期时间部分，以YYYY-MM-DD - HH：MM：SS字符串格式返回。
	"""
	current_time = get_time(xtime=xtime,time_format=time_format)
	return current_time







def get_hh(xtime):
	"""
	说明：根据传入的时间 ，返回小时部分（整型）
	参数：xtime，可以是格式为 hh:mm:ss 的时间字符串，也可以是时间戳
	返回值：整型 hh
	"""

	temp_time = xtime
	if type(xtime) != str:
		temp_time = get_time(xtime = xtime)

	time_str = None
	time_arr = temp_time.split(':')
	if len(time_arr) >= 1:
		time_str = int(time_arr[0])

	return time_str
	






def get_mm(xtime):
	"""
	说明：根据传入的时间 ，返回分钟部分（整型）
	参数：xtime，可以是格式为 hh:mm:ss 的时间字符串，也可以是时间戳
	返回值：整型 mm
	"""

	temp_time = xtime
	if type(xtime) != str:
		temp_time = get_time(xtime = xtime)

	time_str = None
	time_arr = temp_time.split(':')
	if len(time_arr) >= 2:
		time_str = int(time_arr[1])

	return time_str
	





def get_ss(xtime):
	"""
	说明：根据传入的时间 ，返回秒数部分（整型）
	参数：xtime，可以是格式为 hh:mm:ss 的时间字符串，也可以是时间戳
	返回值：整型 ss
	"""

	temp_time = xtime
	if type(xtime) != str:
		temp_time = get_time(xtime = xtime)


	time_str = None
	time_arr = temp_time.split(':')
	if len(time_arr) >= 3:
		time_str = int(time_arr[2])

	return time_str
	










def hms_to_minutes(xtime):
	"""
	功能说明：将 HH:MM:SS 转为分钟数
	参数：xtime，是字符串，格式必须为 hh:mm:ss
	返回值：分钟数
	"""	

	minutes = None

	hh=get_hh(xtime)
	mm=get_mm(xtime)
	if hh is not None and mm is not None:
		minutes=hh*60+mm
	
	return minutes









def hms_to_seconds(xtime):
	"""
	功能说明：将 HH:MM:SS 转为分秒数
	参数：xtime，是字符串，格式必须为 hh:mm:ss
	返回值：秒数
	"""		
	
	seconds = None

	hh=get_hh(xtime)
	mm=get_mm(xtime)
	ss=get_ss(xtime)

	if hh is not None and mm is not None and ss is not None:
		seconds=hh*60*60+mm*60+ss
	
	return seconds






def seconds_to_hms(seconds):
	"""
	说明：将秒数转为 hms 形式
	参数：seconds，秒数
	返回值：hms, 表示 HH:MM:SS 格式的时间
	"""

	hh = int(seconds / 3600)
	mm = int((seconds % 3600) / 60)
	ss = int((seconds % 3600) % 60)

	hh = char_fill(s = str(hh),bit = 2)
	mm = char_fill(s = str(mm),bit = 2)
	ss = char_fill(s = str(ss),bit = 2)

	hms = hh + ":" + mm + ":" + ss

	return hms









def timestamp_to_hms(timestamp):
	"""
	功能说明：将传入的时间戳转换为 HH:MM:SS 返回
	"""
	timestamp = int(timestamp)

	hhmmss = time.strftime(cf.TIME_FORMAT,time.localtime(timestamp))

	return hhmmss





	


def hms_to_timestamp(xtime,xdate=None):
	"""
	功能说明：将输入的日期时间转成时间戳戳（timestamp），
	参数：xdate 可以是字符串形式，也可以是python date 格式，如果没有输入，则取今天
	xtime 必须是 hh:mm:ss 形式
	返回值： 转换后的时间戳
	"""
	if xdate is None:
		xdate = get_today()
	t = str(xdate) + ' ' + str(xtime)
	t_arr = time.strptime(t,cf.DATE_TIME_FORMAT1)
	timestamp = time.mktime(t_arr) 				# 创建时间戳

	return timestamp










def timestamp_to_datetime(timestamp):
	"""
	功能说明：将时间戳转换为 YYYY-MM-DD HH:MM:SS 返回
	"""
	timestamp = int(timestamp)
	hhmmss = time.strftime(cf.DATE_TIME_FORMAT1,time.localtime(timestamp))

	return hhmmss









def get_timestamp(xtime,xdate=None):
	"""
	将输入的日期时间转成时间戳戳（timestamp），
	参数：xdate 可以是字符串形式，也可以是python date 格式，如果没有输入，则取今天
	xtime 必须是 hh:mm:ss 形式
	返回值： 转换后的时间戳
	"""

	timestamp = hms_to_timestamp(xtime = xtime,xdate = xdate)

	return timestamp








def get_lastfile(xpath):
	"""
	功能说明：从 xpath 目录中找出修改时间为最新的一个文件，并返回给主调函数

	"""
	lst = os.listdir(xpath)
	lst.sort(key=lambda fn: os.path.getmtime(xpath + fn) if not os.path.isdir(xpath + fn) else 0)
	d = datetime.datetime.fromtimestamp(os.path.getmtime(xpath + lst[-1]))
	lastfile = lst[-1]
	#time_end=time.mktime(d.timetuple())
	return lastfile








def ftp_open(host = None,port = None, username = None, password = None):
	"""
	功能说明：初始化 FTP 连接，返回指向 ftp 服务器的连接符。首先会尝试从传入的参数中读取信息，若没传入，则次选从用户的配置文件 user_config.ini 中读取FTP 服务器配置信息，若没有，则第3选择从 py 配置文件中读取，若还是没有，则返回 None

	"""
	if host is None or port is None or username is None or password is None:
		try:
			cfg = ConfigObj('user_config.ini')
		except:
			print('用户没有提供配置文件 user_config.ini，下面尝试从 common_config.py 中读取配置信息')
			try:
				host = cf.FTP_HOST
				port = cf.FTP_PORT
				username = cf.FTP_USERNAME
				password = cf.FTP_PASSWORD
			except:
				print('错误：common_config.py 配置文件中没有FTP服务器信息')	
				return None	
		else:		
			host = cfg['FTP_HOST']
			port = cfg['FTP_PORT']
			username = cfg['FTP_USERNAME']
			password = cfg['FTP_PASSWORD']	

	# --------------
	ftp = FTP()
	ftp.set_debuglevel(2)
	ftp.connect(host=host,port=port)
	ftp.login(username,password)

	return ftp










def ftp_close(ftp):
	"""
	功能说明：关闭FTP 连接
	"""

	ftp.set_debuglevel(0)
	ftp.quit()








def ftp_up(ftp,filename):
	"""
	功能说明：该函数用来上传文件到FTP 服务器，
	参数：ftp: 指向 FTP 服务器的连接符；filename: 待上传的文件，可以是windows 格式包含全路径的文件
	返回值：无
	"""
	#print(ftp.getwelcome())
	#ftp.cwd('xxx/www')
	file_handler = open(filename,'rb')
	ftp.storbinary('STOR %s' % (os.path.basename(filename)),file_handler)
	file_handler.close()

	print('FTP up OK.')










def ftp_down(ftp,filename):
	"""
	功能说明：该函数用来从 FTP 服务器下载文件，
	参数：ftp: 指向 FTP 服务器的连接符；filename: 待下载的文件，可以是windows 格式包含全路径的文件
	返回值：无
	"""	
	#print(ftp.getwelcome())
	#ftp.cwd('xxx/www')
	file_handler = open(filename,'wb')
	ftp.retrbinary('RETR %s' % (os.path.basename(filename)),file_handler)
	file_handler.close()

	print('FTP down OK.')









# 以下自定义函数的功能是将传入的 list 转成元组，包括只有一个元素的情形
def list_to_tuple(arr,quote_flag = False):
	"""
	功能说明：该函数用于将 list 转成 tuple，包括只有一个元素的情形
	参数：arr, 待转换的数组，quote_flag 表示是否给转换后的每个元组元素加上单引号，如果是 True 的话就加，加上去主要为了给数据库查询语句 select 用
	返回值：xtuple, 字符串形式的元组
	"""
	#判断只有一个元素时要单独处理，如果直接用 tuple()转，则会在末尾加一个逗号，导致不符合要求
	if len(arr) == 0:
		if quote_flag == True:
			xtuple="('')"

		if quote_flag == False:
			xtuple = "()"		

	if len(arr) == 1:	
		if quote_flag == True:
			xtuple="('" + str(arr[0]) + "')"

		if quote_flag == False:
			xtuple = "(" + str(arr[0]) + ")"

	if len(arr) > 1:
		if quote_flag == True:
			arr1 = [str(x) for x in arr]
			xtuple = tuple(arr1)

		if quote_flag == False:
			xtuple = tuple(arr)

	return str(xtuple)












def list2tuple(arr,quote_flag = False):
	"""
	功能说明：列表转成元组。实际上该函数与上述函数是一样的，是上述别名

	"""
	xtuple = list_to_tuple(arr=arr,quote_flag = quote_flag)
	return xtuple









def append_arr_to_df(df,arr):
	"""
	功能说明：把数组形式的 arr （必须是一维）追加到 DataFrame 形式的 df 行末尾，并将 df 返回到主调函数，要求 arr 的元素个数及含意与 df 的列数及含义相同

	"""
	columns = df.columns
	temp_df = pd.DataFrame(data=[arr], columns=columns)
	result_df = pd.concat([df,temp_df])

	return result_df









def xround(f,bit = 2):
	"""
	功能说明：由于 python3 的  round() 函数返回的结果与我们中国人的常规认识不同，所以自定义一个 xround() 函数 来代替系统提供的 round()
	参数：f: 要进行四舍五入的目标数值；bit: 表示保留几位小数
	返回值：四舍五入后的数值

	"""

	if(type(bit)!=type(1) or bit<0):
		print('xround(f,bit) 的 bit 参数必须为正整数。')
		return None

	xresult = None			# 预设返回值为 None

	"""
	num_part_arr = list(math.modf(f)) 			# math.modf(f) 的作用是对传入的浮点数 f 分成小数部分与整数部分形成 tuple 返回，这个 tuple 只有两个元素，第1个是小数部分，第2个是整数部分
	decimal_part = num_part_arr[0] 			# 获取小数部分
	integer_part = num_part_arr[1] 			# 获取整数部分
	"""
	alittle=0.0000001 		# 小幅修正值

	# 只有传入的数值的小数部分的长度小于上面的修正值时，才能继续下去，否则返回 None
	if bit <= 6:
		try:
			xresult=round(f + alittle, bit)
		except:
			print('xround 转换失败')
	else:
		print('错误：本函数最多支持 6 位精度。')

	#xresult=decimal.Decimal(str(f)).quantize(round(decimal.Decimal('1'),bit),rounding=decimal.ROUND_HALF_UP)
	return xresult



	





def time_spend(t1):
	"""
	功能说明：该函数计算t1 到 t2 之间的时间差，并输出信息，一般在程序末尾调用，输出程序执行花了多少时间
	参数：t1： 表示起始时间，需时间戳形式，即秒数
	返回值：无
	"""
	t2 = time.time()
	begin_time = get_time(time_format=cf.DATE_TIME_FORMAT2, xtime=t1)
	current_time = get_time(time_format=cf.DATE_TIME_FORMAT2, xtime=t2)
	#print('\n----------------------------')
	#print(get_today())
	print("Begin time:",begin_time)
	print("Current time:",current_time)
	#print('要判断上面代码执行花了多少时间，请查看上面最近两个 Current time 之间的时间差。')
	time_spend=seconds_to_hms(t2-t1)
	print("Time spend: ",time_spend,'\n')










def get_uuid():
	"""
	功能说明：该自定义函数用于获取一个 uuid()，并且以时间开头，方便需要时判断
	参数：无
	返回值：生成的十进制 uuid
	"""
	#return int(uuid.uuid1().hex,16) 	# 调用模块 uuid 的 uuid1()函数，生成一个 uuid ，并转成10进制数返回
	s = get_time(xtime=time.time(),time_format=cf.DATE_TIME_FORMAT3)
	t = str(int(uuid.uuid1().hex,16)) 	# 调用模块 uuid 的 uuid1()函数，生成一个 uuid ，并转成10进制数
	my_uuid = int(s+t)

	return my_uuid











def get_arr_add(arr1,arr2):
	"""
	功能说明：计算两个数组（相同维度）对应元素（必须数值型）的加法，把结果保留4位小数放在新的数组里返回
	"""
	result_arr = None

	if len(arr1) != len(arr2):
		print('错误！  %s 和 %s 维数不相等' % (str(arr1),str(arr2)))
		return None
	else:
		try:
			arr = list((np.array(arr1) + np.array(arr2)))
		except:
			print('错误！ 两数组对应元素相加出错，请确保数组元素为数值型。')
			return None
		else:
			#result_arr = [xround(x,4) for x in arr]
			result_arr = arr


	return result_arr	










def get_arr_sub(arr1,arr2):
	"""
	功能说明：计算两个数组（相同维度）对应元素（必须数值型）的减法(arr1 - arr2)，把结果保留4位小数放在新的数组里返回
	"""
	result_arr = None

	if len(arr1) != len(arr2):
		print('错误！  %s 和 %s 维数不相等' % (str(arr1),str(arr2)))
		return None
	else:
		try:
			arr = list((np.array(arr1) - np.array(arr2)))
		except:
			print('错误！ 两数组对应元素相加出错，请确保数组元素为数值型。')
			return None
		else:
			result_arr = arr
			#result_arr = [xround(x,4) for x in arr]

	return result_arr	











def get_arr_multiply(arr1,arr2):
	"""
	功能说明：计算两个数组（相同维度）对应元素（必须数值型）的乘积，把结果保留4位小数放在新的数组里返回
	"""
	result_arr = None

	if len(arr1) != len(arr2):
		print('错误！  %s 和 %s 维数不相等' % (str(arr1),str(arr2)))
		return None
	else:
		try:
			arr = list((np.array(arr1) * np.array(arr2)))
		except:
			print('错误！ 两数组对应元素相乘出错，请确保数组元素为数值型。')
			return None
		else:
			#result_arr = [xround(x,4) for x in arr]
			result_arr = arr

	return result_arr	










# 计算两个数组（相同维度）对应元素相除，把结果放在新的数组里
def get_arr_divide(arr1,arr2):
	"""
	功能说明：计算两个数组（相同维度）对应元素（必须数值型）的除法(arr1 / arr2)，把结果保留4位小数放在新的数组里返回
	"""
	result_arr = None

	if len(arr2) == 0 or len(arr1) != len(arr2):
		print('错误！ %s 为空，或 %s 和 %s 维数不相等' % (str(arr2),str(arr1),str(arr2)))
		return None
	else:
		try:
			arr = list((np.array(arr1) / np.array(arr2)))
		except:
			print('计算出错，可能 %s 数组中含有 0 值' % (str(arr2)))
			return None
		else:
			result_arr = [xround(x,4) for x in arr]

	return result_arr












def get_arr_ratio(arr1,arr2):
	"""
	功能说明：计算两个等长数组 arr1 和 arr2 的各对应元素差值后的幅度，即 (arr2 - arr1 ) / arr1 这个意思，具体要用到 numpy ，python 的 list 无法直接这样计算，必须先转成 numpy 的 array 才行。

	"""

	if len(arr1)==0 or len(arr1) != len(arr2):
		print('错误！ %s 为空，或 %s 和 %s 维数不相等' % (str(arr1),str(arr1),str(arr2)))
		return None
	else:
		try:
			arr = list((np.array(arr2) - np.array(arr1)) / np.array(arr1))
		except:
			print('计算出错，可能 %s 数组中含有 0 值' % (str(arr1)))
			return None
		else:
			result_arr = [xround(x,4) for x in arr]

	return result_arr










def is_valid_date(xdate):
	"""
	功能说明：判断是否日期
	参数：xdate: 表示传入的日期
	返回值：True: 表示传入的的确是日期；False: 表示传入的不是日期
	"""
	try:
		time.strptime(xdate,cf.DATE_FORMAT)
	except:
		return False
	else:
		return True












def strdate_to_pydate(xdate):
	"""
	功能说明：将字符串形的日期，转化成python datetime.date() 表示的日期
	参数：xdate: 字符串形式的日期
	返回值：py 形式的日期

	"""
	py_date='' 		# 如果传进来的日期是有效的，则转化成 datetime.date(y,m,d) 形式，并传递给变量 py_date

	if is_valid_date(xdate) == True:
		temp_arr=xdate.split('-')
		y=int(temp_arr[0]) 		# 获取并转化年
		m=int(temp_arr[1]) 		# 获取并转化月
		d=int(temp_arr[2]) 		# 获取并转化日
		py_date=datetime.date(y,m,d)

	return py_date













def strdate2pydate(xdate):
	"""
	功能说明：将字符串形的日期，转化成python datetime.date() 表示的日期。该函数和上面这个是一样的
	参数：xdate: 字符串形式的日期
	返回值：py 形式的日期

	"""
	py_date = strdate_to_pydate(xdate=xdate)
	return py_date









def df2list(df):
	"""
	功能说明：将 df 转成二维数组（包括列名）
	参数：df: pandas的 DataFrame数据
	返回值：二维数组

	"""
	col = list(df.columns)
	np_arr = df.as_matrix() 		# 把 df 转成 numpy 上的二维矩阵（即二维数组），二维数组中的每一行对应 df 中的一行

	d2_arr = [col] 					# 列名也保存下来
	for row in np_arr:
		d2_arr.append(list(row))

	return d2_arr		













def df2tuple(df):
	"""
	功能说明：将 df 转成二维元组（包括列名），即整个是元组，里面每一行也是元组
	参数：df: pandas的 DataFrame数据
	返回值：二维元组

	"""	

	d2_tpl = []

	d2_arr = df2list(df=df)
	for row in d2_arr:
		d2_tpl.append(tuple(row))
	d2_tpl = tuple(d2_tpl)

	return d2_tpl










def df2table(df = None,align = 'center',color_flag = False,fore_color1 = None,fore_color2 = None,bgcolor1 = "#F5F5DC",bgcolor2 = "#A7EEFB"):
	"""
	功能说明：将DF 转成 html 的 table 形式，并以字符串形式返回，主要是为了发电子邮件用
	参数：df:待转换的 pandas DataFrame数据；align:对齐方式；color_flag:要不要用前景色背景色装饰表格；
		fore_color1: 前景色1（即定体颜色）；fore_color2:前景色2（字体颜色）；bgcolor1: 表格行背景色1；bgcolor2:表格行背景色2
	返回值：字符串形式的 html table

	"""
	if df is None:
		print('错误！ 没有传入 DataFrame.')
		print(' df2table(df) 函数功能是将 pandas 的 DataFrame 转成 html 下的 <table>形式。用法: 参数 df 必须是 pandas 的 DataFrame 格式，不能为空。返回值是字符串形式的 html 下的 <table>，可独立作网页使用，也可拼接到其他 html 页面使用。')
		return ''

	d2_arr = df2list(df=df)

	# 预设表格行的前景色为黑色（即字体为黑色）
	fore_color = 'black'

	if fore_color1 is None:
		fore_color1 = fore_color

	if fore_color2 is None:
		fore_color2 = fore_color

	s = """
		<script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js"></script>
		<div style="text-align:%s;">
		<table width="500" border=1 style="word-break:norawp;">
		""" % (align)
		
	for k1,v1 in enumerate(d2_arr):
		# 设置前景色
		if color_flag == True:
			if k1 % 2 == 0:
				fore_color = fore_color1
			else:
				fore_color = fore_color2

		# 设置前景色
		s += '<tr style="color:%s;">' % (fore_color)
		for k2,v2 in enumerate(v1):
			s += '<td>' + str(v2) + '</td>'
		s += '</tr>'

	s += '</table></div>'

	# 设置背景色
	if color_flag == True:
		s += """ 
			<script>
			$(document).ready(function(){
			//隔行表色
			$("tr:even").css("background-color", "%s"); //为双数行表格设置背颜色素
			$("tr:odd").css("background-color", "%s");})
			</script>
			""" % (bgcolor1,bgcolor2)

	return s











def df2webpage(df = None,align = 'center',color_flag = False,fore_color1 = None,fore_color2 = None,bgcolor1 = "#F5F5DC",bgcolor2 = "#A7EEFB"):
	"""
	功能说明：将DF 转成 html page 形式，并以字符串形式返回，主要是为了发电子邮件用
	参数：df:待转换的 pandas DataFrame数据；align:对齐方式；color_flag:要不要用前景色背景色装饰表格；
		fore_color1: 前景色1（即定体颜色）；fore_color2:前景色2（字体颜色）；bgcolor1: 表格行背景色1；bgcolor2:表格行背景色2
	返回值：字符串形式的 html page

	"""

	s1 = """
		<html>
		<head>
		<style type="text/css">
		td
		{
			white-space: nowrap;
		}
		</style>
		<script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.min.js"></script>

		</head>
		<body>
		<div style="text-align:%s;"><table width="500" border=1 style="word-break:norawp;">
		""" % (align)
		
	html_table = df2table(df = df)

	s2 = '</body></html>'

	s = s1 + html_table + s2

	return s













def get_current_function_name():
	"""
	功能说明：当该函数被调用时，将返回上级函数（即主调函数）的函数名，所以一般用它放在函数内部来获取函数名 
	"""
	# return sys._getframe(0).f_code.co_name 		# 返回本函数名
	return sys._getframe(1).f_code.co_name 			# 返回上级函数名（或模块名）









# 
def start_app_by_pywinauto(app_path, retry_count = 5, wait_for_ready = 10):
	"""
	说明：调用 pywinauto 的 application.Application()功能来启动一个 app_path（一般是指 windows 下的 exe 程序），并返回指向这个 exe 程序的对象（句柄）到主调函数 
	参数：app_path, 要启动的应用程序全路径；retry_count: 启动失败的话最多尝试的次数；wait_for_ready，启动成功后最多等待的秒数，为了充分就绪
	返回值：若启动成功，则返回指向应用程序的句柄，否则返回 None
	"""
	func_name = get_current_function_name() + ': ' 		# 取得本函数名，即 start_app_by_pywinauto
	app = None
	xcount = 0
	while True:
		if xcount >= retry_count:
			print(func_name,' 已尝试 %d 次，均失败，不再尝试' % (retry_count))
			return None 			# 如果尝试 retry_count 次后，仍失败，则返回 None 到主调函数

		try:
			app = application.Application().connect(path = app_path) 			# 尝试连接佣金宝客户端
		except:
			try:
				app = application.Application().start(app_path) 		# 尝试启动佣金宝客户端
			except:
				#raise Exception('pywinauto 找不到程序 ' + app_path)
				xcount += 1
				continue
			else:
				#print(func_name + '%s 第一次启动。成功。' % (app_path))
				time.sleep(wait_for_ready) 	# 这个时间设长一点好，以便等待上述应用启动并准备就绪 ，8秒一般是够了，如果不够，则继续加大
				return app 		# 如果启动成功，则将 app 返回主调函数
		else:
			#print(func_name + '%s 已启动在那里，无需重复启动。' % (app_path))
			return app 			# 如果连接成功，则将 app 返回主调函数


	return app







# 
def goto_window(app,window_title,retry_count=5):
	"""
	功能说明：该函数用于返回到程序为 app对象（由 pywinauto 创建） 的 window_title 窗口上，并强烈清除该窗口下弹出的所有子孙窗口
	该函数没有返回值，调用后将带致指定 app对象（由 pywinauto 创建）下的 标题为 window_title 的窗口，并该窗口上方的杂七杂八各种弹出窗口都关掉，只留主窗口
	"""
	func_name = get_current_function_name() + ': '

	if app is None:
		print(func_name + '目标应用程 app 还没启动，请先调用 start_app_by_pywinauto() 启动目标程序。')
		return False

	# 根据窗口标题来清除其上所有窗口
	xcount = 0
	while True:
		if xcount >= retry_count:
			break
		title = app.top_window().texts()[0] 					# 取得程序顶层窗口（即最上面一层，top window）的标题
		#if title.find(window_title) == -1: 					# 在顶层窗口标题中搜索传入的标题字符串，如果没找到（即搜索结果是 －1），则把该窗口关了（注意：这种搜索方法要求 window_title 是普通字符串，而不能包含正则符号）
		if len(re.findall(window_title,title)) == 0: 			# 传入的参数 window_title 是包含目标题的正则表达式，相当于 pattern，用 re.findall() 在当前窗口的标题 xtitle 中去搜索正则模式的目标标题 window_title，如果没搜到，返回空的 list，表示当前窗口不是要找的窗口，关掉它。
			try:
				app.top_window().close()
			except:
				app.top_window().set_focus() 		# 把焦点落在顶层子窗口上
				app.top_window().close_alt_f4() 	# 用 ALT + F4 的方法关闭顶层窗口

			xcount += 1			
			time.sleep(0.1)						
		else:
			return True	

	return False









def char_fill(s, char='0', position='L', bit=6):
	"""
	功能说明：给传入的字符串 s 在 position （L代表左，即头部，R 代表右，即尾部）位置，用 字符（数字）c 填充，使之总长度为 bit 位
	参数：s: 待补齐前导字符或后导字符的字符串；bit: 补齐后的字符串位数; char: 要补什么字符；position: 补左边还是右边
	返回值：补齐后的字符串

	"""
	xresult = s
	if len(s)<bit:
		if position=='L' or position == 'l':
			xresult=char * (bit - len(s)) + s
		if position=='R' or position == 'r':
			xresult=s + char * (bit - len(s))

	return xresult











def attach_mail_image(msgRoot,fn_arr,mode='inline'):
	"""
	功能说明：msgRoot 是邮件基信息定义，一般由 email 包下的 Multipart() 函数的返回值得到，fn_arr 是个数组，每个元素是图片文件所在的全路径（含图片文件名），该函数的作用是把 fn_arr 数组中每条路径上的图片以邮件格式附加到 msgRoot，并把 msgRoot 带回主调函数，mode 表示图片内嵌到正文还是以附件形式
	首先要构造 Multipart，有3种参数类型，分别是 mixed, related, alternative. 有效范围依次递减，mixed 级别最大，可以发文件邮件，HTML邮件，内嵌图像，发附件等等 
	msgRoot = MIMEMultipart('mixed')  		# MIMEMultipart 表示允许附件在邮件正文件中直接显示

	"""
	#for k,img_file in enumerate(msg_dict['fn_arr']):
	for k,img_file in enumerate(fn_arr):
		img_pos = '<p><img src="cid:imgid%d" /></p>' % (k)
		
		msgRoot.attach(MIMEText(img_pos,'html','utf-8'))

		fp = open(img_file, 'rb')
		msgImage = MIMEImage(fp.read())
		fp.close()

		# 图片以内嵌方式发
		if mode == 'inline':
			msgImage.add_header('Content-ID', '<imgid%d>' % (k))
			#msgImage["Content-Disposition"] = 'inline; filename="imgid%s"' % (str(k))

		# 图片以附件方式发
		if mode == 'attachment':
			msgImage.add_header("Content-Disposition", "attachment", filename=os.path.split(img_file)[1])
			#msgImage["Content-Disposition"] = 'attachment; filename="%s"' % (os.path.split(img_file)[1])
			
		msgRoot.attach(msgImage)

	return msgRoot











def send_mail(msg_dict,smtp_server,smtp_port,sender_email,sender_password,receiver_arr,mode='inline'):
	"""
	功能说明：自定义发邮件函数，
	参数：msg_dict: 为邮件标题和内容构成的字典，只需包含content 和 subject 两项即可，有其他项数据也是可以的; 
		smtp_server: smtp 服务器IP或域名；smtp_port: smtp 服务器端口；
		sender_email: 邮件发送者的email 地址；sender_passwprd: 发送者的密码；
		receiver_arr: 邮件接收者email 构成的数组；mode 取值为 inline 或 attachment，表示对图片是内嵌方式发还是附件形式发
		注意，参数 receiver_arr 必须为数组形式，每个元素是字符串，内容是email 地址，如果有多个收件人，则在数组中以逗号分割; sender: 发件人的邮箱地址，字符串格式。
	返回值：无

	"""

	# 构造邮件信息 
	# 首先要构造 Multipart，有3种参数类型，分别是 mixed, related, alternative. 有效范围依次递减，mixed 级别最大，可以发文件邮件，HTML邮件，内嵌图像，发附件等等 
	msgRoot = MIMEMultipart('mixed')  		# MIMEMultipart 表示允许附件在邮件正文件中直接显示

	msgText = MIMEText(msg_dict['content'],'html','utf-8')			# 中文需参数‘utf-8’，单字节字符不需要 
	msgRoot.attach(msgText)

	msgRoot['Subject'] = msg_dict['subject']
	#msgRoot['From'] = formataddr(['wind',cf.MAIL_SENDER])
	#msgRoot['To'] = formataddr(['Friend',','.join(receiver_arr)])
	msgRoot['From'] = formataddr(['',sender_email])
	msgRoot['To'] = formataddr(['',','.join(receiver_arr)])

	# 如果存在图片要发送，则把图片附加到邮件上
	if 'fn_arr' in msg_dict.keys():
		msgRoot = attach_mail_image(msgRoot = msgRoot,fn_arr=msg_dict['fn_arr'],mode=mode)

	try:
		# 连接邮件服务器
		smtp = smtplib.SMTP_SSL(smtp_server,smtp_port)
		# 登录
		smtp.login(sender_email,sender_password)
		# 发送
		smtp.sendmail(sender_email, receiver_arr, msgRoot.as_string()) 
		print('Mail sent to %s successfully.' % (str(receiver_arr)))
		smtp.quit()  	
	except:
		print("邮件发送失败。")   










def handle_verify_code(code_image):
	"""
	功能说明：处理验证码，传入的参数 code_image 为待处理的验证码图片（不是图片文件，而是图片数据）
	参数：code_image: 待处理的验证码图片（不是图片文件，而是图片数据）
	返回值：文本验证码

	"""
	image_path = tempfile.mktemp()+'.jpg'
	code_image.capture_as_image().save(image_path)
	time.sleep(0.1)
	vcode = recognize_verify_code(image_path=image_path)
	"""
	if vcode is not None:
		xresult = ''.join(re.findall('[a-zA-Z0-9]+', vcode))
	"""

	return vcode










def recognize_verify_code(image_path):
	"""
	功能说明：识别验证码，其中具体调用下面的 recognize_code_by_tesseract() 来识别
	参数：image_path: 图片路径
	返回值：文本形式的验证码

	"""
	#vcode = None
	img = Image.open(image_path)
	vcode = recognize_code_by_pytesseract(img=img) 			# 调用 tesseract 识别

	return vcode









def recognize_code_by_pytesseract(img):
	"""
	功能说明：调用 pytesseract 识别验证码。 pytesseract 识别准确率不是很高，但也够用了
	参数：img:传入的的图片文件路径
	返回值：对图片识别后的文本验证码字符返回

	"""

	# 设置环境变量
	# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
	# tessdata_dir_config = '--tessdata-dir "D:/Program Files (x86)/Tesseract-OCR/tessdata"'

	try:
		vcode_str = pytesseract.image_to_string(img)
	except:
		print('pytesseract 未安装 或 tesseract-OCR 未安装，或已安装但传给 pytesseract 的参数有问题，验证码无法识别。')
		return None

	valid_chars_arr = re.findall('[0-9A-Za-z]', vcode_str, re.IGNORECASE)
	vcode = ''.join(valid_chars_arr)

	return vcode












def num2words(num):
	"""
	说明：转换数字为大写货币格式( format_word.__len__() - 3 + 2位小数 )
	num 支持 float, int, long, string
	"""
	format_word = ["分", "角", "元",
			   "拾","佰","仟","万",
			   "拾","佰","仟","亿",
			   "拾","佰","仟","万",
			   "拾","佰","仟","兆"]

	format_num = ["零","壹","贰","叁","肆","伍","陆","柒","捌","玖"]
	if type(num) == str:
		# - 如果是字符串,先尝试转换成float或int.
		if '.' in num:
			try:
				num = float(num)
			except:
				print('无法转换 %s' % (str(num)))
				return None
		else:
			try:
				num = int(num)
			except:
				print('无法转换 %s' % (str(num)))
				return None

	if type(num) == float:
		real_numbers = []
		for i in range(len(format_word) - 3, -3, -1):
			if num >= 10 ** i or i < 1:
				real_numbers.append(int(round(num/(10**i), 2)%10))

	elif isinstance(num, (int)):
		real_numbers = [int(i) for i in str(num) + '00']

	else:
		print('无法转换 %s' % (str(num)))
		return None

	zflag = 0                       #标记连续0次数，以删除万字，或适时插入零字
	start = len(real_numbers) - 3
	change_words = []
	for i in range(start, -3, -1):  #使i对应实际位数，负数为角分
		if 0 != real_numbers[start-i] or len(change_words) == 0:
			if zflag:
				change_words.append(format_num[0])
				zflag = 0
			change_words.append(format_num[real_numbers[start - i]])
			change_words.append(format_word[i+2])

		elif 0 == i or (0 == i%4 and zflag < 3):    #控制 万/元
			change_words.append(format_word[i+2])
			zflag = 0
		else:
			zflag += 1

	if change_words[-1] not in (format_word[0], format_word[1]):
		# - 最后两位非"角,分"则补"整"
		change_words.append("整")

	return ''.join(change_words)













def get_computer_name():
	"""
	说明：该函数用于获取电脑名称
	"""
	#获取本机电脑名
	#computer_name = socket.getfqdn(socket.gethostname())
	computer_name = socket.gethostname()

	return computer_name









def get_host_name():
	"""
	说明：该函数用于获取电脑名称
	"""
	return get_computer_name()












def get_host_ip():
	"""
	说明：该函数用于获取内网 ip 地址。注意：在多张网卡（包括虚拟网卡）的情形下，取到的内网 IP 可能不是想要的 IP。
		建议使用上面的 get_real_host_ip()
	"""	
	computer_name = get_computer_name()
	#获取本机ip
	private_ip = socket.gethostbyname(computer_name)

	return private_ip






def get_real_host_ip():
	"""
	说明：获取本机内网ip地址，这是获取到真实的内网IP，比下面的 get_host_ip() 准确，应优先使用本函数。
	返回值：本机内网 IP。
	"""
	private_ip = None
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		private_ip = s.getsockname()[0]
	finally:
		s.close()

	return private_ip







def get_private_ip():
	"""
	说明：该函数通过调用 get_real_host_ip() 获取本机内网IP并返回给上一层
	"""
	return get_real_host_ip()






def get_public_ip():
	"""
	说明：获取本机公网 ip
	"""
	url = urlopen("http://txt.go.sohu.com/ip/soip")
	text = url.read()
	ip_arr = re.findall('\d+\.\d+\.\d+\.\d+',str(text))

	public_ip = ip_arr[0]

	return public_ip








def get_mac_address(): 
	"""
	说明：获取本机 MAC 地址
	"""
	# 先获取本机 MAC 地址（字符串形式的十六进制）
	mac = uuid.UUID(int = uuid.getnode()).hex[-12:]  
	# 将上述 MAC 地址字符串中的字母全部转成大写
	mac = mac.upper() 		
	# 再用冒号切分后返回
	return ":".join([mac[e:e+2] for e in range(0,11,2)])









def get_hash_md5(s):
	"""
	说明：采用 md5 对传入的字符串 s 进行 hash 后返回
	"""
	xresult = hashlib.md5(str(s).encode('utf-8')).hexdigest()

	return xresult






def get_hash_sha512(s):
	"""
	说明：采用 sha512 对传入的字符串 s 进行 hash 后返回
	"""
	xresult = hashlib.sha512(str(s).encode('utf-8')).hexdigest()

	return xresult





def get_hash(s, hash_mode = 'sha512'):
	"""
	说明：根据传入的哈希算法对传入的字符串 s 进行哈希计算，并将结果返回
	"""
	if hash_mode == 'md5' or hash_mode == 'MD5':
		xresult = get_hash_md5(s = s)

	if hash_mode == 'sha512' or hash_mode == 'SHA512':
		xresult = get_hash_sha512(s = s)

	return xresult








def security_check(ip = None, mac = None):
	"""
	说明：本函数内获取本机 公网 ip ，然后做 hash 操作，然后和传入的 ip （应事先已 hash）比较，以判断程序是否运行在传入的 ip 电脑上，
		若不是，则返回 False 给上层代码，以决定是否退出，这样可防止程序被非法运行在指定 IP 以外的电脑上。
	"""
	public_ip = get_public_ip()
	hash_ip = get_hash(s = public_ip, hash_mode = 'sha512')

	if ip is None or hash_ip != ip:
		return False
	else:
		return True

	





def kill_app_by_name(app_name):
	"""
	功能说明：根据传入的进程名称 app_name 杀死该进程
	参数：app_name: 进程名称
	返回值：成功返回 True, 失败返回 False
	"""
	try:
		os.system('taskkill /F /IM %s /T' % (app_name))
	except:
		print('灭杀 %s 出错。' % (app_name))
		return False
	else:
		return True






def kill_app_by_process_id(process_id):
	"""
	功能说明：根据传入的进程ID process_id 杀死该进程
	参数：process_id: 进程 ID
	返回值：成功返回 True, 失败返回 False
	"""
	try:
		os.system('taskkill /F /PID %d /T' % (process_id))
	except:
		print('灭杀 %d 出错。' % (process_id))
		return False
	else:
		return True







def kill_app(app_name = None, process_id = None):
	"""
	说明：该任务函数的作用是用来杀掉应用程序
	参数：app_name 指向程序名；process_id 指向进程 id；这两个参数只需传入一个即可。若两个都传入，只优先使用 app_name，若采用 app_name关闭失败，则再采用 process_id 来关闭。
	返回值：灭杀应用程序或进程成功的话返回 True，否则返回 False
	"""

	if app_name is None and process_id is None:
		print('请传入程序文件名给形参 app_name 或传入进程id 给形参 process_id')
		return False

	if app_name is not None:
		xresult = kill_app_by_name(app_name=app_name)
		if xresult == True:
			return xresult

	if process_id is not None:
		xresult = kill_app_by_process_id(process_id=process_id)
		return xresult







def magic_square_odd(n = 3, arr = None):
	"""
	说明：该函数用来产生一个奇数阶方阵，使得横竖斜每条线加起来结果都相等
	参数：n ，必须是一个正的奇数，表示方阵的边长; 
		如果 n 没有输入, 则 arr 必须传入, arr 是一维 list, 元素个数必须是一个奇数的平方,函数表示对 arr 进行做幻方操作
	返回值：是符合要求的方阵（二维数组）
	"""

	if n is None and arr is None:
		print('错误! n 和 arr 必须输入其一')
		return None

	if arr is not None:
		n = int(math.sqrt(len(arr)))
		if pow(n,2) != len(arr):
			print('错误! 传入的 arr 长度(即元素个数)必须是奇数的平方才行!')
			return None
	else:			
		if n is None or n <=2 or n % 2 != 1:
			print('错误！请输一个正的奇数')
			return None
		else:
			arr = list(range(1,pow(n,2) + 1))

	result_arr = [[None for i in range(n)] for i in range(n)]

	i = 0
	j = 0
	
	#for num in range(1,pow(n,2) + 1):
	for num in arr:
		if num == arr[0]:
			i = 0
			j = int(n / 2)
		else:
			if i == 0 and j == n - 1:
				i = 1
			else:
				old_i = i
				old_j = j

				i = i - 1
				j = j + 1

				if i < 0:
					i = n - 1
				if j > n - 1:
					j = 0

				if result_arr[i][j] is not None:
					i = old_i + 1
					j = old_j

		result_arr[i][j] = num

	return result_arr









def magic_square_4k_df(n = 4):
	"""
	说明: 这是双偶阶(4k)幻方.
	算法参考: https://wenku.baidu.com/view/8f81130d168884868662d608.html
	"""

	if n is None or n <=2 or n % 4 != 0:
		print('错误！请输一个正的4的倍数')
		return None

	#d2_arr = [[None for i in range(n)] for i in range(n)]

	d2_arr = get_d2_arr(n = n) 		# 初始化一个 n X n 的二维数组
	df1 = pd.DataFrame(data = d2_arr)

	d2_arr = get_d2_arr(n = n,asscending = False) 		# 初始化一个 n X n 的倒排二维数组
	df2 = pd.DataFrame(data = d2_arr) 		# 生成 DataFrame

	k = int(n / 4)

	# 从倒排的 df (即 df2)中扣取 4 块覆盖到df1 中相应的位置
	# 第 1 块(上块)
	df1.ix[0:(k - 1),k:(3 * k - 1)] = df2.ix[0:(k - 1),k:(3 * k - 1)]

	# 第 2 块(下块)
	df1.ix[(n - k):(n - 1),k:(3 * k - 1)] = df2.ix[(n - k):(n - 1),k:(3 * k - 1)]

	# 第 3 块(左块)
	df1.ix[k:(n - k - 1),0:(k - 1)] = df2.ix[k:(n - k - 1),0:(k - 1)]

	# 第 4 块(右块)
	df1.ix[k:(n - k - 1),(n - k):(n - 1)] = df2.ix[k:(n - k - 1),(n - k):(n - 1)]

	return df1









def magic_square_4k(n = 4):

	if n is None or n <=2 or n % 4 != 0:
		print('错误！请输一个正的4的倍数')
		return None

	magic_df = magic_square_4k_df(n = n)
	magic_arr = df2list(df = magic_df) 		# 这个返回结果的第一项是列名, 后面是数据
	magic_arr = magic_arr[1:] 				# 去掉列名, 即让纯数据返回

	return magic_arr









def magic_square_4k_2_df(n = 6):
	"""
	说明: 这是单偶阶(4k + 2)幻方, 是3类幻方中最复杂的一种.
	算法参考: https://wenku.baidu.com/view/11402d1af7ec4afe04a1dfde.html
	"""

	if n is None or n <=2 or n % 4 != 2:
		print('错误！请输一个 4 * k + 2 的数(k 取正整数)')
		return None

	k = int(n / 4)

	m = int(n / 2)

	arr = list(range(1,pow(n,2) + 1))
	arr_len = len(arr)

	# 把边长为 4 * k + 2 的单偶阶方阵切成 4 块
	arr1 = arr[0:int(arr_len * 1/4)]
	arr2 = arr[int(arr_len * 1/4):int(arr_len * 2/4)]
	arr3 = arr[int(arr_len * 2/4):int(arr_len * 3/4)]
	arr4 = arr[int(arr_len * 3/4):int(arr_len * 4/4)]

	# 对 4 块中的每一块按奇数阶幻方处理
	df1 = magic_square_df(n = m,arr = arr1)
	df4 = magic_square_df(n = m,arr = arr2)
	df2 = magic_square_df(n = m,arr = arr3)
	df3 = magic_square_df(n = m,arr = arr4)

	# 开始交换
	#middle_line_num = int(m / 2)
	temp_df = df1.ix[0:k,0:k]
	temp_df = temp_df.copy(deep = True)
	df1.ix[0:k,0:k] = df3.ix[0:k,0:k]
	df3.ix[0:k,0:k] = temp_df

	temp_df = df1.ix[k,k:(k + k)]
	temp_df = temp_df.copy(deep = True)
	df1.ix[k,k:(k + k)] = df3.ix[k,k:(k + k)]
	df3.ix[k,k:(k + k)] = temp_df

	temp_df = df1.ix[(k + 1):(k + 1 + k),0:k]
	temp_df = temp_df.copy(deep = True)
	df1.ix[(k + 1):(k + 1 + k),0:k] = df3.ix[(k + 1):(k + 1 + k),0:k]
	df3.ix[(k + 1):(k + 1 + k),0:k] = temp_df

	if k > 1:
		temp_df = df2.ix[:,2:(k + 1)]
		temp_df = temp_df.copy(deep = True)
		df2.ix[:,2:(k + 1)] = df4.ix[:,2:(k + 1)]
		df4.ix[:,2:(k + 1)] = temp_df


	# 交换完成后进行合并
	left_df = pd.concat([df1,df3])
	right_df = pd.concat([df2,df4])

	magic_df = pd.concat([left_df,right_df],axis = 1)

	return magic_df











def magic_square_4k_2(n = 6):

	if n is None or n <= 2 or n % 4 != 2:
		print('错误！请输一个 4 * k + 2 的数(k 取正整数)')
		return None

	magic_df = magic_square_4k_2_df(n = n)
	magic_arr = df2list(df = magic_df)
	magic_arr = magic_arr[1:]

	return magic_arr







def magic_square(n = 3, arr = None):
	if n is None or n <=2:
		print('错误！请输一个大于 2 的正整数')
		return None	

	result_arr = None
	if n % 2 == 1:
		result_arr = magic_square_odd(n = n, arr = arr)

	if n % 4 == 0:
		result_arr = magic_square_4k(n = n)

	if n % 4 == 2:
		result_arr = magic_square_4k_2(n = n)

	return result_arr









def magic_square_df(n = 3, arr = None):
	"""

	"""
	if n is None or n <= 2 or type(n) != int:
		print('错误！请输一个大于 2 的正整数')
		return None	

	result_arr = magic_square(n = n,arr = arr)

	if result_arr is None:
		return None
	else:
		row_arr = ['r' + str(c) for c in range(1, n + 1)]
		col_arr = ['c' + str(c) for c in range(1, n + 1)]

		df = pd.DataFrame(data = result_arr,index = row_arr,columns = col_arr)
		
		return df











def get_d2_arr(n = 3,asscending = True):
	"""
	说明: 该函数用来产生一个 n X n 的二维数组, asscending = True 表示从小到大, 否则就从大到小
	"""
	if n is None or n <=0:
		print('错误!  请输入一个正整数')
		return None

	d2_arr = []

	d1_arr = list(range(1,pow(n,2) + 1))

	if asscending == False:
		d1_arr.reverse() 				# 翻转排列, 即从大到小

	i = 0 		# 首个元素的下标
	while True:		
		temp_arr = d1_arr[i:i + n]
		if len(temp_arr) > 0:
			d2_arr.append(temp_arr)
		else:
			break

		i += n

	return d2_arr










def get_randint_list(xbegin = 1,xend = 10):
	"""
	说明：调用该函数返回一个在xbegin（含） 和 xend（含）之间的随机整数 list
	"""
	arr = [x for x in range(xbegin,xend + 1)]
	random.shuffle(arr)

	return arr








def get_randint_arr(xbegin=1, xend=10):
	"""
	说明：调用该函数返回一个在xbegin（含） 和 xend（含）之间的随机整数 list
	"""
	arr = get_randint_list(xbegin=xbegin, xend=xend)
	return arr








def get_randint_df(n = 3):
	"""
	说明：调用该函数返回一个 n x n 的 元素为随机整数的 df
	"""
	arr=[]
	col_arr = []

	for i in range(n):
		temp_arr = get_randint_list(xend = n)
		arr.append(temp_arr)
		col_arr.append('col' + str(i))

	df = pd.DataFrame(data = arr,columns = col_arr)

	return df








def quick_sort(arr):    
	"""
	功能说明：对传入的数组进行快速排序，用到了递归
	参数：arr: 待排序的数组
	返回值：排序后的数组
	"""    
	if len(arr) >= 2:  # 递归入口及出口        
		mid = arr[len(arr)//2]  # 选取基准值，也可以选取第一个或最后一个元素        
		left, right = [], []  # 定义基准值左右两侧的列表        
		arr.remove(mid)  # 从原始数组中移除基准值        
		for num in arr:            
			if num >= mid:                
				right.append(num)            
			else:                
				left.append(num)        
		return quick_sort(left) + [mid] + quick_sort(right)    
	else:        
		return arr





		

def sort_df_column(df,column_arr):
	"""
	说明：对传入的 df ，将其各列按照 column_arr 中的列顺序排列后形成新的 df 返回。
		1. 若 df 中的列名与 column_arr 没有交集，则返回原 df;
		2. 若 df 中的列名与 column_arr 只有部分交集，则只对 df 中的交集字段按 column_arr 排序，然后放在新 df 的前面，df中有而column_arr 中没有的字段统统按原来顺序排在新生成的 df 后面；
		3. 若 df 中的列名是 column_arr 子集，则将 df 中的所有列完全按照 column_arr 中的顺序排列。
	参数：df ，待（按列）排序的 df; column_arr: 被参照排序的字段 list
	返回值：列排序后的 df
	"""
	position = 0
	for i,col in enumerate(column_arr):
		if col in list(df.columns):
			df.insert(position,col,df.pop(col))
			position += 1

	return df







def int2list(intnum):
	"""
	说明：对输入的一个整型数 intnum 以 list形式返回，list 中的每个元素都是整型，他们是原整型数的各个数位
	"""
	s = str(intnum) 			# 将输入整数转成字符串
	arr = list(s) 				# 将字符串转成一个个字符构成的列表
	result_arr = list(map(lambda x:int(x),arr)) 		# 将上述 arr 中的每个字符型元素 map 成一个整型元素，形成列表返回

	return result_arr








def get_window_handles():
	"""
	说明：该函数通过调用 win32gui.EnumWindows() 获取所有的窗口句柄以数组形式返回
	"""

	h_arr = []
	win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), h_arr) 		# 这个函数解释起来费劲，EnumWindows() 函数必须两个参数，前一个是用户定义的回调函数，这个回调函数的第一个参数 hWnd 位置是固定的，由系统返回的顶层窗口句柄，第2个参数 param 接受 EnumWindows() 的第 2 个参数作用它的参数。

	return h_arr






def get_window_attrs(window_handle):
	"""
	说明：根据传入的窗口句柄，返回该窗口的标题，类名等属性形成的 list 
	"""
	title = win32gui.GetWindowText(window_handle)
	class_name = win32gui.GetClassName(window_handle)

	attr_arr = [title,class_name]

	return attr_arr






def is_my_handle(window_handle,window_title):
	"""
	说明：该函数根据输入的窗口句柄 window_handle 判断该窗口是否包含窗口标题 window_title，如果是，返回 True, 否则返回 False
	"""

	attr_arr = get_window_attrs(window_handle = window_handle)
	title = attr_arr[0] 		#标题
	#if title.find(window_title) == -1: 				# 在返回的窗口标题中搜索是否包含想要找的标题字符串，若不是返回 -1。由于 window_title 是正则表达式，而 str.find() 不支持正则，所以用下面这句
	if len(re.findall(window_title, title)) == 0:
		return False
	else:
		return True






def get_prime_arr(n = 100):
	"""
	返回 n 以内的所有素数
	"""
	if n is None or n < 2:
		print('请输入一个大于 2 的正整数')
		return None

	prime_arr = [2]
	for num in range(3,n + 1):
		if num % 2 == 0:
			continue
		#sqrt_num = int(math.sqrt(num)) + 1
		prime_flag = True

		for prime in prime_arr:
			if num % prime == 0:
				prime_flag = False
				break

			#if prime > sqrt_num:
			if prime * prime > num:
				break

		if prime_flag == True:
			prime_arr.append(num)

	return prime_arr











def get_count_result(num1,num2,operator):
	"""
	说明: 对传入的 num1 和 num2,按操作符 operator 进行计算, 并把计算结果返回
	"""
	if (operator == '/' or operator =='%') and (num2 == 0 or str(num2) == '0'):
		#print('operator 为除法 / 或模 % 操作时，请确保 num2 不为 0')
		return None

	procedure_arr = [str(num1) + ' ' + operator + ' ' + str(num2)]
	expression = str(num1) + operator + str(num2)
	"""
	if operator == '/':
		result = Fraction(expression)
	else:
	"""
	result = eval(expression)

	return [procedure_arr,result]










def get_arr_rolling_count(num_arr, operator_arr=None, result=24,times_arr=[0]):
	"""
	说明: 对传入的操作数 num_arr( list 形式)和 操作符 operator_arr(list 形式),进行运算, 
		目标是计算出 result, 若找到,则返回解法步骤; 若无解, 则返回空.
	"""

	if len(num_arr) == 1 and abs(float(num_arr[0]) - result) <= 0.000001:
		return [[],True]

	if len(num_arr) == 1 and abs(float(num_arr[0]) - result) > 0.000001:
		return [[],False]

	# -------------
	same_value_arr = [] # 保存相同的值对

	plus_arr = [] 		# 加法数组里保存值对
	minus_arr = [] 		# 减法数组里保存值对
	multi_arr = [] 		# 剩法数组里保存值对
	divide_arr = [] 	# 除法数组里保存值对
	# =================
	# 若没有传入操作符 list, 则初始化操作符 list 为加减乘除
	if operator_arr is None:
		operator_arr = ['+','-','*','/'] 		

	# ----------------------------
	for i,num1 in enumerate(num_arr):
		for j,num2 in enumerate(num_arr):
			if j == i:
				continue

			# ----------
			# 遇两个相同数, 后续只要计算一遍即可, 无需交换后再做一遍计算, 以节约时间.
			if num1 == num2:
				if [num1,num2] in same_value_arr:
					continue
				else:
					same_value_arr.append([num1,num2]) 		# 保存值对
			# =============


			# 初始化 一个子数组
			sub_num_arr = []
			for k,v in enumerate(num_arr):
				if k != i and k != j:
					sub_num_arr.append(v)
			
			for operator in operator_arr:
				# ----------------------
				# 遇加法的, 两个数只计算一遍即可, 无需重复计算, 因为两数交换后加法结果是一样的.
				if operator == '+':
					if [num1,num2] in plus_arr or [num2,num1] in plus_arr:
						continue
					else:
						plus_arr.append([num1,num2]) 		# 保存值对

				# 遇减法的, 若相同的被减数和减数已经出现过的话, 则无需重复再做
				if operator == '-':
					if [num1,num2] in minus_arr:
						continue
					else:
						minus_arr.append([num1,num2])

				# 遇乘法的, 两个数只计算一遍即可, 无需重复计算, 因为两数交换后乘法结果是一样的.
				if operator == '*':
					if [num1,num2] in multi_arr or [num2,num1] in multi_arr:
						continue
					else:
						multi_arr.append([num1,num2]) 		# 保存值对

				# 遇除法的, 若相同的被除数和除数已经出现过的话, 则无需重复再做
				if operator == '/':
					if [num1,num2] in divide_arr:
						continue
					else:
						divide_arr.append([num1,num2])

				# ====================

				result_arr = get_count_result(num1 = num1,num2 = num2, operator = operator)
				times_arr[0] += 1 			# 这个是计数器, 上述 get_count_result() 每返回一次, 这里就 +1, 表示完成了一次计算
				#print(times_arr[0],end = ', ')
				if result_arr is None:
					continue
				else:
					[procedure_arr,middle_result] = result_arr
					#sub_num_arr.append(middle_result) 			# 这句也是正确的, 但为了优先使用中间结果, 所以用下面这一句, 即把中间计算结果插到第一个位置
					sub_num_arr.insert(0,middle_result) 		# 将计算返回的值插入到第一个位置, 即优先使用中间的计算结果, 这样符合人的思维

					# 把上述计算结果放回原队列, 并去掉已经用过的数, 形成一个新的数字队列, 然后递归调用本函数, 直至队列中只剩下一个数据就结束
					[sub_procedure_arr,flag] = get_arr_rolling_count(num_arr = sub_num_arr,operator_arr = operator_arr, result = result,times_arr = times_arr)

					if flag == True:
						sub_procedure_arr.insert(0,procedure_arr)
						return [sub_procedure_arr,flag]
					else:
						sub_num_arr.pop(0) 			# 如流程进入这里, 表明没有计算到目标值, 则去掉上面插进去的第一个值
						continue

	return [[],False]	
					










def get_expression(num_arr,operator_arr = None,result = 24,times_arr = [0]):
	"""
	说明: 根据传入的操作数 num_arr (list形式) 和操作符 operator_arr(list 形式), 每个数用且只用一次, 返回计算结果和 result 一致的表达式
	参数: num_arr: 操作数 list;  operator_arr: 操作符 list; result: 要求计算达到的结果
	返回值: 表达式
	"""


	if num_arr is None:
		print('错误! 请传入操作数 list')
		return None

	if 0 or '0' in num_arr:
		print('错误! 传入的操作数请不要包含 0, 避免计算过程中出现无穷大.')
		return None

	# 若没有传入操作符 list, 则初始化操作符 list 为加减乘除
	if operator_arr is None:
		operator_arr = ['+','-','*','/'] 		

		N = len(num_arr)
		M = len(operator_arr)
		total = pow(math.factorial(N),2) / N * pow(M, N - 1)

		print('数据个数 N = %d' % (N))
		print('运算符个数 M = %d' % (M))
		print('最多有 %d 个计算表达式' % (int(total)))

	[procedure_arr,flag] = get_arr_rolling_count(num_arr = num_arr,operator_arr = operator_arr,result = result,times_arr = times_arr)

	#print('耗费 %d / %d 步.' % (times_arr[0],total))

	return procedure_arr









