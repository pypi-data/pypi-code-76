import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oneworld", 
    version="1.0.4",
    author="Antoni Aguilar Mogas",
    author_email="aguilar.mogas@gmail.com",
    description="Python mapping made easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://taguilar@bitbucket.org/taguilar/oneworld",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: GIS"
    ],
    python_requires='>=3.7',
    install_requires=[ 
          "numpy>=1.18.1",
          "pandas>=1.0.1",
          "matplotlib>=3.2.0",
          "seaborn>=0.10.0",
          "jinja2>=2.11.1",
          "cartopy>=0.17.0"
      ],
)
