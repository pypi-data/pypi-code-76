from setuptools import find_namespace_packages, setup

# Installation dependencies
install_requires = [
]

# Development dependencies
development_extras = [
    'coverage>=5.3,<6.0',
    'flake8>=3.8,<4.0',
    'pytest>=6.2,<7.0',
    'tox>=3.21,<4.0',
]

setup(
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    include_package_data=True,
    license='MIT License (MIT)',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='{{cookiecutter.repository_url}}',
    author='{{cookiecutter.author}}',
    author_email='{{cookiecutter.author_email}}',
    install_requires=install_requires,
    extras_require={
        'development': development_extras,
    },
    classifiers=[
        # See https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        # Typically you may include
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Environment :: Console',
        # 'Environment :: Web Environment',
        # 'Intended Audience :: Developers',
        # 'Intended Audience :: End Users/Desktop',
        # 'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        # 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        # 'Topic :: Office/Business',
        # 'Topic :: Software Development',
    ],
)
