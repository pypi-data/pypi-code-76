from setuptools import setup, find_packages
import pkg_resources
import re


def get_version(VERSIONFILE):
    verstrline = open(VERSIONFILE, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
    return verstr


with open('./requirements.txt') as reqfile:
    requirements = reqfile.readlines()

def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()

setup(
    name="meajur",
    version=get_version("VERSION"),
    description="Command line ",
    long_description=readfile('README.md'),
    author="Athmane Bouazzouni",
    author_email="Athmane2dz@gmail.com",
    url="",
    py_modules=['meajur'],
    license=readfile('LICENSE'),
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'meajur = meajur:main'
        ]
    },
)