import pathlib

import pyttsx3
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="movefiletoextensionfolder",
    version="1.0.1",
    description="It will move all files in the source path to their respective ext folder in destination path provided",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/bhaskarkh/movefiletoextensionfolder",
    author="kumar bhaskar",
    author_email="bhaskar646@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["movefiletoextensionfolder"],
    include_package_data=True,
    install_requires=["pyttsx3==2.6"],

)
