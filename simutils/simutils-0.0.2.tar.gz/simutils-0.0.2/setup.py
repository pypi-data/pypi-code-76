from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='simutils',
    version='0.0.2',
    description='Tools for logging simulation information for later reproductions.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Shunichiro Nomura',
    author_email='nomura@space.t.u-tokyo.ac.jp',
    install_requires=[],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    url='https://github.com/shunichironomura/simutils',
    download_url='https://github.com/shunichironomura/simutils/archive/v0.0.2.tar.gz',
    license='MIT',
    packages=find_packages(exclude=('tests')),
    test_suite='tests',
    zip_safe=False
)
