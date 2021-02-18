#! /usr/bin/python
# coding:utf-8

'''
企业微信机器人及API
1 企业微信机器人
2 企业微信API
'''

from 配置 import 企业微信配置,企业微信机器人
from hashlib import md5
from base64 import b64encode
from requests_toolbelt import MultipartEncoder
import os
import json 
import requests

class 企业微信机器人:
    def _init__(self,口令=企业微信机器人['默认'])
        '''
        请设置一个默认的webhook
        '''
        self.__url = 口令

    def 发文本(self,文本):
        '''
        文本参数可以是
        1 循环型(列表,元组,集合)
        2 文本
        3 其他会被文本化
        '''
        self.__text = 文本
        if isinstance(文本,(list,tuple,set)):
            for text in 文本:
                self._sendText(text)
        elif isinstance(文本,str):
            self._sendText(文本)
        else:
            text = str(文本)
            self._sendText(text)
        print('文本已发送')

    def _sendText(self,text):
        self.__data = json.dumps({
            'msgtype':'text',
            'text'   :{
                'contect':text
            }
        })
        requests.post(self.__url,self.__data)  

    def 发Markdown(self,Markdown):
        self.__Markdown = Markdown
        if isinstance(Markdown,(list,tuple,set)):
            for md in Markdown:
                self._sendMarkdown(md)
        else:
            self._sendMarkdown(Markdown)
        print('Markdown已发送')

    def _sendMarkdown(self,mkd):
        self.__data = json.dumps({
            'msgtype':'markdown',
            'markdown':{
                'content':mkd
                }
        })
        requests.post(self.__url,self.__data) 

    def 发图片(self,图片):
        '''
        参数为图片的完整路径 或者完整路径的集合类元素
        '''
        self.__image = 图片
        if isinstance(图片,(list,tuple,set)):
            for img in 图片:
                self._sendImage(img)
            print('图片集已发送')
        elif isinstance(图片,str):
            self._sendImage(图片)
            print('图片已发送')
        else:
            print('请传入完整的图片路径')

    def _sendImage(self,imgPath):
        # md5编码
        # base64编码
        with open(imgPath,'rb') as f:
            m = md5()
            m.update(f.read())
            md = m.hexdigest()
            base = str(b64encode(f.read()),'utf-8')
        
        self.__data = json.dumps({
            'msgtype':'image',
            'image':{
                'base64':base,
                'md5':md
            }
        })
        post(self._url,self.__data)

    def 发图文(self,图文):
        '''
        参数为 列表/元组/集合 内嵌字典的形式 或者直接为字典
        参照微信官方说明看看key值有啥
        自带批量发送 故不用建子类
        '''
        self.__图文 = 图文
        self.__data = json.dumps({
            "msgtype": "news",
            "news": {
            "articles" : 图文
            }
        })
        requests.post(self._url,self.__data)
        print('图文已发送')

    def 发文件(self,文件):
        '''
        文件列表或者单个文件完整路径
        '''
        self.__file = 文件
        if isinstance(文件,(list,tuple,set)):
            for file in 文件:
                self._sendFile(file)
            print('文件集已发送')
        elif isinstance(文件,str):
            self._sendFile(文件)
            print('文件已发送')
        else:
            print('请传入完整的文件路径')

    def _sendFile(self,file,key=self.__url[-36:]):
        with open(file, 'rb') as f:
            files = {'uploadFile':(os.path.basename(file),f)}
        data = MultipartEncoder(files)
        headers = {
            'Content-Type':data.content_type,
            'Content-Disposition':'form-data;name="media";filename="test.xlsx";filelength=6'
        }
        __urlUpload = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=%s&type=file' % key
        response = requests.post(__urlUpload,headers=headers,data=data)
        mid = json.loads(response.text)['media_id']
        
        self.__data = json.dumps({
            'msgtype':'file',
            'file':{
                'media_id':mid
            }
        })
        requests.post(self._url,self.__data)
            
        
