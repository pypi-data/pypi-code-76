#!/usr/bin/env python
"""
Setup Module to setup Python Handlers for the SparkMonitor extension.
"""
import os

from jupyter_packaging import (
    create_cmdclass, install_npm, ensure_targets,
    combine_commands, ensure_python, get_version,
)
import setuptools

name="sparkmonitor"

HERE = os.path.abspath(os.path.dirname(__file__))
NBEXTENSION = os.path.join(HERE, "nbextension")

ensure_python(">=3.5")

# Get our version
version = get_version(os.path.join(name, "_version.py"))

lab_path = os.path.join(HERE, name, "labextension")
nb_path = os.path.join(HERE, name, "nbextension")

# Representative files that should exist after a successful build
targets = [
    os.path.join(HERE, "lib", "index.js"),
    os.path.join(nb_path, "extension.js"),
    os.path.join(HERE, name, "listener_2.11.jar"),
    os.path.join(HERE, name, "listener_2.12.jar"),
]

package_data_spec = {
    name: [
        "*"
    ]
}

data_files_spec = [
    ("share/jupyter/lab/extensions", lab_path, "*.tgz"),
    ("etc/jupyter/jupyter_notebook_config.d",
     "jupyter-config", "sparkmonitor.json"),
]

cmdclass = create_cmdclass("deps", 
    package_data_spec=package_data_spec,
    data_files_spec=data_files_spec
)

cmdclass["deps"] = combine_commands(
    install_npm(HERE, build_cmd="build:labextension", npm=["jlpm"]),
    install_npm(NBEXTENSION, build_cmd="webpack"),
    install_npm(HERE, build_cmd="build:scalalistener", npm=["jlpm"]),
    ensure_targets(targets),
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name=name,
    version=version,
    url="https://github.com/swan-cern/jupyter-extensions",
    author="SWAN Admins",
    description="Helper to connect to CERN's Spark Clusters",
    long_description= long_description,
    long_description_content_type="text/markdown",
    cmdclass= cmdclass,
    packages=setuptools.find_packages(),
    install_requires=[
        "jupyterlab~=2.0",
        "bs4",
    ],
    zip_safe=False,
    include_package_data=True,
    license="AGPL-3.0",
    platforms="Linux",
    keywords=["Jupyter", "JupyterLab", "SWAN", "CERN"],
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Jupyter",
    ],
)


if __name__ == "__main__":
    setuptools.setup(**setup_args)
