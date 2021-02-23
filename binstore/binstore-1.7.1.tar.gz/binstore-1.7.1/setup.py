from distutils.core import setup, Extension, DEBUG
import setuptools
sfc_module = Extension('binstore', sources = ['module_bins.c'])

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="binstore",
    version="1.7.1",
    author="John Herrema",
    author_email="jherrema@gmail.com",
    description="Module to implement C extension Bins class for bin-based storage of items",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "https://pypi.org/project/binstore/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    ext_modules = [sfc_module]
)