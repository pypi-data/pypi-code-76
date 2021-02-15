from setuptools import setup, find_packages
import os

with open('VERSION', 'r') as f_ver:
    VERSION = f_ver.read()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='watson_machine_learning_client_V4',
    version=VERSION,
    python_requires='>=3.6',
    author='IBM',
    author_email='svagaral@in.ibm.com, nagiredd@in.ibm.com, amadeusz.masny1@ibm.com',
    description='Watson Machine Learning API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='BSD',
    classifiers=['Development Status :: 4 - Beta',
                 'Natural Language :: English',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python :: 3.6',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: POSIX :: Linux',
                 'Operating System :: Microsoft :: Windows',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Information Technology',
                 'Topic :: Software Development :: Libraries',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Scientific/Engineering :: Information Analysis',
                 'Topic :: Internet'],
    keywords=["watson", "machine learning", "IBM", "Bluemix", "client", "API", "IBM Cloud"],
    url='http://wml-api-pyclient-v4.mybluemix.net',
    packages=find_packages(),
    install_requires=[
        'requests',
        'urllib3',
        'pandas<=1.0.5',
        'certifi',
        'lomond',
        'tabulate',
        'ibm-cos-sdk==2.7.*'
    ],
    include_package_data=True
)
