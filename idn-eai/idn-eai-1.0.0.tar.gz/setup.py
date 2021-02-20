from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# This call to setup() does all the work
setup(
    # Here is the module name.
    name="idn-eai",

    # version of the module
    version="1.0.0",

    # Name of Author
    author="Arpit Gupta",

    # your Email address
    author_email="gupta.arpit03@gmail.com",

    # Small Description about module
    description="Read the README file",

    # Specifying that we are using markdown file for description
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Any link to reach this module, ***if*** you have any webpage or github profile
    url="https://github.com/imarg3/idn-eai",

    packages=find_packages(exclude=("tests",)),
    # packages=["eai"],
    # include_package_data=True,

    # if module has dependecies i.e. if your package rely on other package at pypi.org
    # then you must add there, in order to download every requirement of package
    install_requires=["dnspython"],

    license="MIT",

    # classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
