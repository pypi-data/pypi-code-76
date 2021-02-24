from setuptools import setup, find_packages

setup(
    name='webMole',
    version=open('VERSION.txt').read().strip(),
    description='This is a webscraper module in python, it is focused on geting products from online stores, but it works as a webscraper, it uses selenium and pandas.',
    long_description="README",
    url='http://samuelsilva.live/',
    author='Samuel Silva',
    author_email='goncalves@axiros.com',
    license='MIT',
    packages=find_packages(),
    
    install_requires=[
        'selenium',
        'openpyxl',
        'pandas'
    ],
    keywords="webscraper"
)