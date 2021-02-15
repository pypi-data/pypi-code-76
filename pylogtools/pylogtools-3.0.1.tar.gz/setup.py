from setuptools import setup

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='pylogtools',
    version='3.0.1',
    py_modules=['pylogtools'],
    install_requires=[
    ],
    license='MIT',
    entry_points='''
        [console_scripts]
        pylogtools=pylogtools:pylogtools
    ''',
)
