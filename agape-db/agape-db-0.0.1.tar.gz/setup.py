import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='agape-db',
    version='0.0.1',
    packages=['agape'],
    include_package_data=True,
    license='All rights reserved.', 
    description='Field factories for Django models.',
    long_description=README,
    long_description_content_type='text/markdown',
    url = 'https://gitlab.com/MiverikMinett/agape',
    author='Maverik Minett',
    author_email='maverik.minett@gmail.com',
    test_suite = "runtests.runtests",
    install_requires = [
        'Django>=2.2.9',
        'django-autoslug>=1.9.7'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)
