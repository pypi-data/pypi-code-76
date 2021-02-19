from setuptools import setup, find_packages

setup(
    name='gloat-matcher',
    version='0.1',
    description='Backend assigment for Gloat',
    packages=find_packages(include=['src', 'src.*']),
    download_url='https://github.com/Rantzur1992/gloat-backend/archive/0.1.tar.gz',
    python_requires='>3.7',
    install_requires=[
        'Click'
    ],
    entry_points=
    '''
        [console_scripts]
        matcher=src.Runner:match
    ''',
)
