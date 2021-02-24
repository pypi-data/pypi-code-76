#!/usr/bin/env python3
from setuptools import setup


from link_all import __version__


setup(
    long_description_content_type='text/markdown',
    name='djangocms-link-all',
    version=__version__,
    author='Victor Yunenko',
    author_email='victor@what.digital',
    long_description=open('README.md').read(),
    url='https://gitlab.com/what-digital/djangocms-link-all',
    packages=[
        'link_all',
    ],
    include_package_data=True,
    install_requires=[
        'django >= 2.2, < 4',
        'django-cms >= 3.7, < 4',
        'django-filer',
        'jsons',
    ],
    python_requires='>= 3.7',
)
