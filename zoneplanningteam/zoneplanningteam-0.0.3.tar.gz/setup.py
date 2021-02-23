from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'First zone planning team package'
LONG_DESCRIPTION = 'This is a package to be used by zone planning team'

# Setting up
setup(
    name="zoneplanningteam",
    version=VERSION,
    author="Pablo Galaz Cares",
    author_email="<pablo.galaz.c@ug.uchile.cl>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
