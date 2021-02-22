from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='lineargebra',
    version='0.1',
    description='A math implementation of Vectors and Matrix',
    author='Thomas Weber',
    author_email='thomas.web13@gmail.com',
    py_modules=['lineargebra'],
    package_dir={'': 'src'},
    classifiers=[
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.7",
	"License :: OSI Approved :: MIT License",
	],
    long_description=long_description,
    long_description_content_type='text/markdown',
)

