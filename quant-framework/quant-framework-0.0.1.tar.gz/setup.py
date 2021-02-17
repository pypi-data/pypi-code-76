from setuptools import setup, find_packages

setup(
    name='quant-framework',
    version='0.0.1',
    author='Brendan Geck',
    author_email='bpgeck@gmail.com',
    url='https://github.com/brendangeck/quant-framework',
    description='A basic framework for backtesting and going live with quant strategies',
    long_description=open('README.md').read(),
    license='LICENSE.txt',
    packages=find_packages(),
    scripts=[],
    entry_points={
        "console_scripts": [
            "quant_framework=quant_framework.main:main"
        ],
    },
    install_requires=[]
)