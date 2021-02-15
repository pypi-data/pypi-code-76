import setuptools

with open("READMEpypi.rst", "r") as fh:
    long_description = fh.read()


setuptools.setup(
      name="scikit-mcda",
      version="0.21.47",
      author="Antonio Horta",
      author_email='ajhorta@cybercrafter.com.br',
      description="Library for Multi-criteria Decision Aid Methods",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://gitlab.com/cybercrafter/scikit-mcda",
      install_requires=[
            "numpy~=1.18",
            "pandas~=1.0",
            "tabulate"
            ],
      license="Apache License 2.0",
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Mathematics"
      ],
      python_requires='>=3.6',
      )
