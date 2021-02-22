import os
import re
import sys
import time
from setuptools import setup

HERE = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(HERE, os.pardir))
TEMP_PATH = "target"

in_src = os.path.isfile(os.path.join(ROOT_DIR, "pom.xml"))

if in_src:
    pom_file = os.path.join(ROOT_DIR, 'pom.xml')
    with open(pom_file) as pomf:
        pom = pomf.read()
    version_match = re.search(r'\n  <version>([\w\.\-]+)</version>', pom)
    if version_match:
        version_string = version_match.group(1)
        print("Version from: '%s' is: %s" % (pom_file, version_string))
        version_elements = version_string.split("-")
        is_release = "SNAPSHOT" != version_elements[-1]
        base_version_elements = version_elements if is_release else version_elements[0:-1]
        base_version = base_version_elements[0] + ".".join(base_version_elements[1:])
        version = base_version if is_release else "%s+%08x" % (base_version, int(time.time()))
    else:
        print("ERROR: Cannot read version from pom file '%s'." % pom_file, file=sys.stderr)
        exit(1)

    print("Module version is: %s" % version)
    print("Writing version file in: %s" % os.path.abspath("."))
    with open("pyrander/version.py", "w") as vf:
        vf.write("__version__='%s'\n" % version)

with open('pyrander/version.py') as vf:
    exec(vf.read())

setup(
    name='pyrander',
    packages=['pyrander'],  # this must be the same as the name above
    version=__version__,
    description='A random test lib',
    author='Piotr Szul',
    author_email='piotr.szul@csiro.au',
    url='https://github.com/piotrszul/pyrander',
    keywords=['testing', 'logging', 'example'],  # arbitrary keywords
    classifiers=[],
    extras_require={
        'test': [
            'pyspark==2.1.2',
        ],
        'dev': ['twine'],
    },
    license="MIT",
)
