import json
import setuptools

name = "fugle_realtime_compatible"

with open("requirements.txt") as fid:
    requires = [line.strip() for line in fid]

setuptools.setup(
    name=f"{name}",
    version="0.2.8c",
    description=f"{name}",
    install_requires=requires,
    long_description="使用方法同 [fugle-realtime](https://pypi.org/project/fugle-realtime/) 主要只是兼容 python3.8、python3.9",
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=setuptools.find_packages(),
    package_data={"": ["*.json"]},
)
