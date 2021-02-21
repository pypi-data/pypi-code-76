import setuptools

setuptools.setup(
  name='SysDynPy',
  version='0.1.0',
  author='Tim Herker',
  author_email='tim.herker@stud.hs-bochum.de',
  url='https://github.com/t16h05008/SysDynPy',
  license='LICENSE.txt',
  description='A framework to build System Dynamics models',
  long_description=open('README.md').read(),
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
  install_requires=[
    "matplotlib"
   ]
)