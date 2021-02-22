from distutils.core import setup

setup(
    name='quicklock3',
    packages=['quicklock'],
    version='0.1.8',
    description='A simple Python 3.x resource lock to ensure only one process at a time is operating with a particular resource.',
    author='Mathias Ziebarth (forked from Nate Ferrero)',
    author_email='mathias.ziebarth@gmail.com',
    url='https://github.com/untixx/quicklock/',
    download_url='https://github.com/untixx/quicklock/tarball/0.1.8',
    keywords=['lock', 'locking', 'singleton', 'process', 'resource', 'exclusive lock'],
    classifiers=[],
    platforms='any',
    install_requires=[
        'psutil>=2.2'
    ]
)
