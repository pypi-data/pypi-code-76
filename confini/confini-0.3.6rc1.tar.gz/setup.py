from setuptools import setup

f = open('./README.md', 'r')
long_description = f.read()
f.close()

setup(
        name='confini',
        version='0.3.6rc1',
        description='Parse, verify and merge all ini files in a single directory',
        author='Louis Holbrook',
        author_email='dev@holbrook.no',
        license='GPL3',
        long_description=long_description,
        long_description_content_type='text/markdown',
        install_requires=[
            'python-gnupg>=0.4.6,<0.5.0',
        ],
        packages=[
            'confini',
            'confini.runnable',
        ],
        url='https://gitlab.com/nolash/python-confini',
        )
