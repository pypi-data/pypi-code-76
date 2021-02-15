from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='TradingTechnicals',
    version='0.0.1',
    description='Technical Analysis',
    Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='MegzMugz',
    License='MIT',
    classifiers=classifiers,
    keywords='technicals',
    packages = find_packages(),
    install_requires=['pandas-datareader', 'datetime']
)