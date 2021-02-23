import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from os import path, environ
import sys
import subprocess

_base_version = '1.1'

root_dir = path.abspath(path.dirname(__file__))

def _get_requires_list():
    if (sys.version_info.major == 2):
        if sys.maxsize > 2**32:
            # if 64bit:
            raise RuntimeError(
                'Python 2.7 64bit on Windows is not supported. Please find alternative'
                ' ways to install the relevant dependancies')
        else:
            # 32 bit
            result = 'mapy_dependencies_py27'
    else:
        minor_version_str = {
            6: 'mapy_dependencies_py36',
            7: 'mapy_dependencies_py37',
            8: 'mapy_dependencies_py38',
            9: 'mapy_dependencies_py39'
        }

        result = minor_version_str[sys.version_info.minor]

    # return as a list not a string
    return [result]

def readme():
    with open(path.join(root_dir, 'README.md')) as f:
        return f.read()


# See https://packaging.python.org/guides/single-sourcing-package-version/
# This uses method 4 on this list combined with other methods.
def _get_version_number():
    travis_build = environ.get('TRAVIS_BUILD_NUMBER')
    travis_tag = environ.get('TRAVIS_TAG')

    if travis_build:
        if travis_tag:
            version = travis_tag
        else:
            version = '{}.dev{}'.format(_base_version, travis_build)

        with open(path.join(root_dir, 'VERSION'), 'w') as version_file:
            version_file.write(version.strip())
    else:
        try:
            ver = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
            version = '{}+local.{}'.format(_base_version, ver.decode('ascii').strip())
        except Exception:
            with open(path.join(root_dir, 'VERSION')) as version_file:
                version = version_file.read().strip()

    return version


setup(
    name='mapactionpy_controller_dependancies',
    version=_get_version_number(),
    description='Controls the workflow of map and infographic production',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='http://github.com/mapaction/mapactionpy_controller_dependancies',
    author='MapAction',
    author_email='github@mapaction.com',
    license='GPL3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=_get_requires_list(),    
    test_suite='unittest',
    tests_require=['unittest'],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Win32 (MS Windows)",
        "Operating System :: Microsoft :: Windows"
    ])
