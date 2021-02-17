from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'Making statistics easier with python'
LONG_DESCRIPTION = 'A package that allows to do complex statsitical calculation very easily'

# Setting up
setup(
    name="StatsWithSahira",
    version=VERSION,
    author="Sahira Sheikh",
    author_email="<sheikh_sahira1703@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['statsmodels', 'numpy', 'pandas', 'sklearn', 'matplotlib'],
    keywords=['python', 'statistics', 'made', 'easy', 'mean', 'median', 'mode', 'standard deviation', 'skewness'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
