#! /usr/bin/python
# coding:utf-8

'''
由于主要基于pywin32模块,所以基本只能在Windows模块运行
'''

import os
import datetime
import time
from win32com.client import Dispatch
from PIL import ImageGrab

class 表格:
    def __init__(self,工作簿路径='',工作表序号=0,是否杀进程=True):
        '''
        工作簿路径如果为空则新建
        '''
        if 是否杀进程:
            os.system('taskkill /F /IM EXCEL.EXE')
        
        self.__app = Dispatch('excel.application')
        if 工作簿路径 == '':
            self.__wkb = self.__app.Workbooks.Add()
        else:
            self.__wkb = self.__app.Workbooks.open(工作簿路径)

        self.__sht = self.__app.Worksheets[工作表序号]

    @property 
    def 获取工作簿(self):
        return self.__wkb
    
    @property 
    def 获取工作表(self):
        return self.__sht

    def 刷新(self):
        self.__wkb.refreshAll()

    def 运行宏(self,宏名):
        self.__app.run(宏名)

    def 生成图片文件(self,对象名,文件夹,格式='jpg'):
        '''
        可以是文本(对象名) 也可以是数字(对象索引) 或者可循环的对象 对象内为文本/数字
        '''

        self.__folder = 文件夹
        if not os.path.exists(self.__folder)
            os.makedirs(self.__folder)
        
        self.__format = 格式

        self.__imgpaths = []
        if isinstance(对象,(list,tuple,set)):
            for obj in 对象:
                self.__imgpaths.append(self._saveImg(obj))
        else:
            self.__imgpaths.append(self._saveImg(对象名))
    
    @property 
    def 获取图片(self):
        return self.__imgpaths

    def _saveImg(self,对象名):
        '''
        无论是对象名还是索引号 方法都是一样的
        '''
        self.__sht.shapes(对象).copy() 
        img = ImageGrab.grabclipboard()
        self.__imgpath = os.path.join(self.__folder,'{filename}.{format}'.format(filename=对象名,format=self.__format))
        img.save(self.__imgpath)
        print('图片已保存:{path}'.format(self.__imgpath))
        time.sleep(1)
        return self.__imgpath

    def 关闭(self,是否保存=True,另存为路径='',是否关闭程序=False):
        '''
        另存为路径为空则不另存为 否则另存为
        '''
        if 是否保存:
            self.__wkb.Save()
        
        if 另存为路径 != '':
            self.__wkb.SaveAs(另存为路径)

        self.__wkb.Close(0)

        if 是否关闭程序:
            self.__app.quit()

    def 刷新保存关闭(self,休眠时间=10):
        self.刷新()
        time.sleep(休眠时间)
        self.关闭()
    
    def 刷新另存为关闭(self,另存为路径,休眠时间=10):
        self.刷新()
        time.sleep(休眠时间)
        self.关闭(另存为路径)
    
    def 运行宏保存关闭(self,宏名,休眠时间=10):
        self.运行宏(宏名)
        time.sleep(休眠时间)
        self.关闭()
    
    def 运行宏另存为关闭(self,宏名,另存为路径,休眠时间=10):
        self.运行宏(宏名)
        time.sleep(休眠时间)
        self.关闭(另存为路径=另存为路径)
    
    def 刷新运行宏关闭(self,宏名,休眠时间=10):
        self.刷新()
        time.sleep(休眠时间)
        self.运行宏(宏名)
        time.sleep(休眠时间)
        self.关闭()

    def 刷新运行宏关闭(self,宏名,另存为路径,休眠时间=10):
        self.刷新()
        time.sleep(休眠时间)
        self.运行宏(宏名)
        time.sleep(休眠时间)
        self.关闭(另存为路径=另存为路径)
    
    def 刷新存图关闭(self,图片对象,文件夹,格式='jpg',休眠时间=10):
        self.刷新()
        time.sleep(休眠时间)
        self.生成图片文件(对象名=图片对象,文件夹=文件夹,格式=格式)
        self.关闭()
        return self.获取图片

    def 嵌套对象导出为工作簿(self,文件路径,嵌套对象,标题=[]):
        '''
        常见从数据库导出到Excel
        '''
        if len(标题) > 0:
            for y in range(len(标题)):
                try:
                    self.__sht.cells(1,y+1).value = str(标题[x])
                except Exception as e:
                    print(e)
                    self.__sht.cells(1,y+1).value = ''
            sRow += 1
        
        for x in range(len(嵌套对象)):
            for y in range(len(x)):
                try:
                    self.__sht.cells(x+2,y+1).value = 嵌套对象[x][y]
                except Exception as e:
                    print(e)
                    self.__sht.cells(x+2,y+1).value = ''
        self.关闭(另存为路径=文件路径)
        print('已保存为{file}'.format(file=文件路径))



