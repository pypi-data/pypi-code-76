#!/usr/bin/python3
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tpnetwork',
    version='1.2.0a2',
    author='Thomas Pajon',
    author_email='th.pajon45@gmail.com',
    description='A python network module',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tomarrok/tpnetwork',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Networking',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Natural Language :: English'
    ],
    packages=setuptools.find_packages(),
    install_requires=['dpath'],
    python_requires='>=3.5'
)
