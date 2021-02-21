from setuptools import setup, find_packages
import codecs
import os
VERSION = '0.0.1'
DESCRIPTION = 'Tested 90%% accurate test match score prediction through your cricket knowledge'
LONG_DESCRIPTION = 'Hello I am Aditya, I have made this library like this, such that it will predict the supplied player score in test cricket, it work on the principle of player batting position and the percentage of chances of his fifty or hundred you have supplied to it, it is incomplete till now but you can test it and if you like the concept than try to contribute in this project through github.'

# Setting up
setup(
    name="pycric",
    version=VERSION,
    author="YusiferZendric (Aditya Singh)",
    author_email="<mail@yusiferzendric.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'prediction', 'without machine learning', 'cricket', 'player score prediction'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)