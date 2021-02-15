from setuptools import setup, find_packages
import pathlib

classifiers = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Other Audience',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Software Development :: Build Tools',
    'Topic :: System :: Operating System',
    'Topic :: System :: Shells',
    'Topic :: System :: System Shells',
    'Topic :: Terminals',
    'Topic :: Utilities',
]

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

CHANGELOG = (HERE / 'CHANGELOG.md').read_text()

setup(
    name='batchexec',
    version='0.0.4a',
    description='Batch execute any task, with simple json config',
    long_description=README + CHANGELOG,
    long_description_content_type='text/markdown',
    url='https://github.com/krisu-g/Universal_batch_executer',
    author='Krzysztof Grabowski',
    author_email='grabowski.krzysztof@gmail.com',
    license='GNU GPLv3',
    classifiers=classifiers,
    keywords='batch,convert,run,shell,terminal,os,independent,',
    packages=find_packages(),
    install_requires=['']
)
