import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='clusterservice',
    version='0.0.12',
    author='Mark Moloney',
    author_email='m4rkmo@gmail.com',
    description='ClusterService API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/markmo/clusterservice',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
    ],
    python_requires='>=3.6',
)
