#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Mark
# Mail: 1782980833@qq.com
# Created Time:  2020-3-29 16:00:00
#############################################

from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="ZmUser",  # 这里是pip项目发布的名称
    version="1.0.0",  # 版本号，数值大的会优先被pip
    keywords=("ZmUser", "zm"),
    description="北京蓝气球用户、角色、权限封装",
    long_description="http://markdoc.handsomemark.com/project-3/doc-24/",
    license="MIT Licence",
    url="https://gitee.com/medincmedinc/zm_user",  # 项目相关文件地址，一般是github
    author="Zm",
    author_email="1782980833@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["flask","sqlalchemy_utils","psycopg2"]  # 这个项目需要的第三方库
)
