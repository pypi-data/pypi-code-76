from setuptools import find_packages
from setuptools import setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="tkns",
    version="0.1",
    # scripts=['dokr'],
    author="Alex Lopez",
    author_email="pedrolop15@hotmail.com",
    description="A token and keys generation utility package",
    long_description="long_description",
    # long_description_content_type="text/markdown",
    # url="https://github.com/furby32/tkns",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
