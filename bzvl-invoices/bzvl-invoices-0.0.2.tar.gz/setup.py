from setuptools import find_packages, setup


setup(
    name='bzvl-invoices',
    version='0.0.2',

    author='Stefan Bunde',
    author_email='stefanbunde+git@posteo.de',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'bzvl-invoices=bzvl_invoices.bzvl_invoices:main',
        ],
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
