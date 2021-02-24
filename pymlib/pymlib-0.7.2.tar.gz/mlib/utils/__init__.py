# -*- coding: utf-8 -*-

import datetime, time, hashlib, glob, os, json
import smtplib
from email.mime.text import MIMEText
from .langconv import Converter

def get_beginday_timestamp(days=0, hours=8):
    """
    计算一天开的时间戳
    """
    # 计算当日凌晨的时间戳
    # 获取时间
    strtime = datetime.datetime.utcnow()+datetime.timedelta(days=-1+days, hours=hours)
    strtime = strtime.strftime('%Y-%m-%d {}:00:00'.format(24-hours))

    # 转换时间戳
    timeArray = time.strptime(strtime, "%Y-%m-%d %H:%M:%S")
    #转换成时间戳
    timestamp = time.mktime(timeArray)
    return timestamp

def sent163email(sender, pwd, receivers, title, content, host="smtp.163.com", port=465):
    body = content
    # 设置邮件正文，这里是支持HTML的
    msg = MIMEText(body, 'html') 
    # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = title
    # 设置邮件标题
    msg['from'] = sender  
    # 设置发送人
    msg['to'] = receivers
    # 设置接收人
    try:
        s = smtplib.SMTP_SSL(host, port)  
        # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
        s.login(sender, pwd)  
        # 登陆邮箱
        s.sendmail(sender, receivers, msg.as_string())
        # 发送邮件！
        return
    except smtplib.SMTPException as e:
        raise e
    except Exception as e:
        raise e

def get_file_md5(fname):
    m = hashlib.md5()   #创建md5对象
    with open(fname,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  #更新md5对象

    return m.hexdigest()    #返回md5对象

def work_all_dir(path):
    for file_path in glob.glob(os.path.join(path, "*")):
        if os.path.isfile(file_path):
            yield file_path
            continue
        gf = work_all_dir(file_path)
        for v in gf:
            yield v

# 转换繁体到简体
def cht_to_chs(line):
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line