import setuptools

from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="indi-mr",
    version="0.2.6",
    author="Bernard Czenkusz",
    author_email="bernie@skipole.co.uk",
    description="INDI - MQTT - REDIS - provides functions for transferring the INDI protocol via MQTT and converting to redis storage, with tools to read/write to redis and hence control remote instruments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bernie-skipole/indi-mr",
    packages=['indi_mr'],
    keywords='indi mqtt astronomy instrument',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator"
    ],
)
