# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path

with open("README.rst", "r") as file:
    long_description = file.read()

_dir = path.dirname(__file__)
with open(path.join(_dir, 'OpFlowLab', 'version.py'), encoding="utf-8") as f:
    exec(f.read())

setup(
    name='OpFlowLab',
    version=__version__,
    description='Calculation of optical flow velocity field in biological images',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    install_requires=[
        "opencv-python>4.3.0",
        "numpy>=1.17.0",
        "matplotlib>=3.0.0",
        "numba>=0.47.0",
        "scikit-image>=0.17.1",
        "pykdtree>=1.3.4",
        "scipy>=1.5.0",
        "PyQt5>=5.9.2",
        "tqdm>=4.40.0",
        "ruamel.yaml>=0.16.0",
        "pyqtgraph>=0.11.0",
        "QtAwesome>=1.0.2"
    ],
    author='Xianbin Yong',
    author_email='xianbin.yong@u.nus.edu',
    url='https://gitlab.com/xianbin.yong13/OpFlowLab',

    packages=find_packages(),
    license="GPLv3",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.7',
    project_urls={
        'Documentation': 'https://opflowlab.readthedocs.io/',
        'Research group': 'https://ctlimlab.org/',
        'Source': 'https://gitlab.com/xianbin.yong13/OpFlowLab',
    },
    entry_points={
        'console_scripts': ['opflowlab=OpFlowLab.OpFlowLab_GUI:main'],
    },
)