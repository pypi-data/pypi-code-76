from setuptools import setup
setup(
    name = 'eldf',
    py_modules = ['eldf'],
    version = '2021.2',
    description = 'A Python implementation of ELDF data format',
    long_description = open('README.md', encoding = 'utf-8').read(),
    long_description_content_type = 'text/markdown',
    author = 'Alexander Tretyak',
    author_email = 'alextretyak@users.noreply.github.com',
    url = 'https://eldf.org',
    download_url = 'https://sourceforge.net/p/eldf/code/ci/default/tarball',
    license = "MIT",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
    ],
)
