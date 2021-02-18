import pathlib
import setuptools
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='bal-tools',
      version='1.2.5',
      url='https://github.com/blackacornlabs/bal_tools',
      long_description=README,
      description='Black Acorn Labs tools library',
      long_description_content_type="text/markdown",
      packages=setuptools.find_packages(),
      author='BlackAcornLabs',
      author_email='git@blackacorn.io',
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Programming Language :: Python :: 3.8",
          "Intended Audience :: Developers",
          'Topic :: Software Development',
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.8',
      zip_safe=False,
      install_requires=[
      ])
