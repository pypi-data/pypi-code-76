from setuptools import find_packages, setup


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pyublox',
    version_cc='{version}',
    author='Rokubun',
    author_email='info@rokubun.cat',
    description='Interface with ublox chipsets using Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='EUROPEAN SPACE AGENCY PUBLIC LICENSE - V2.4 - STRONG COPYLEFT',
    url="https://gitlab.esa.int/AMIC/pyublox.git",
    setup_requires=['setuptools-git-version-cc'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "docopt",
        "pyserial",
        "roktools>=1.4"
    ],
    entry_points={
        'console_scripts': [
            'pyublox = pyublox.main:main'
        ]
    }
)

