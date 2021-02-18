from setuptools import setup,find_packages
setup(
    name='PY_GUI',
    version='1.0.0',
    description='Create a pygame session for specific functions',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/donno2048/PY-GUI',
    packages=find_packages(),
    license='MIT',
    author='Elisha Hollander',
    classifiers=['Programming Language :: Python :: 3'],
    install_requires=['pygame', 'pygame-gui'],
    entry_points={ 'console_scripts': [ 'PY-GUI=PY_GUI.__main__:main' ] }
)
