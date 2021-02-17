from setuptools import setup, find_packages

VERSION = '1.1' 
DESCRIPTION = 'My package'
LONG_DESCRIPTION = 'My first Python package but with a longer description'

# Setting up
setup(
        name="my_package_19CS10073", 
        version=VERSION,
        author="Rajat Bachhawat",
        author_email="<myemail@abc.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['matplotlib', 'opencv-python'],
        keywords=['python', 'first-package'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)
