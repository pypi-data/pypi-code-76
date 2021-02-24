from setuptools import setup
with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name = 'shapley:lz',
    version = '0.0.4',
    description = 'Computes the Shapley Lorenz Zonoid share of a set of covariates',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Roman Enzmann',
    author_email = 'ryenzmann@hotmail.com',
    url = 'https://github.com/roye10/ShapleyLorenz',
    license = 'MIT',
    py_modules = ['shapley_lz'], # list of actual python code modules,
    package_dir = {'': 'src'}, # code is under a src directory

    classifiers = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    keywords = 'shapley lorenz zonoid explainable machine learning AI',

    install_requires = ['numpy', 'scipy', 'tqdm', 'matplotlib', 'sklearn'],

    extras_require = {
        'dev': [
            'pytest>=3.7',
        ],
    },
)

# next built this by running the command
# 'python setup.py bdist_wheel' in terminal --> outputs a wheel file, that is appropriate to upload to PiPy
# copies .py code file into the lib directory
# gitignore egg-info
# build directory --> moved files here
# actual wheel file in dist directory

# then 'pip install -e .' --> -e links to the code one is working on NOT copying code into another location.
# Hence once installed can continue working on it, w/o having two copies of code.
# Full stop says install THIS package in the current directory (defined by setup.py file)
# run this everytime changing setup.py file.

# N.B. code is now in source directory not in current directory --> cannot import code.py yet
