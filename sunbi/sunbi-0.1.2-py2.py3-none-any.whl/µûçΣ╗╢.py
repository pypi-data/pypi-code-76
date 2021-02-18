#! /usr/bin/python
# coding:utf-8

'''
处理文件和文件夹, 以及路径相关
1 获取文件夹下所有或指定关键词文件
2 清空文件夹文件
'''

import os
from ftplib import FTP

class 文件:
    def __init__(self,文件夹):
        '''
        初始传入一个文件夹 方便后操作
        '''
        if not os.path.exists(文件夹):
            os.makedirs(文件夹)

        self.__folder = 文件夹
        self.__files  = os.listdir(self.__folder)

    def 获取文件夹文件(self,关键词='*'):
        '''
        关键词为* 获取其下所有文件
        关键词不为* 根据关键词过滤
        '''
        if 关键词=='*' :
            return [os.path.join(self.__folder,x) for x in self.__files]
        else:
            _filelist = []
            for file in self.__files:
                if 关键词 in file:
                    _filelist.append(os.path.join(self.__folder,file))
            return _filelist
    
    def 清空文件夹文件(self):
        for file in files:
            if os.path.isfile(os.path.join(self.__folder,file)):
                os.remove(file)
        print('已清空文件')
    
    def ftp复制文件(self,ftpip,目录):
        '''
        链接FTP服务器(免密)
        获取文件
        传输到本地文件夹(防止重复建议先清空本地)
        '''
        ftp = FTP()
        ftp.connect(ftpip)
        ftp.login()
        ftp.cwd(目录)
        _fileInfo = []
        ftp.retrlines('LIST',_fileInfo.append)
        self._files = [x.split()[-1] for x in _fileInfo]
        # 提前清空
        self.清空文件夹文件()
        for file in self._files:
            with open(file=os.path.join(self.__folder,file),mode='wb') as f:
                ftp.retrbinary('RETR %s' % file,f.write)
        print('FTP传输成功,本地文件保存地址:%s' % self.__folder)
    
    @property
    def 获取FTP文件列表(self):
        return self._files

