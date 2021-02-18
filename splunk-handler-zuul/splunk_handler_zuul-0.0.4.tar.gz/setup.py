from setuptools import setup

setup(
    name='splunk_handler_zuul',
    version='0.0.4',
    license='MIT License',
    description='A Python logging handler that sends zuul conponent logs to Splunk',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Lida Liu',
    author_email='lindaliu0712@gmail.com',
    url='https://github.com/lidall/splunk_handler',
    packages=['splunk_handler_zuul'],
    install_requires=['requests >= 2.6.0, < 3.0.0', 'python-json-logger >= 2.0.1'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Logging'
    ]
)
