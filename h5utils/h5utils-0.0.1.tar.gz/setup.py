#!/usr/bin/env python3
import setuptools

name='h5utils'

#packages=[f'{name}.{package}'
        #for package
        #in setuptools.find_packages(where='src')]
packages=setuptools.find_packages()
#print(packages)
#raise
#print(packages)

#packages = (
    #setuptools.find_packages(exclude=['data'])
    #+
    #[
        #f'{name}.{package}'
        #for package
        #in setuptools.find_namespace_packages(include=['data'])
    #]
#)
#print(packages)
#raise
  

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version="0.0.1",
    author="Mike Taverne",
    author_email="Mike.Taverne@bristol.ac.uk",
    description="Utilities to work with HDF5 files. Notably includes h5tovts, which converts HDF5 files to structured VTK files for visualization with VTK-aware programs.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/mtav/h5utils",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    #package_dir={
        #f'{name}.data': 'data',
    #},
    python_requires='>=3.6',
    install_requires=["numpy","vtk","h5py"],
    #scripts=['bin/h5tovts.py'],
    entry_points = {
      #'console_scripts': ['funniest-joke2=funniest.command_line:main'],
      'console_scripts': ['h5tovts=h5utils.h5tovts:main'],
    },
    include_package_data=True,
)


#setuptools.setup(
    #packages=PACKAGES,
    #package_dir={
        #'MyPackage.JSONs': 'JSONs',
    #},
    #include_package_data=True,
    ##
    #name='Something',
    #version='1.2.3',
#)
