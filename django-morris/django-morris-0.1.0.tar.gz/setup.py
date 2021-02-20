#!/usr/bin/env python

import os

from setuptools import find_packages, setup

version = {}
with open("morris/version.py") as fp:
    exec(fp.read(), version)

base_url = "https://gitlab.com/heg-ulmuten"
package_name = "django-morris"
package_url = f"{base_url}/{package_name}"
package_path = os.path.abspath(os.path.dirname(__file__))
long_description_file_path = os.path.join(package_path, "README.md")
long_description_content_type = "text/markdown"
long_description = ""
try:
    with open(long_description_file_path) as f:
        long_description = f.read()
except IOError:
    pass

setup(
    name=package_name,
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    include_package_data=True,
    version=version["__version__"],
    description="A hexadecimal django color field with a preview.",
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    author="HeG Ulmuten",
    author_email="heg@ulmuten.net",
    url=package_url,
    keywords=[
        "admin",
        "color",
        "colorfield",
        "colorpreview",
        "django",
        "field",
        "python",
    ],
    requires=["django (>=2.2)"],
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Build Tools",
    ],
    license="MIT",
)
