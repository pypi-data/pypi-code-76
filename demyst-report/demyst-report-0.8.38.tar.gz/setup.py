from setuptools import setup

setup(
    name='demyst-report',

    version='0.8.38',

    description='',
    long_description='',

    author='Demyst Data',
    author_email='info@demystdata.com',

    license='',
    packages=['demyst.report'],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'demyst-analytics>=0.8.38',
        'matplotlib==3.1.2',
        'scipy==1.3.0',
        'seaborn==0.10.0'
    ]
)
