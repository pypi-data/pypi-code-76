#!/usr/bin/python3
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tpnetwork',
    version='1.1.1',
    author='Thomas Pajon',
    author_email='th.pajon45@gmail.com',
    description='A python network module',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tomarrok/tpnetwork',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: System :: Networking',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Natural Language :: English'
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6'
)
