from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 7',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = "debekCalc",
    version = "0.0.1",
    description = "Czesc",
    Long_descritpion = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author = "Marcin Debowski",
    author_email = "mdebowski78@gmail.com",
    license = "MIT",
    classifiers = classifiers,
    keywords = 'debekCalc',
    packages = find_packages(),
    install_requires = ['']
)