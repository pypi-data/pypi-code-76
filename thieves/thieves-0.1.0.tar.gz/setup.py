from setuptools import setup

setup(
    name='thieves',
    version='0.1.0',
    description='Thieves is a concurrent, thread-safe Google Drive uploader library.',
    url='https://github.com/midoublelo/thieves',
    author='Millo Evers',
    author_email='contact@milloevers.com',
    license='MPL-2.0',
    packages=['thieves'],
    install_requires=['pydrive'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 3 :: Only'
    ]
)