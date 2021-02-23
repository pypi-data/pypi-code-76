import time

from setuptools import setup, find_packages

setup(
    name='flask-templates',
    version='0.0.39',
    author='hzy',
    platforms='any',
    packages=find_packages(),
    package_data={'flask_templates': ['resource/*.yaml', '*.py', '*.pyd'],
                  '': ['*.yaml']
                  },
    install_requires=[
        'flask==1.1.1',
        'requests==2.22.0',
        'pyyaml==5.1.2',
        'pymysql==0.9.3',
        'sqlacodegen==2.1.0',
        'pytest-cov',
        'tenacity==5.1.1',
        'flask-cors==3.0.8',
        'redis==3.3.8',
        'simplejson==3.16.0',
        'marshmallow==3.2.1',
        'pytz==2020.4',
        'flask_apscheduler==1.11.0',
        'nacos-sdk-python==0.1.5',
        'celery==4.4.7',
        'flower==0.9.7'
    ]
)
