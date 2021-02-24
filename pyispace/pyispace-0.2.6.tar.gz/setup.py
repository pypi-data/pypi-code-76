from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyispace',
    version='0.2.6',
    description='Python Instance Space Analysis package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['pyispace'],
    url='https://gitlab.com/ita-ml/pyispace',
    download_url='https://gitlab.com/ita-ml/pyispace/-/archive/v0.2.6/pyispace-v0.2.6.tar.gz',
    license='MIT',
    author='Pedro Paiva',
    author_email='paiva@ita.br',
    install_requires=[
        'numpy>=1.18.5',
        'scipy>=1.5.4',
        'scikit-learn>=0.23.1',
        'shapely>=1.7.1',
        'pandas>=1.1',
        'alphashape>=1.1.0'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
