import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='sea-common',
    version='1.0.18',
    author='SEA Biopharma',
    author_email='sea.biopharma@gmail.com',
    description='SEA Web Services common python packages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sea-biopharma/sea-common',
    packages=setuptools.find_packages(),
    install_requires=[
        'flask>=1.1.2',
        'flask-sqlalchemy>=2.4.4',
        'strawberry-graphql>=0.45.3',
    ],
    python_requires='>=3.8',
)
