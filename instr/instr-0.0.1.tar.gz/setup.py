from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Simple wrapper for various SCPI-compliant instruments'
LONG_DESCRIPTION = 'Convenience wrapper around raw pyvisa objects.'

setup(
        name="instr", 
        version=VERSION,
        author="igrekus",
        author_email="",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],         
        keywords=['python', 'scpi', 'visa'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)
