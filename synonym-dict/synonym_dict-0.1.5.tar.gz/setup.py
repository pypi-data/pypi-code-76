from setuptools import setup, find_packages


setup(
    name='synonym_dict',
    version="0.1.5",
    packages=find_packages(),
    author="Brandon Kuczenski",
    author_email="bkuczenski@ucsb.edu",
    license="BSD 3-clause",
    install_requires=[],
    url="https://github.com/bkuczenski/synonym_dict",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    description='A class that allows retrieval of a given object by any of its synonyms',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
)
