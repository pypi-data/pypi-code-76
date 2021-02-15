from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Assorted PyQt5 tools'
LONG_DESCRIPTION = 'Some convenience classes for PyQt5.'

setup(
        name="qttools", 
        version=VERSION,
        author="igrekus",
        author_email="",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],         
        keywords=['python', 'pyqt5'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)
