from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pset1nik',
      version='0.1.1',
      description='pset1 test',
      py_modules=['pset1'],
      package_dir={'': 'src'},
      packages=['pset1'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
          "Operating System :: OS Independent",
      ],
      url="https://github.com/nikhar1210",
      author="Nikhar",
      author_email="nikhar1210@gmail.com",
      install_requires=['xlrd==1.2.0',
                        'canvasapi>=2.1.0',
                        'environs>=9.3.1',
                        'awscli>=1.19.12'])