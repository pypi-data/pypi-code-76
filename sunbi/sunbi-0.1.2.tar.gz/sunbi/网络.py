#! /usr/bin/python
# coding:utf-8

'''
网络传输,数据同步,API,爬虫
1 requests get/post
2 selenium 由于定制化过高 这里只做演示
'''

import requests 
import json
import os
import time

class 网络:
    def __init__(self,地址,方式,数据包):
        if 方式.lower() == 'get':
            self.__result = json.loads(requests.get(地址).text)
        else:
            self.__result = json.loads(requests.post(地址,json.dumps(数据包)).text)
    
    @property 
    def 返回结果(self):
        return self.__result

class 模拟:
    def __init__(self,下载文件夹,驱动路径=''):
        '''
        初始传入一个下载文件夹路径 一个驱动路径(不传入则需手动放入%python%\scripts)
        初始化就会打开浏览器
        请确认ChromeDirver和Chrome的版本适配
        '''
        from selenium import webdriver 
        if not os.path.exists(下载文件夹):
            os.makedirs(下载文件夹)

        if 驱动路径 != '' and not os.path.exists(驱动路径):
            print('驱动不存在 无法运行')
            exit()

        options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_settings.popups':0,
            'download.default_directory':下载文件夹,
            'excludeSwitches':'enable-logging'
        }
        options.add_experimental_option('prefs',prefs)
        # options.add_argument('--headless')  # 不显示界面运行
        if 驱动路径=='':
            self.__driver = webdriver.Chrome(chrome_options=options)
        else:
            self.__driver = webdriver.Chrome(chrome_options=options,executable_path=驱动路径)

    @property 
    def 获取浏览器对象(self):
        return self.__driver

    def 登录鹰眼(self,鹰眼地址,手机号,二次密码=''):
        '''
        1 需要手动输入验证码
        2 xpath可能会变动 这是20210218当时的xpath
        '''
        self.__driver.get(鹰眼地址)
        self.__driver.find_element_by_xpath('//*[@id="fm1"]/div[2]/div[1]').click()                  # 换到验证码页面
        self.__driver.find_element_by_xpath('//*[@id="username"]').send_keys(手机号)                  # 填入用户名
        self.__driver.find_element_by_xpath('//*[@id="fm1"]/div[1]/div[5]/div[1]/button').click()    # 发送验证码
        time.sleep(1)
        self.__driver.switch_to_alert().accept()    # 关闭提示
        code = input('请输入验证码:')   # 这里需要手动输入验证码
        self.__driver.find_element_by_xpath('//*[@id="password"]').send_keys(code)                  # 填验证码
        self.__driver.find_element_by_xpath('//*[@id="fm1"]/div[1]/div[8]/button').click()          # 点击登录
        try:
            self.__driver.find_element_by_xpath('//*[@id="password"]').send_keys(二次密码)           # 二次密码输入
            self.__driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/input[7]').click()
        except:
            print('未出现二次密码')
        finally:
            self.__driver.maximize_window() # 窗口最大化

    def 关闭浏览器(self):
        self.__driver.close()
        self.__driver.quit()