from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Features to make transfering data into LaTeX documents easier'
LONG_DESCRIPTION = 'A module that can create simple tables from arrays of data.'

# Setting up
setup(
    name="latexqol",
    version=VERSION,
    author="konradg",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyperclip'],
    keywords=['python', 'LateX'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research ",
        "Programming Language :: Python :: 3.6",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)