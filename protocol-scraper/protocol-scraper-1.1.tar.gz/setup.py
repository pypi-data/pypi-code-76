from setuptools import setup, find_packages

VERSION = '1.1'
DESCRIPTION = 'Python CLI for automatically writing protocols.'
LONG_DESCRIPTION = 'This package contains a CLI that scrapes protocol.io to write detailed protocols for a given search.'

# Setting up
setup(
        name="protocol-scraper",
        version=VERSION,
        author="James Sanders",
        author_email="james.sanders1711@gmail.com",
        url = 'https://github.com/J-E-J-S/protocol-scraper',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'requests==2.20.0',
            'click==7.1.2'
        ],
        entry_points = {
            'console_scripts':['protocol-scraper=protocolScraper.protocolScraper:cli']
        }
)
