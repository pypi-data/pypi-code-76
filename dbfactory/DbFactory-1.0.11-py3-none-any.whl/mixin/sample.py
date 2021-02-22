# coding:utf-8
# author caturbhuja
# date   2020/11/4 4:22 下午 
# wechat chending2012 
import inspect


class SampleMixInFunction:
    """
    --------------------------- 提示命令封装 -----------------------------
    inspect.stack()[0][3] = _some_function 也就是这个方法自身的名字，用于反射自身
    """
    def _some_function(self, *args, **kwargs):
        """未来会定义的一些抽象方法"""
        return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)