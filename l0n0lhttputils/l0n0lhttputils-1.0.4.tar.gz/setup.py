import setuptools

# 读取项目的readme介绍
with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="l0n0lhttputils",  # 项目名称，保证它的唯一性，不要跟已存在的包名冲突即可
    version="1.0.4",
    author="l0n0l",  # 项目作者
    author_email="1038352856@qq.com",
    description="平时常用的http server|mysql|腾讯cos|微信公众号等库的集合",  # 项目的一句话描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/l00n00l/http_server_utils",  # 项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pymysql",
        "aiohttp[speedups]",
        "requests",
        "cos-python-sdk-v5",
        "tencentcloud-sdk-python",
        "pycryptodome",
        "pyyaml",
        "xlrd"
    ],
)
