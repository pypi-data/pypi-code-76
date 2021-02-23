"""
setup.py is configuration information for the *x3d* PyPi project.
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="x3d",
    version="4.0.40", 
    author="Don Brutzman",
    author_email="brutzman@nps.edu",
    description="Package support for Extensible 3D (X3D) Graphics International Standard (IS)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.web3d.org/x3d/stylesheets/python/python.html",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9", # not 3.9.x
        "Topic :: Text Processing :: Markup :: VRML"
    ],
###     "Topic :: Text Processing :: Markup :: X3D",
)

### package_dir={'x3d': 'dist/x3d'}, # testing...