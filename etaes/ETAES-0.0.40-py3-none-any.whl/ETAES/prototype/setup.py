#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :setup.py.py
# @Time     :2021/2/24
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @File     :setup.py
# @Time     :2021/2/1
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None
import setuptools

with open("README.md", "r") as f:
    desc = f.read()

setuptools.setup(
    name='$YOUR PROJECT NAME',
    version='$YOUR RECENT VERSION',
    auther='$YOUR NAME',
    auther_email='$YOUR EMAIL',
    description='$YOUR FANTASTIC PROJECT DESC',
    long_description_content_type="text/markdown",
    url='',
    packages=setuptools.find_packages(),
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      ],
    python_reqires='>=3.6'
)
