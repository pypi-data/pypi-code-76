from setuptools import setup,find_packages
setup(
    name='blade_runner',
    include_package_data=True,
    version='1.1.0',
    packages=find_packages(),
    package_data={'blade_runner': ['blade_runner'],},
    license='MIT',
    author='Elisha Hollander',
    classifiers=['Programming Language :: Python :: 3'],
    install_requires=['pygame'],
    entry_points={ 'console_scripts': [ 'blade-runner=blade_runner.__init__:main' ] }
)
