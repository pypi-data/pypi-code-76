# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains the package setup tools.

# Copyright (C) 2018  Niklas Bohn (GFZ, <nbohn@gfz-potsdam.de>),
# German Research Centre for Geosciences (GFZ, <https://www.gfz-potsdam.de>)

# This software was developed within the context of the EnMAP project supported by the DLR Space Administration with
# funds of the German Federal Ministry of Economic Affairs and Energy (on the basis of a decision by the German
# Bundestag: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


from setuptools import setup, find_packages
from importlib import util

requirements_save_to_install_with_setuptools = [
    "scikit-image", "glymur", "pyprind", "gdown",
    "dicttoxml", "tables", "pandas", "psutil", "sympy", "pyproj",
    "cerberus", "scipy", "tqdm", "dill", "geoarray", "mpld3",
    "jsmin", "iso8601", "pint", "matplotlib", "numpy",
    "pillow", "arosics>=1.2.4", "numba", "netCDF4", "pyrsr", "py_tools_ds",
    "cachetools", "requests", "ecmwf-api-client", "openpyxl"]  # openpyxl is implicitly required by pandas.read_excel()

other_requirements = {  # dict of "[needed import]: [proposed command for install]
    "gdal": "conda install -c conda-forge gdal",
    "tables": "conda install -c conda-forge pytables",
    "h5py": "conda install -c conda-forge h5py",
    "numba": "conda install -c conda-forge numba",
    "pyfftw": "conda install -c conda-forge pyfftw",
    "pygrib": "conda install -c conda-forge pygrib",
    "sklearn": "conda install -c conda-forge scikit-learn<=0.24.0"
}

with open("README.rst") as readme_file:
    readme = readme_file.read()

version = {}
with open("sicor/version.py", encoding="utf-8") as version_file:
    exec(version_file.read(), version)

requirements = requirements_save_to_install_with_setuptools

setup_requirements = ["setuptools-git"]

test_requirements = requirements + [
    "coverage", "mock", "pylint", "mypy", "pycodestyle", "pydocstyle", "flake8", "sphinx", "sphinx-argparse", "nose",
    'nose2', "nose-htmloutput", "rednose", "enpt", "ipython_memory_usage", "urlchecker"
]

# test for packages that do not install well with pip
not_installed = {}
for needed_import, propossed_install_command in other_requirements.items():
    is_installed = util.find_spec(needed_import)
    if is_installed is None:
        not_installed[needed_import] = propossed_install_command
if len(not_installed) > 0:
    raise ImportError((
        "Could not find the following packages (please use different installer, e.g. conda).\n" +
        "\n".join(["missing: '{missing_import}', install, e.g. by: '{command}'".format(
            missing_import=missing_import, command=command) for missing_import, command in not_installed.items()])
    ))

setup(
    authors="Niklas Bohn, Daniel Scheffler, Maximilian Brell, André Hollstein, René Preusker",
    author_email="nbohn@gfz-potsdam.de",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    description="Sensor Independent Atmospheric Correction",
    data_files=[
        ("data", [
            "sicor/sensors/S2MSI/GranuleInfo/data/S2_tile_data_lite.json",
            "sicor/sensors/S2MSI/data/S2A_SNR_model.xlsx",
            "sicor/AC/data/k_liquid_water_ice.xlsx",
            "sicor/AC/data/newkur_EnMAP.dat",
            "sicor/AC/data/solar_irradiances_400_2500_1.dill"
        ])],
    keywords=["SICOR", "EnMAP", "EnMAP-Box", "hyperspectral", "remote sensing", "satellite", "atmospheric correction"],
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3 (GPLv3)",
    long_description=readme,
    long_description_content_type="text/x-rst",
    name="sicor",
    package_dir={"sicor": "sicor"},
    package_data={"sicor": ["AC/data/*", "tables/*"]},
    packages=find_packages(exclude=["tests*", "examples"]),
    scripts=[
        "bin/sicor_ac.py",
        "bin/sicor_ecmwf.py",
        "bin/sicor_ac_EnMAP.py"
    ],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url="https://git.gfz-potsdam.de/EnMAP/sicor",
    version=version["__version__"],
    zip_safe=False
)
