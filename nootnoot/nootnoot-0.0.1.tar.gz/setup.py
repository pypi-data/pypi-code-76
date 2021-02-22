from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='nootnoot',
    version='0.0.1',
    description='Noot Noot!',
    py_modules=["nootnoot"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Michael Kim",
    author_email="kim.michael95@gmail.com",
)