from setuptools import find_packages, setup

from distutils.core import setup

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.

setup(name = "nlutils",
    version = "0.0.3-beta",
    description = "Toolkit for research, both for engineers and researchers. It provides colorful logs, esay figuring and parameter collector logs, which aims to boost machine learning research.",
    author = "Mengyang Liu",
    author_email = "mengyang_liu@foxmail.com",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found
    #recursively.)
    packages = find_packages(),
    requires= [
        'coloredlogs',
        'matplotlib',
        'torch',
        'numpy'
    ]
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
    #'runner' is in the root.
    #
    #This next part it for the Cheese Shop, look a little down the page.
    #classifiers = []
)