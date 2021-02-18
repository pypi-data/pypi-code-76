#! /usr/bin/python
# coding:utf-8

'''
发邮件,收邮件
1 发邮件
1.1 收件人
1.2 主题
1.3 正文
1.3.1 普通文本正文
1.3.2 图片正文
1.4 带附件
1.4.1 单附件
1.4.2 多附件
2 收邮件
'''

from 配置 import 邮件配置
import zmail

class 邮件:
    def __init__(self,邮件配置=邮件配置):
        self.__server = zmail.server(邮件配置['username'],邮件配置['password'])

    def 发(self,主题,收件人,正文,附件,抄送=''):
        '''
        收件人应当是列表格式 或者列表内嵌套元组格式 抄送也是如此
        正文是html格式
        '''
        mailConfig={
            'subject':主题,
            'content_html':正文,
            'attachments':附件
        }
        self.__server.send_mail(收件人,mailConfig,cc=抄送)
        print('已发送邮件:{subject}'.format(subject=主题))

    def 按主题下载附件(self,关键字,保存文件夹,第几封=1,找多少封后停止=20):
        '''
        按主题从新往旧
        找到第一封停止
        '''
        _mailCnt = self.__server.stat()[0]
        intervalCnt   = 1
        # 近n封邮件
        for i in range(_mailCnt,_mailCnt-找多少封后停止,-1):
            mail = self.__server.get_mail(i)
            print('邮件编号循环:%s' % i)
            if 关键字 in mail['headers']['Subject']:
                # 找到主题的第几封
                if intervalCnt == 第几封:
                    zmail.save_attachment(self.__server.get_mail(i),保存文件夹)
                    print('保存附件成功:{folder}'.format(folder=保存文件夹))        
                    break
                else:
                    intervalCnt += 1
    