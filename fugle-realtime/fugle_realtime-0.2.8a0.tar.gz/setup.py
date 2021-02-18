import json
import setuptools
import os
from pathlib import Path

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)
loc = Path(__location__)
name = "fugle_realtime"

with open("requirements.txt") as fid:
    requires = [line.strip() for line in fid]

setuptools.setup(
    name=f"{name}",
    version="0.2.8-a",
    description=f"{name}",
    install_requires=requires,
    long_description=open(loc.joinpath("README.md"), "r").read(),
    long_description_content_type="text/markdown",
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
