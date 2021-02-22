from setuptools import setup

# 需要将那些包导入
packages = ["itwalker"]

# 第三方依赖
requires = [
    "PyMySQL>=0.10.0",
    "dbutils>=2.0",
    "pycryptodome>=3.9.8",
    "pytz>=2020.1",
    "urllib3>=1.25.9",
    "PyYAML>=5.3.1",
    "requests>=2.24.0",
    "sanic>=19.12.2",
    "psycopg2>=2.8.6",
]

# 自动读取readme
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='itwalker',  # 包名称
    version='2.1.6',  # 包版本
    description='',  # 包详细描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='itwalker',  # 作者名称
    author_email='2581870602@qq.com',  # 作者邮箱
    url='',  # 项目官网
    packages=packages,  # 项目需要的包
    python_requires=">=3.7",  # Python版本依赖
    install_requires=requires,  # 第三方库依赖
    zip_safe=False,  # 此项需要，否则卸载时报windows error
    classifiers=[  # 程序的所属分类列表
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
