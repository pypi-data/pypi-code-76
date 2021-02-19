import setuptools
from pybind11.setup_helpers import Pybind11Extension
from glob import glob

setuptools.setup(
    name='palsgraph',
    version='0.0.4',
    url="https://github.com/kalngyk/palsgraph",
    packages=setuptools.find_packages(),
    py_modules=['palsgraph'],
    ext_modules=[Pybind11Extension("palsgetpos", glob("src/*.cpp"))],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

