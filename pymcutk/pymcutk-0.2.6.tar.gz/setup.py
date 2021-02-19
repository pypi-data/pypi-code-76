import os
from setuptools import setup, find_packages

version = '0.2.6'

install_requires = [
    'pyocd>=0.28.3',
    'mbed_ls>=1.7.10',
    'pyserial==3.4',
    'xmodem',
    'future',
    "pexpect==4.7.0",
    "click>=7.0",
    "pyelftools",
    "pyyaml",
    'globster',
    'enum34'
]

version_file = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'mcutk/_version.py')

try:
    with open(version_file, 'w') as f:
        f.write("VERSION='%s'" % version)
except Exception as e:
    print(e)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pymcutk",
    version=version,
    url='https://github.com/Hoohaha/pymcutk',
    description="MCU toolkit for mcu automated test.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Haley Guo, Fly Yu",
    license="MIT License",
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mtk = mcutk.__main__:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
