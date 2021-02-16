import re
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from os import path, environ
import sys
import subprocess

_base_version = '1.1'

root_dir = path.dirname(path.abspath(__file__))

temp_name = path.split(root_dir)[1]
temp_name = re.sub(r'_', '-', temp_name.lower())
pkg_name = re.search('mapy[-_]dependencies[-_]py\d\d', temp_name)[0]

def _get_platform_str():
    result = None
    if (sys.version_info.major == 2):
        if sys.maxsize > 2**32:
            # if 64bit:
            result = 'cp27-cp27m-win_amd64'
        else:
            # 32 bit
            result = 'cp27-cp27m-win32'
    else:
        minor_version_str = {
            6: 'cp36-cp36m-win_amd64',
            7: 'cp37-cp37m-win_amd64',
            8: 'cp38-cp38-win_amd64',
            9: 'cp39-cp39-win_amd64'
        }

        result = minor_version_str[sys.version_info.minor]

    return result


def _get_classifiers_strs():
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Win32 (MS Windows)",
        "Operating System :: Microsoft :: Windows"
    ]
    
    if pkg_name[-2:] == "27":
        classifiers.append("Programming Language :: Python :: 2.7")
    else:
        classifiers.append("Programming Language :: Python :: 3")

    return classifiers
    
def get_wheel_paths():
    platform_str = _get_platform_str()

    # The order these packages are intalled  matters, which is why
    # this does not just do something like
    # `glob.glob('{}/dependancy_wheels/*.whl'.format(root_dir))`

    if (sys.version_info.major == 2):
        wheel_list = [
            (platform_str, 'pyproj-1.9.6-{}.whl'.format(platform_str)),
            (platform_str, 'Shapely-1.6.4.post2-{}.whl'.format(platform_str)),
            (platform_str, 'GDAL-2.2.4-{}.whl'.format(platform_str)),
            (platform_str, 'Fiona-1.8.13-{}.whl'.format(platform_str)),
            (platform_str, 'Rtree-0.9.3-{}.whl'.format(platform_str))
        ]
    else:
        wheel_list = [
            (platform_str, 'pyproj-3.0.0.post1-{}.whl'.format(platform_str)),
            (platform_str, 'Shapely-1.7.1-{}.whl'.format(platform_str)),
            (platform_str, 'GDAL-3.1.4-{}.whl'.format(platform_str)),
            (platform_str, 'Fiona-1.8.17-{}.whl'.format(platform_str)),
            (platform_str, 'Rtree-0.9.4-{}.whl'.format(platform_str))
        ]

    # platform netural packages. This is installed here (rather than using the
    # `install_requires` parameter, because of the dependancy on other wheel files.
    wheel_list.append(('py2.py3-none-any', 'geopandas-0.6.2-py2.py3-none-any.whl'))

    return [path.join(root_dir, 'dependency_wheels', dir_name, wheel_name) for dir_name, wheel_name in wheel_list]


def install_from_wheels(command_subclass):
    """A decorator for classes subclassing one of the setuptools commands.

    It modifies the run() method so that it prints a friendly greeting.

    https://blog.niteo.co/setuptools-run-custom-code-in-setup-py/
    """
    orig_run = command_subclass.run

    def modified_run(self):
        print('Custom run() method')

        if sys.platform == 'win32':
            for wheel_path in get_wheel_paths():
                # wheel_path = path.join(root_dir, 'dependency_wheels', dir_name, wheel_name)
                print('Installing {} from wheel file.'.format(wheel_path))
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', wheel_path])
                    # pip_result = pip.main(['install', wheel_path])
                    # print('pip result = {}'.format(pip_result))
                except SystemExit:
                    pass

        print('About to call default install run() method')
        orig_run(self)

    command_subclass.run = modified_run
    return command_subclass


@install_from_wheels
class CustomDevelopCommand(develop):
    pass


@install_from_wheels
class CustomInstallCommand(install):
    pass


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
    name=pkg_name,
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
    },
    version=_get_version_number(),
    description='Controls the workflow of map and infographic production',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='http://github.com/mapaction/mapy_dependancies_deploy',
    author='MapAction',
    author_email='github@mapaction.org',
    license='GPL3',
    packages=find_packages(),
    include_package_data=True,
    test_suite='unittest',
    tests_require=['unittest'],
    zip_safe=False,
    classifiers=_get_classifiers_strs()
)