class 企业微信API:
    def __init__(self,企业ID=企业微信配置['企业ID'],客户secret=企业微信配置['客户secret'],通讯录secret=企业微信配置['通讯录secret']):
        # 使用字典传输可能会是一个很大的坑!
        self.__corpid    = 企业ID
        self.__secretOrg = 通讯录secret
        self.__secretCus = 客户secret

        # 内部token
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}'.format(corpid=self.__corpid,secret=self.__secretOrg)
        jsn = json.loads(requests.get(url).text)
        # print(jsn)
        if jsn.get('errcode') == 0:
            print('获取内部access_token成功')
            self.__tokenOrg = jsn.get('access_token')
        else:
            print('获取内部access_token失败')
            self.__tokenOrg = None

        # 外部token
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}'.format(corpid=self.__corpid,secret=self.__secretCus)
        jsn = json.loads(requests.get(url).text)
        # print(jsn)
        if jsn.get('errcode') == 0:
            print('获取外部access_token成功')
            self.__tokenCus = jsn.get('access_token')
        else:
            print('获取外部access_token失败')
            self.__tokenCus = None

    @property 
    def 获取内部口令(self):
        return self.__tokenOrg
    
    @property 
    def 获取外部口令(self):
        return self.__tokenCus

    def 生成部门(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token={token}&id='.format(token=self.__tokenOrg)
        jsn = json.loads(requests.get(url).text)
        if jsn.get('errcode') == 0:
            print('获取部门列表成功')
            self.__deps = jsn.get('department')
        else:
            print('获取部门列表失败')

    @property 
    def 获取部门(self):
        return self.__deps

    def 生成部门成员(self,部门ID,是否递归=0):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token={token}&department_id={depid}&fetch_child={isall}'.format(token=self.__tokenOrg,depid=部门ID,isall=是否递归)
        jsn = json.loads(requests.get(url).text)
        if jsn.get('errcode') == 0:
            print('获取部门[%s]成员成功' % depid)
            self.__depUser = jsn['userlist']
        else:
            print('获取部门[%s]成员失败' % depid)

    @property 
    def 获取部门成员(self):
        return self.__depUser

    def 生成成员客户(self,成员ID):
        '''输入单个userid,返回客户id列表'''
        url = 'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/list?access_token={token}&userid={userid}'.format(token=self.__tokenCus,userid=成员ID)
        jsn = json.loads(requests.get(url).text)
        # print(jsn)
        if jsn.get('errcode') == 0:
            print('获取[%s]客户列表成功' % userid)
            self.__userCustomer = jsn.get('external_userid')
        else:
            # 没有外部客户的似乎会报错
            print('获取[%s]客户列表失败' % userid)

    @property 
    def 获取成员客户(self):
        return self.__userCustomer

    def 生成客户详情(self,外部客户ID):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get?access_token={token}&external_userid={external_userid}'.format(token=self.__tokenCus,external_userid=外部客户ID)
        jsn = json.loads(requests.get(url).text)
        if jsn.get('errcode') == 0:
            print('获取客户详情成功')
            self.__customer = jsn.get('external_contact')
        else:
            print('获取客户详情失败')
    
    @property 
    def 获取客户详情(self):
        return self.__customer

    def 生成客户群(self,游标=''):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/list?access_token={token}'.format(token=self.__tokenCus)
        data = json.dumps({
            'cursor':游标,
            'limit':1000
        })
        jsn = json.loads(requests.post(url,data).text)
        if jsn.get('errcode') == 0:
            print('获取客户群成功')
            self.__group = jsn['group_chat_list']
        else:
            print('获取客户群失败')

    @property 
    def 获取客户群(self):
        return self.__group 

    def 生成客户群详情(self,客户群ID):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/get?access_token={token}'.format(token=self.__tokenCus)
        data = json.dumps({
            'chat_id':客户群ID
        })
        jsn = json.loads(requests.post(url,data).text)
        if jsn.get('errcode') == 0:
            print('获取客户群详情成功')
            self.__groupDetail = jsn['group_chat']
        else:
            print('获取客户群详情失败')

    @property 
    def 获取客户群详情(self):
        return self.__groupDetail
