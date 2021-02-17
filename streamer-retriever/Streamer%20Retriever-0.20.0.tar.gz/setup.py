#! /usr/bin/env python3


from streamerretriever import constants
import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='Streamer Retriever',
    version=constants.__version__,
    author=constants.__author__,
    description='Filter Twitch streams that are online from follows text file.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/obtusescholar/streamerretriever',
    entry_points={ 'console_scripts': ['streamerretriever = streamerretriever.cli:main'] },
    packages=setuptools.find_packages(
        include=['streamerretriever'],
        exclude=['streamerretriever/__pycache__']
    ),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
    license='GPLv3+',
    keywords='twitch terminal',
    python_requires='>=3.8'
)
