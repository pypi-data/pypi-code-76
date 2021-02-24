import os
from setuptools import setup

# The directory containing this file
HERE = os.getcwd()

# The text of the Readme file
README = open(HERE+"/"+"Readme.md").read()

# This call to setup() does all the work
setup(
    name="cricketpy",
    version="1.1.9",
    description="View cricket scores,commentary and scorecard from the command line",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sAksham-Ar/cricketpy",
    author="Saksham Arya",
    author_email="aryasaksham@gmail.com",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["cricketpy"],
    include_package_data=True,
    install_requires=["criapi","pyfiglet"],
    entry_points={
        "console_scripts": [
            "cricketpy=cricketpy.__main__:cricpy",
        ]
    },
)