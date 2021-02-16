from setuptools import setup, find_packages

VERSION = '0.0.6' 
DESCRIPTION = 'My package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="19CS30055_package", 
        version=VERSION,
        author="Neha Dalmia",
        author_email="<nehadalmia002@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
        ], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=[],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
