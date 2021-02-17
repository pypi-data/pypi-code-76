from os.path import dirname, join, abspath
from setuptools import setup, find_packages

ROOT_DIR = dirname(abspath(__file__))

requirements = [
  'pysolr',
  'django>=1.11'
]

setup_requirements = []

setup(
    author="Haidar Naufal Sunni",
    author_email='haidar.naufal@gramedia.digital',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Django Health Check custom module for GDN supported services",
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='gdn_health_check',
    name='gdn_health_check',
    packages=find_packages(where='src'),
    package_dir={'gdn_health_check': join('src','gdn_health_check')},
    setup_requires=setup_requirements,
    version='0.0.1',
    zip_safe=False,
)