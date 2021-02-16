# coding: utf-8
from setuptools import setup, find_packages  # noqa: H301

NAME = "groupdocs-assembly-cloud"
VERSION = "21.1.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.16", "six >= 1.10", "certifi", "python-dateutil"]
TEST_REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    description="GroupDocs.Assembly for Cloud API Reference",
    author='Yaroslaw Ekimov',
    author_email="yaroslaw.ekimov@aspose.com",
    url="https://github.com/groupdocs-assembly-cloud",
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
        'Topic :: Office/Business :: Office Suites',
		'Topic :: Software Development :: Libraries',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
	],
    keywords=["groupdocs", "python", "groupdocs cloud", "assembly"],
    install_requires=REQUIRES,
	tests_require=TEST_REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    This repository contains GroupDocs.Assembly Cloud SDK for Python source code. This SDK allows you to work with GroupDocs.Assembly Cloud REST APIs in your Python applications quickly and easily, with zero initial cost.
    """
)
