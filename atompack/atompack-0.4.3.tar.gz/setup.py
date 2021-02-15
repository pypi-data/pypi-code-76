from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(name="atompack",
      version="0.4.3",
      description="A flexible Python library for atomic structure generation.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Seaton Ullberg",
      author_email="seatonullberg@gmail.com",
      url="https://github.com/seatonullberg/atompack",
      license="MIT License",
      packages=find_packages(),
      package_data={'': ['data/*.json']},
      include_package_data=True,
      extras_require={"dev": [
          "isort",
          "mypy",
          "pdoc3",
          "pyflakes",
          "pytest",
          "pytest-benchmark",
          "yapf",
      ]})
