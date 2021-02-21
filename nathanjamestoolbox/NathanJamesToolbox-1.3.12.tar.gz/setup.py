import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='NathanJamesToolbox',
    version='1.3.12',
    description='Collection of tools developed for NathanJames',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/pfajardo-nj/NathanJamesToolbox',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    packages=['NathanJamesToolbox'],
    include_package_data=True,
    install_requires=[
        'requests',
        'slacker',
        'datetime',
        'google.cloud',
        'pymysql',
        'selenium'
    ]
)
