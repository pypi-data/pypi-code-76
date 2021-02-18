'''
说明：这个配置文件是 for jxbase 这个包的

'''


# --------------
# DOS 风格
DOS_ARR = [
	'DOS',
	'dos'
	]


# WINDOWS 风格
WINDOWS_ARR = [
	'WINDOWS',
	'windows'
	]


# LINUX 风格
LINUX_ARR = [
	'LINUX',
	'linux'
	]



# UNIX 风格
UNIX_ARR = [
	'UNIX',
	'unix'
	]


DOS_STYLE_ARR = DOS_ARR + WINDOWS_ARR
UNIX_STYLE_ARR = UNIX_ARR + LINUX_ARR



# --------------------------
# 程序中要用到的几种时间格式
DATE_FORMAT='%Y-%m-%d'
TIME_FORMAT='%H:%M:%S'

DATE_TIME_FORMAT1 = DATE_FORMAT + ' ' + TIME_FORMAT
DATE_TIME_FORMAT2 = DATE_FORMAT + ' - ' + TIME_FORMAT
DATE_TIME_FORMAT3 = '%Y%m%d%H%M%S'




