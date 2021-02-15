#coding=utf-8
#返回值需要使用更新全局变量函数。返回值全局变量为 LASTRET
import sys
import requests
from . import graphic
_black=1
_red=2
_green=3
_yellow=4
_blue=5
_magenta=6
_cyan=7
_white=8
_grey=9
def __APIEXIT__():
    print('[N0ShellAPI]:Please run it in N0Shell.')
    sys.exit(0)
def consoleOut(identity,_content,leftColor='grey',rightColor='grey',colorStr='n0p'):
    #向N0Shell控制台输出的标准函数
    __APIEXIT__()
def debugOut(identity,_content,leftColor='grey',rightColor='grey',colorStr='n0p'):
    #在Debug模式下才会输出
    __APIEXIT__()
def echo(content,color=_white,**kv):
    #不询问身份的简单输出
    __APIEXIT__()
def argv(id):
    #获取N0Shell命令行参数
    __APIEXIT__()
def newArgv(offset):
    #向后偏移产生新的参数列表
    __APIEXIT__()
def realPath(_path,isFile=False):
    #将文件名或目录转为可访问路径
    __APIEXIT__()
def openFile(fileName):
    #打开文件 返回一个文件对象
    __APIEXIT__()
    file=open('example')
    return file
def request(_method,targetURL,paramsData='$n0p',postData='$n0p',_header='$n0p',_timeout=3):
    #发送请求 get post json paramsData postData _header均为dict类型
    __APIEXIT__()
    web=requests.get('example.cn')
    return web
def delPublicVar(publicVarName):
    #删除公共变量
    __APIEXIT__()
def publicVar(publicVarName,_value='$n0p'):
    #访问公开变量,_value置空将返回变量值，否则将赋值给变量。如果变量不存在则创建
    __APIEXIT__()
    return 'example'
def snipper(_tapList,_web):
    #精确的从web页面取出内容
    __APIEXIT__()
    return 'example'
def tapExtractor(tapName,targetStr,tapParamStr=''):
    #从页面中取出第一个html标签匹配结果
    __APIEXIT__()
    return 'example'