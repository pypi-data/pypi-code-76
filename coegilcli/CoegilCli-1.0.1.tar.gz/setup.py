from setuptools import setup, find_packages

setup(
    name='CoegilCli',
    version='1.0.1',
    author="Mike Levine",
    author_email="mike@coegil.com",
    description="Coegil Command Line Interface",
    packages=find_packages(),
    include_package_data=True,
    url="https://coegil.com",
    python_requires='>=3.6',
    install_requires=[
        'click',
        'wheel',
        'boto3',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'coegil=coegil.Cli:cli'
        ]
    }
)