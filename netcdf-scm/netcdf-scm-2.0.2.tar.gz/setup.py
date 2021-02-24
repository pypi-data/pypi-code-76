from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

import versioneer

PACKAGE_NAME = "netcdf-scm"
DESCRIPTION = "Processing netCDF files for use with simple climate models"
KEYWORDS = [
    "netcdf",
    "netCDF",
    "python",
    "climate",
    "atmosphere",
    "simple climate model",
    "reduced complexity climate model",
    "data processing",
]

AUTHOR = "Zebedee Nicholls"
EMAIL = "zebedee.nicholls@climate-energy-college.org"
URL = "https://github.com/znicholls/netcdf-scm"
PROJECT_URLS = {
    "Bug Reports": "https://github.com/znicholls/netcdf-scm/issues",
    "Documentation": "https://openscm.readthedocs.io/en/latest",
    "Source": "https://github.com/znicholls/netcdf-scm",
}
LICENSE = "3-Clause BSD License"
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: BSD License",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.7",
]

ENTRY_POINTS = {"console_scripts": ["netcdf-scm = netcdf_scm.cli:cli"]}


REQUIREMENTS_INSTALL = [
    "cftime<1.4",  # until resolution to https://github.com/SciTools/cf-units/issues/163
    "click",
    "numpy",
    "python-dateutil",
    "pymagicc>=2.0.0rc5",
    "scmdata>=0.7",
    "scipy",
    "tqdm",
]
REQUIREMENTS_AR6REGIONS = ["regionmask>=0.6"]
REQUIREMENTS_TESTS = [
    "codecov",
    "nbval",
    "pytest>=4.0,<5.0",
    "pytest-benchmark",
    "pytest-cov",
    "pytest-console-scripts",
    "pytest-xdist",
]
REQUIREMENTS_NOTEBOOKS = [
    "ipywidgets",
    "notebook",
    "expectexception",
    "seaborn",
]
REQUIREMENTS_DOCS = [
    "nbsphinx",
    "sphinx>=1.4,<2.1",
    "sphinx_rtd_theme",
    "sphinx-click",
    "sphinx-copybutton",
]
REQUIREMENTS_DEPLOY = ["twine>=1.11.0", "setuptools>=38.6.0", "wheel>=0.31.0"]
requirements_dev = [
    *[
        "bandit",
        "beautifulsoup4",
        "black==19.10b0",
        "black-nb",
        "flake8",
        "isort",
        "mypy",
        "nbdime",
        "pydocstyle",
        "pylint>=2.4.0",
    ],
    *REQUIREMENTS_AR6REGIONS,
    *REQUIREMENTS_DEPLOY,
    *REQUIREMENTS_DOCS,
    *REQUIREMENTS_NOTEBOOKS,
    *REQUIREMENTS_TESTS,
]

REQUIREMENTS_EXTRAS = {
    "ar6regions": REQUIREMENTS_AR6REGIONS,
    "deploy": REQUIREMENTS_DEPLOY,
    "dev": requirements_dev,
    "docs": REQUIREMENTS_DOCS,
    "notebooks": REQUIREMENTS_NOTEBOOKS,
    "tests": REQUIREMENTS_TESTS,
}


SOURCE_DIR = "src"

# no tests/docs in `src` so don't need exclude
PACKAGES = find_packages(SOURCE_DIR)
PACKAGE_DIR = {"": SOURCE_DIR}
PACKAGE_DATA = {"netcdf_scm": ["weights/*.nc"]}


README = "README.rst"

with open(README, "r") as readme_file:
    README_TEXT = readme_file.read()


class netCDFSCM(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        pytest.main(self.test_args)


cmdclass = versioneer.get_cmdclass()
cmdclass.update({"test": netCDFSCM})

setup(
    name=PACKAGE_NAME,
    version=versioneer.get_version(),
    description=DESCRIPTION,
    long_description=README_TEXT,
    long_description_content_type="text/x-rst",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    project_urls=PROJECT_URLS,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    install_requires=REQUIREMENTS_INSTALL,
    extras_require=REQUIREMENTS_EXTRAS,
    cmdclass=cmdclass,
    entry_points=ENTRY_POINTS,
)
