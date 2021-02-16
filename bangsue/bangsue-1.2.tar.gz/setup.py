import setuptools
from setuptools.config import read_configuration

conf_dict = read_configuration("setup.cfg")
with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="bangsue",
    version="1.2",
    author="ARSANANDHA",
    author_email="arsanandha.ap@gmail.com",
    description="Bangsue. Thai Codename Generator",
    long_description="Bangsue. Thai Codename Generator from data.go.th, BTS(Wikipedia), MRT(Wikipedia)",
    long_description_content_type="text/markdown",
    url="https://github.com/aphisitworachorch/bangsue",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    python_requires='>=3.6',
)
