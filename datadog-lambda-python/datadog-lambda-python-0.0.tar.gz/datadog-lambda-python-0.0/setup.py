from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='datadog-lambda-python',
      version='0.0',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Datadog',
      license='MIT',
      install_requires=["datadog-lambda"],
      zip_safe=False)
print("This is a placeholder, you should use the datadog-lambda package instead. https://pypi.org/project/datadog-lambda/\n")
