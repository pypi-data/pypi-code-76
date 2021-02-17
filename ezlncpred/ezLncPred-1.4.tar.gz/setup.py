import setuptools
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

DIR = path.dirname(path.abspath(__file__))
INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()

setuptools.setup(
    name="ezLncPred",
    version="1.4",
    author="Xiaohan Zhao, Shuai Liu, Weiyang Li, Guangzhan Zhang, Wen Zhang*",
    license='MIT',
    author_email="hannah__zhao@outlook.com",
    description="An integrated python package for lncRNA identification",
    keywords = ['lncRNA','lncRNA identification'],
    long_description_content_type = "text/markdown",
    url="https://github.com/LittleHannah/ezLncPred",
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=INSTALL_PACKAGES,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ezLncPred=ezLncPred.ezLncPred:main'
        ],
    },
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        
    ),
)
