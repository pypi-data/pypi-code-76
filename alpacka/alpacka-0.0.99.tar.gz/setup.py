from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requirements = [
    "keras",
    "sklearn",
    "matplotlib",
    "tensorflow>=2.2",
    "numpy>=1.18"]

setup(name='alpacka',
      version='0.0.99',
      description='The alpacka Python package, used to extract and visualize metadata from text data sets',
      author='Fredrik Möller',
      author_email='fredrikmoller@recordefuture.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/BernhardMoller/alpacka',
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent"],
      licence='LICENCE.txt',
      python_requires='>=3.6',
      install_requires=install_requirements
      )
