from setuptools import setup, find_packages

VERSION = "0.1.0"
DESCRIPTION = "A collection of tools for analyzing the HMJR Collection."
LONG_DESCRIPTION = "A collection of tools for analyzing the HMJR Collection."

setup(
    name="hmjr",
    version=VERSION,
    author="Teddy Randby",
    author_email="tedrandby@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['python-graphql-client'],
    keywords=['archives','analysis'],
    url="https://github.com/TeddyRandby/hmjrPyTools",
    download_url="https://github.com/TeddyRandby/hmjrPyTools/archive/0.1.0.tar.gz",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ]
)

