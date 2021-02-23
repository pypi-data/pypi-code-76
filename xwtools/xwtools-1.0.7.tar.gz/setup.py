import os
from setuptools import setup

# 根据es版本安装python es库
# pymongo
# "elasticsearch-dsl>=6.3.1",
# "elasticsearch-dsl>=7.2.0",

requirements = [
    'pika==0.12.0',
    'numpy==1.16.4',
    'shortuuid==0.5.0',
    'threadpool==1.3.2',
    'redis==3.3.11',
    'elasticsearch_dsl==7.3.0',
    'matplotlib==3.1.3',
    'jieba==0.42.1',
    'wheel==0.34.2',
    'PyMySQL==0.9.3',
    'pypinyin==0.37.0',
    'selenium==3.141.0',
    'elasticsearch==7.8.1',
    'pymongo==3.10.1',
    'pandas==1.1.1',
    'requests==2.22.0',
    'beautifulsoup4==4.9.3',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='xwtools',
    version='1.0.7',
    packages=[
        "xwtools",
    ],
    license='BSD License',  # example license
    description='xwtools',
    long_description='这是一个通用的python工具包，帮助你快速的开发项目',
    install_requires=requirements,
    long_description_content_type="text/markdown",
    url='https://github.com/xulehexuwei',
    author='xuwei',
    author_email='15200813194@163.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
