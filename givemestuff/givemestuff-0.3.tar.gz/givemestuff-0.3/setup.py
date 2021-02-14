from setuptools import setup

setup(
    name='givemestuff',
    version='0.3',
    author="Zhe Wang",
    author_email="wangzhetju@gmail.com",
    description="Giveme info",
    py_modules=['giveme'],
    install_requires=[
        'Click',
        'requires'
    ],
    entry_points='''
        [console_scripts]
        giveme=giveme.main:cli
    ''',
)