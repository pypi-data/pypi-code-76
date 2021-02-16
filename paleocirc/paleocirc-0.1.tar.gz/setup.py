from setuptools import find_packages, setup

setup(
    name='paleocirc',
    packages=find_packages(include=['paleocirc']),
    url='https://github.com/xFranciB/paleocirc',
    download_url='https://github.com/xFranciB/paleocirc/archive/v0.1.tar.gz',
    version='v0.1',
    description='My first Python library',
    author='xFranciB',
    license='MIT',
    install_requires=['requests', 'beautifulsoup4'],
)