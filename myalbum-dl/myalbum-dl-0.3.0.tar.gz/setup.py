import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
]

REQUIREMENTS = ['requests']

setuptools.setup(
    name='myalbum-dl',
    version='0.3.0',
    author='Giovanni Salinas',
    author_email='gbs3@protonmail.com',
    description='A command line tool for downloading albums from MyAlbum',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/GBS3/myalbum-dl',
    packages=setuptools.find_packages(),
    classifiers=CLASSIFIERS,
    keywords=['myalbum', 'scraper', 'download', 'photos', 'videos'],
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': ['myalbum-dl=myalbum_dl.myalbum_dl:main']
    }
)
