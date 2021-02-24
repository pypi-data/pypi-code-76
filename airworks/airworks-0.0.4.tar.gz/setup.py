import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="airworks",
    version="0.0.4",
    scripts=[],
    author="valuesimplex",
    description="Tools for airworks airworks_api sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coder-baymax/airworks",
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    classifiers=[
        # 发展时期,常见的如下
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # 开发的目标用户
        'Intended Audience :: Developers',
        # 属于什么类型
        'Topic :: Software Development :: Build Tools',
        # 许可证信息
        'License :: OSI Approved :: MIT License',
        # 目标 Python 版本
        'Programming Language :: Python :: 3',
    ],
)
