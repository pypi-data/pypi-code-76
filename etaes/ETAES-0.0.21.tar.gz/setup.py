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
    name='ETAES',
    version='0.0.21',
    auther='jiawei.li',
    auther_email='jiawei.li@shopee.com',
    description='A temp upload for ETA prediction',
    long_description_content_type="text/markdown",
    url='',
    packages=setuptools.find_packages(),
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      ],
    python_reqires='>=3.6',
    include_package_data=True,
)
