from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	name = "mllpa",
	version = "1.0.1",
	author = "Vivien WALTER",
	author_email = "walter.vivien@gmail.com",
	description = (
	"Machine Learning-assisted Lipid Phase Analysis - Module to analyse a lipid membrane generated using Molecular Dynamics (MD) simulations and predict the thermodynamical phase of the lipids."
	),
	license = "GPL3.0",
	url='https://vivien-walter.github.io/mllpa/',
	download_url = 'https://github.com/vivien-walter/mllpa/archive/v_1a.tar.gz',
	packages=[
	'mllpa',
	'mllpa.configurations']
	,
	install_requires=[
	'cython',
	'h5py',
	'MDAnalysis',
	'numpy',
	'pandas',
	'scikit-learn>=0.22.0',
	'tess',
	'tqdm'
	],
	long_description=long_description,
    long_description_content_type='text/markdown'
)
