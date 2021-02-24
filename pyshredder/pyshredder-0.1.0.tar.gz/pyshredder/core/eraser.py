#!/usr/bin/env python3
# coding=utf-8
# ----------------------------------------------------------------------------------------------------
# 类 eraser
# ----------------------------------------------------------------------------------------------------
# 变更履历：
# 2021-02-24 | Zou Mingzhe   | Ver0.1  | 初始版本
# ----------------------------------------------------------------------------------------------------
# MAP：
# 已测试 | fill(self, ...)              | 填充擦除
# 已测试 | random(self, ...)            | 随机擦除（字节）
# 未开发 | random_block(self, ...)      | 随机擦除（块）
# ----------------------------------------------------------------------------------------------------
import os
import random
# ----------------------------------------------------------------------------------------------------
class eraser:
    """
    eraser类提供了对文件的擦除操作。
    """
    def __init__(self):
        self.__version = "0.1"
        self.__align = 4096
# ----------------------------------------------------------------------------------------------------
    def fill(self, path, data = [0]):
        """
        填充擦除（字节）：
        输入参数：path 文件路径， data 填充数据
        返回参数：True 成功， False 失败
        说明：该方法通过对文件填充数据来擦除文件。
        填充数据会被字节对齐至self.__align值，
        若填充数据不足self.__align则循环生成，
        覆写后文件大小为self.__align值的整数倍。
        """
        # 判断文件是否存在
        if not os.path.exists(path):
            return False
        # 生成填充数据
        while len(data) < self.__align:
            data = data * 2
        byte = bytes(data[:self.__align])
        # print("fill data len:", len(byte), len(data))
        # 读取文件大小
        size = os.path.getsize(path)
        # 对文件用填空数据覆写
        with open(path, "wb+") as f:
            length = 0
            while length < size:
                length = length + self.__align
                f.write(byte)
                f.flush()
        return True
# ----------------------------------------------------------------------------------------------------
    def random(self, path):
        """
        随机擦除（字节）：
        输入参数：path 文件路径
        返回参数：True 成功， False 失败
        说明：该方法通过对文件覆写随机数（字节）来擦除文件。
        由于每个字节均调用一次随机数生成，速度较慢；
        覆写后文件大小不改变，并且所有数据完全随机。
        """
        # 判断文件是否存在
        if not os.path.exists(path):
            return False
        # 读取文件大小
        size = os.path.getsize(path)
        # 对文件用二进制随机数（字节）覆写
        with open(path, "wb+") as f:
            for idx in range(size):
                f.write(bytes([random.randint(0,255)]))
                if not (idx % self.__align):
                    print(idx)
                    f.flush()
        return True
# ----------------------------------------------------------------------------------------------------
    def random_block(self, path):
        """
        随机擦除（块）：
        输入参数：path 文件路径
        返回参数：True 成功， False 失败
        说明：该方法通过对文件覆写随机数（块）来擦除文件，
        由于按self.__align值生成随机数（块），
        并用随机数（块）循环覆写文件，速度较快；
        但是覆写后文件大小为self.__align值的整数倍，
        并且数据按随机数（块）大小重复。
        """
        # 判断文件是否存在
        if not os.path.exists(path):
            return False
        # 生成填充数据
        fill = []
        for idx in range(self.__align):
            fill.append(random.randint(0,255))
        data = bytes(fill)
        # print("fill data:", data)
        # 读取文件大小
        size = os.path.getsize(path)
        # 对文件用二进制随机数（块）覆写
        with open(path, "wb+") as f:
            length = 0
            while length < size:
                length = length + self.__align
                f.write(data)
                f.flush()
        return True
# ----------------------------------------------------------------------------------------------------
