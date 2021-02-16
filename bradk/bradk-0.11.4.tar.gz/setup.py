# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
# python setup.py sdist
# python -m twine upload dist/*

from setuptools import setup

setup(name='bradk',
      version='0.11.4',
      description='The bradk packages developed by Brad Kim',
      url='http://github.com/bomsoo-kim/packages',
      author='Brad Kim',
      author_email='bk2717@columbia.edu',
      license='MIT',
      packages=['bradk', 'bradk.model_selection', 'bradk.finance', 'bradk.neural_networks'],
      zip_safe=False)