from setuptools import find_packages, setup

setup(
    name='ngitung',
    packages = find_packages(include=['ngitung']),
    version='0.1.0',
    description='Uji Coba Library Python Sederhana',
    author = 'Mahasin',
    author_email='mmasadar@gmail.com',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)