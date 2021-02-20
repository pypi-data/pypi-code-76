#!/usr/bin/env python3
'''setup.py for use by setuptools'''
import setuptools

NAME = 'h5utils'

packages = setuptools.find_packages()

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=NAME,
    version="0.0.2",
    author="Mike Taverne",
    author_email="Mike.Taverne@bristol.ac.uk",
    description='''Utilities to work with HDF5 files.
      Notably includes h5tovts, which converts HDF5 files to structured VTK files
      for visualization with VTK-aware programs.''',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/mtav/h5utils",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["numpy", "vtk", "h5py"],
    entry_points={
        'console_scripts': ['h5tovts=h5utils.h5tovts:main'],
    },
    include_package_data=True,
)
