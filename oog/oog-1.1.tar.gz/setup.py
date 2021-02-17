"""Installation script."""

from setuptools import find_packages
from setuptools import setup
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='oog',
    version='1.1',
    description=('Object-Oriented Games is a python-based game engine.'),
    author='Nicholas Watters',
    url='https://github.com/jazlab/oog.github.io',
    license='MIT license',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        'ai',
        'reinforcement-learning',
        'python',
        'machine learning',
        'objects',
        'psychology',
        'neurophysiology',
        'psychophysics',
        'physics',
        'environment',
    ],
    packages=(
        ['oog_demos', 'oog'] + 
        ['oog_demos.' + x for x in find_packages('oog_demos')] +
        ['oog.' + x for x in find_packages('oog')]
    ),
    install_requires=[
        'spriteworld',
        'imageio',
        'mss',
    ],
    tests_require=[
        'nose',
        'tqdm',
        'gym',
    ],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
    ],
)