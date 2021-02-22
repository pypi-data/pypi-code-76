import os
from setuptools import find_packages
from setuptools import setup


# Update
# Delete all the file in the dist folder
# Update the version in the setup.py file
# python setup.py sdist bdist_wheel
# twine upload dist/*


lib_folder = os.path.dirname(os.path.realpath(__file__))
requirements_path = lib_folder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirements_path):
    with open(requirements_path) as fp:
        install_requires = fp.read().splitlines()


setup(
    name='nlp4ml',
    packages=find_packages(include=['nlp4ml']),
    version='0.1.23',
    description='Python NLP wrapper',
    author='Yang Wang',
    author_email='penguinwang@smail.nchu.edu.tw',
    url='https://github.com/penguinwang96825/nlp4ml.git',
    license='MIT',
    install_requires=install_requires,
    tests_require=['pytest==4.4.1'],
    setup_requires=['pytest-runner'],
    test_suite='tests'
)
