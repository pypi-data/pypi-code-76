import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PolyMID",
    version="0.0.3",
    author="Nathaniel M Vaanti",
    author_email="",
    description="PolyMID is a software package for analyzing stable-isotope tracing data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VacantiLab/PolyMID",
    packages=setuptools.find_packages(),
    package_data={'': ['*.txt']},
    install_requires=[
          'numpy',
          'pandas',
          'tk'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
