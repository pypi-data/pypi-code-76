from setuptools import setup

setup(
    name='slatmet',
    version='2.0',
    packages=['slatmet'],
    url='',
    license='MIT',
    author='Martin Slater',
    author_email='martinhslater@gmail.com',
    description='Weather forecast data',
    keywords=['weather', 'forecast', 'openweather'],
    install_requires=[
        'requests',
    ]
)
