from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'simple test cricket player score prediction via your cricket knowledge'
LONG_DESCRIPTION = 'A deep use of random module is done in that to make it accurate, if you know much about test cricket players than you will be able to predict their possible runs in the future matches'

# Setting up
setup(
    name="cric_predict",
    version=VERSION,
    author="YusiferZendric (Aditya Singh)",
    author_email="<mail@yusiferzendric.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'cricket', 'test-cricket', 'score prediction'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)