from setuptools import setup

desc = '''
# 辅助工具库

* 时间辅助工具： time_helper
* 任务辅助工具： dfx_task
* 其他辅助工具： funcs

## 安装

pip install dfxhelper

## 使用

from dfx_utils.funcs import random_str

tmp_str = random_str(32)
'''


setup(
    name='DfxHelper',
    version='0.0.33',
    author='dfx',
    author_email='1817556010@qq.com',
    url='https://www.baidu.com',
    license='GPL',
    packages=['dfx_utils', 'dfx_utils/api_work'],
    description='辅助工具',
    python_requires='>=3.6.0',
    long_description=desc,
)