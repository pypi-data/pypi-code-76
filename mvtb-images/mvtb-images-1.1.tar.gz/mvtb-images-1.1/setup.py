from setuptools import setup, find_packages

import pkg_resources
import os
import sys
here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

release = "1.1"

# list all data folders here, to ensure they get packaged

data_folders = [
    'mvtbimages',
]

# https://stackoverflow.com/questions/18725137/how-to-obtain-arguments-passed-to-setup-py-from-pip-with-install-option
# but get an error
def package_files(directory):
    paths = []
    for (pathhere, _, filenames) in os.walk(directory):
        # skip bulky image folders, PyPI has 100MB limit :()
        if any([folder in pathhere for folder in ['bridge', 'campus', 'mosaic']]):
            continue
        for filename in filenames:
            paths.append(os.path.join('..', pathhere, filename))
    return paths

extra_files = []
for data_folder in data_folders:
    extra_files += package_files(data_folder)
# extra_files.append('../montage.png')
print(extra_files)
print(find_packages(exclude=["test_*", "TODO*"]))

setup(
    name='mvtb-images',

    version=release,

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    description='Images for the Machine Vision Toolbox for Python.', #TODO
    
    long_description=long_description,
    long_description_content_type='text/markdown',

    classifiers=[
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 5 - Production/Stable',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3 :: Only'],

    project_urls={
        'Source': 'https://github.com/petercorke/machinevision-toolbox-python',
    },

    url='https://github.com/petercorke/machinevision-toolbox-python',

    author='Peter Corke',

    author_email='rvc@petercorke.com', #TODO

    keywords='python machine-vision computer-vision color blobs',

    # license='MIT',

    package_data={'mvtbimages': extra_files},
    # include_package_data=True,
    # data_files = [('mvtbimages', ["../image-data/monalisa.png", "../image-data/street.png"]),],

    packages=find_packages(exclude=["test_*", "TODO*"]),


)
