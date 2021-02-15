import setuptools

setuptools.setup(
    name='mkrexx',
    version='0.7.2',
    author='Guilherme Cartier',
    description='Python library that leverage include statements in rexx files for the build process.',
    packages=['mkrexx',
              'mkrexx.utilities'],
    install_requires=['pyrexx',
                      'python-decouple'],
    python_requires='>=3.6'
)
