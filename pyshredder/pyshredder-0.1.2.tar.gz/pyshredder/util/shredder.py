#!/usr/bin/env python3
# coding=utf-8
# ----------------------------------------------------------------------------------------------------
# 类 shredder
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2021-02-24 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | file(self, ...)              | 删除文件
# ----------------------------------------------------------------------------------------------------
import os
import time
import base64
from ztools import hash
from ztools import AnsiStyle, AnsiFore, AnsiBack, tprint
from ..core.eraser import eraser
# ----------------------------------------------------------------------------------------------------
class shredder(eraser, hash, tprint):
    """
    shredder类提供了对文件、文件夹的彻底删除操作，
    并且具有4中模式可选：
        快速模式（'fast'）
        标准模式（'standard'）
        安全模式（'safe'）
        毁灭模式（'destroy'）
    """
    def __init__(self, mode = 'standard'):
        eraser.__init__(self)
        tprint.__init__(self)
        self.__version = "0.1"
        self.__mode = mode
# ----------------------------------------------------------------------------------------------------
    def eraser(self, path, loop = 1, check = False):
        """
        文件擦除：
        输入参数：path 文件路径， loop 循环次数， check 是否校验
        返回参数：True 成功， False 失败
        说明：该方法通过对文件先填充无效数据的方式达到擦除文件数据的目的。
            快速模式（'fast'）下，仅使用随机数擦除1次。
            标准模式（'standard'）下，分别使用0、1、随机数各擦除1次。
            安全模式（'safe'）下，分别使用0、1、随机数各擦除3次。
            毁灭模式（'destroy'）下，使用随机数各擦除10次。
        """
        # 判断文件是否存在
        if not os.path.exists(path):
            return False
        if check:
            hash_md5_old = self.md5(filename = path)
            hash_sha1_old = self.sha1(filename = path)
        if loop < 1:
            loop = 1
        for cnt in range(loop):
            if self.__mode == 'fast':
                # 快速模式（'fast'）
                if not self.random_block(path):
                    return False
            elif self.__mode == 'safe':
                # 安全模式（'safe'）
                for idx in range(3):
                    if not self.fill(path, [0]):
                        return False
                    if not self.fill(path, [1]):
                        return False
                    if not self.random_block(path):
                        return False
            elif self.__mode == 'destroy':
                # 毁灭模式（'destroy'）
                for idx in range(10):
                    if not self.random_block(path):
                        return False
            else:
                # 标准模式（'standard'）
                if not self.fill(path, [0]):
                    return False
                if not self.fill(path, [1]):
                    return False
                if not self.random_block(path):
                    return False
        if check:
            hash_md5_new = self.md5(filename = path)
            hash_sha1_new = self.sha1(filename = path)
            # print('MD5:', hash_md5_old, '->', hash_md5_new)
            self.color('MD5:')
            self.color(hash_md5_old, AnsiFore.red)
            self.color('->')
            self.color(hash_md5_new, AnsiFore.green)
            self.flush()
            # print('SHA1:', hash_sha1_old, '->', hash_sha1_new)
            self.color('SHA1:')
            self.color(hash_sha1_old, AnsiFore.red)
            self.color('->')
            self.color(hash_sha1_new, AnsiFore.green)
            self.flush()
        return True
# ----------------------------------------------------------------------------------------------------
    def rename(self, path):
        """
        文件擦除：
        输入参数：path 文件路径
        返回参数：True 成功， False 失败
        说明：该方法通过对文件重命名达到清除文件原有属性信息的目的。
            快速模式（'fast'）下，仅重命名3次。
            标准模式（'standard'）下，重命名5次。
            安全模式（'safe'）下，重命名10次。
            毁灭模式（'destroy'）下，重命名100次。
        """
        # 标准模式（'standard'）
        loop = 5
        if self.__mode == 'fast':
            # 快速模式（'fast'）
            loop = 3
        elif self.__mode == 'safe':
            # 安全模式（'safe'）
            loop = 10
        elif self.__mode == 'destroy':
            # 毁灭模式（'destroy'）
            loop = 100
        try:
            srcFile = path
            dstFile = path
            folder = os.path.dirname(path)
            name = os.path.basename(path)
            for cnt in range(loop):
                # 判断文件是否存在
                if not os.path.exists(srcFile):
                    return False
                # 判断文件是否存在
                while os.path.exists(dstFile):
                    namebytes = (str(int(time.time()*100))).encode("utf-8")
                    name = base64.b64encode(namebytes).decode("utf-8")[:16]
                    dstFile = folder + '\\' + name
                # 重命名文件
                os.rename(srcFile,dstFile)
                srcFile = dstFile
                # time.sleep(1)
            # 判断文件是否存在
            if os.path.exists(path):
                return False
            # 重命名回原文件名
            os.rename(srcFile,path)
        except Exception as e:
            print(e)
            os.rename(srcFile,path)
            return False
        return True
# ----------------------------------------------------------------------------------------------------
    def file(self, path, check = False, delete = True):
        """
        文件删除：
        输入参数：path 文件路径， check 是否校验， delete 是否删除
        返回参数：True 成功， False 失败
        说明：该方法通过对文件先覆写数据、再重命名、最后删除系列操作确保文件数据被可靠删除。
        """
        # 判断文件是否存在
        if not os.path.exists(path):
            return False
        if not self.eraser(path, check = check):
            return False
        if not self.rename(path):
            return False
        if delete:
            if not os.path.isfile(path):
                return True
            try:
                os.remove(path)
            except Exception as e:
                print(e)
                return False
            return (not os.path.isfile(path))
        return True
# ----------------------------------------------------------------------------------------------------
