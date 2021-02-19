import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).parent

requirements = [
    'six',
    'urllib3',
    'certifi',
    'python-dateutil'
]

setup(
    name='cakemail-openapi',
    version='1.4.6',
    description='OpenAPI generated client for Cakemail Next-gen API',
    python_requires='>=3.6',
    url='https://github.com/cakemail/cakemail-openapi-python',
    license='MIT',
    packages=[
        'cakemail_openapi',
        'cakemail_openapi.api',
        'cakemail_openapi.models'
    ],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False
)
