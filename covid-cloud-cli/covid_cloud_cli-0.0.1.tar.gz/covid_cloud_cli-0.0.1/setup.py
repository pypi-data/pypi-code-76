from setuptools import find_packages, setup


setup(
    name='covid_cloud_cli',
    packages=find_packages(include=['covid_cloud_cli']),
    version='0.0.1',
    description='DNAstack COVID Cloud CLI Library',
    author='Derek',
    license='MIT',
    install_requires=['search-python-client>=0.1.7',
                      'urllib3==1.26.3',
                      'requests==2.25.1',
                      'click==7.1.2'
                      ],
)