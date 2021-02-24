import io
import os

from setuptools import setup, find_packages

dir = os.path.dirname(__file__)

with io.open(os.path.join(dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytrends-httpx',
    python_requires=">=3.7.1",
    version='1.0.0',
    description='Pseudo API for Google Trends - Async version with httpx',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hctpbl/pytrends-httpx',
    author='Héctor Pablos',
    author_email='hectorpablos@gmail.com',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: AsyncIO',
        'Framework :: Trio',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=['httpx==0.16.*', 'pandas>=0.25', 'lxml', 'tenacity>=6.3'],
    keywords='google trends api search async asyncio httpx',
    packages=find_packages(include=['pytrends_httpx']),
)
