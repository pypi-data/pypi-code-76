# -*- coding: utf-8 -*-


class JustError(Exception):
    """
        @author: hujian9@jd.com
        @description: 应用程序异常
        @date: 2019-10-08 15:24
        @modified by:
    """

    def __init__(self, message):
        """
        初始化函数
        :param message: 异常信息
        """
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message
