from setuptools import setup
import os
import re


def get_version(*file_paths):
    """Retrieves the version from audiolipsum/__init__.py"""
    filename = os.path.join(
        os.path.dirname(__file__),
        *file_paths
    )

    version_file = open(filename, 'r').read()
    version_match = re.search(
        r"^__version__ = '([^']+)'",
        version_file,
        re.M
    )

    if version_match is not None:
        return version_match.group(1)

    raise RuntimeError('Unable to find version string.')


version = get_version('audiolipsum', '__init__.py')
readme = open('README.md').read()


setup(
    name='opawg-audiolipsum',
    version=version,
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Open Podcast Analytics Working Group',
    url='https://github.com/opawg/audiolipsum',
    packages=['audiolipsum'],
    include_package_data=True,
    install_requires=[
        'Click',
        'lorem',
        'mutagen',
        'Pillow',
        'qrcode'
    ],
    license="MIT",
    entry_points=(
        '[console_scripts]\n'
        'audiolipsum=audiolipsum.cli:main'
    )
)
