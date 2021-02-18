"""Sets up Python-DDNS to be installed"""
import os
from setuptools import setup, find_packages
from pddns import __version__


def read(fname):
    """Reads README.md as long description"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_reqs = open("requirements.txt").readlines()
test_reqs = open("requirements-dev.txt").readlines()[1:]

setup(
    name="python-ddns",
    version=__version__,
    author="Cyb3r Jak3",
    author_email="jake@jwhite.network",
    install_requires=["dnspython", "requests", "psutil"],
    description="A DDNS client that updates providers with host machine's current IP.",
    url="https://gitlab.com/Cyb3r-Jak3/python-ddns",
    project_urls={
        "Changelog": "https://gitlab.com/Cyb3r-Jak3/python-ddns/-/blob/master/CHANGELOG.md",
        "Issues": "https://gitlab.com/Cyb3r-Jak3/python-ddns/issues",
        "Source": "https://gitlab.com/Cyb3r-Jak3/python-ddns",
    },
    data_files=[("config.conf", ["pddns/config.dist.conf"])],
    license='GPL-3.0',
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Installation/Setup",
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    entry_points={
        "console_scripts": ['pddns=pddns.pddns:run']
    },
    tests_require=test_reqs
)
