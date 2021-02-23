from setuptools import find_packages, setup

setup(
    name='metlibvi',
    packages=find_packages(include=['metlibvi']),
    version='0.1.0',
    description='Library for metropolized variational inference.',
    author='Nikita Kotelevskii, Achille Thin',
    author_email='Nikita.Kotelevskii@skoltech.ru',
    url='https://github.com/nkotelevskii/metlib',
    install_requires=['torch'],
    license='MIT',
    long_description="https://github.com/nkotelevskii/metlib/blob/master/README.md",

)
