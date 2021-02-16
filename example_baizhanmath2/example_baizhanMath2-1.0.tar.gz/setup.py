#coding=utf-8
from distutils.core import setup
setup(
    name='example_baizhanMath2', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，教学测试使用，无内容', #描述
    author='crab.ge', # 作者
    author_email='182076141@qq.com',
    py_modules=['baizhanMath2.demo1','baizhanMath2.demo2'] # 要发布的模块
)