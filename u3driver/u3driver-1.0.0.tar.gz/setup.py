# coding: utf-8
import os, re
from setuptools import setup, find_namespace_packages

with open(os.path.join("u3driver", "__init__.py"), encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='u3driver',
    version=version,
    python_requires='>=3.6',
    description='u3driver',
    url='https://github.com/king3soft/u3driver',
    author='king3soft',
    author_email='buutuud@gmail.com',
    license='GPLv3',
    include_package_data=True,
    packages=find_namespace_packages(include=['u3driver.*', "u3driver"]),
    install_requires=''''''.split('\n'),
    zip_safe=False)