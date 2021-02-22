from distutils.core import setup

setup(
    name='setify',
    packages=['setify'],
    version='0.8',
    license='MIT',
    description='Dataset packages',
    author='Mina Gabriel',
    author_email='developer.mina@gmail.com',
    url='https://github.com/MinaGabriel/setify.git',
    download_url='https://github.com/MinaGabriel/setify/archive/v0.8.tar.gz',
    keywords=['Dataset', 'Data'],
    install_requires=[
        'pandas',
        'numpy',
        'tqdm',
        'colorama',
        'tables'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    long_description='Setify is an open-source dataset package manager written in Python and designed to enable fast experimentation for Machine Learning, Setify allows you to reach hundreds of datasets with one command.',
    long_description_content_type='https://developer-mina.gitbook.io/setify/',
)
