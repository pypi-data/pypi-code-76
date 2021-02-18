#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'rest3client',
        version = '0.3.0',
        description = 'An abstraction of the requests library providing a simpler interface to enable consumption of HTTP REST APIs',
        long_description = '\nrest3client is an abstraction of the HTTP requests library (https://pypi.org/project/requests/) providing a simpler interface to enable consumption of HTTP REST APIs.\n\nThe library further abstracts the underlying requests methods providing HTTP verb equivalent methods for GET, POST, PATCH, PUT and DELETE. The library includes a RESTclient class that implements a consistent approach for processing request responses, extracting error messages from responses, providing standard headers to request methods, and enabling request resiliency through integration with the retrying library. The abstraction enables the consumer to focus on their business logic and less on the complexites of setting up requests and processing request responses.\n\nA subclass inheriting RESTclient can override the base methods providing further customization and flexibility including the ability to automatically retry on exceptions.\n',
        author = 'Emilio Reyes',
        author_email = 'emilio.reyes@intel.com',
        license = 'Apache License, Version 2.0',
        url = 'https://github.com/soda480/rest3client',
        scripts = [],
        packages = ['rest3client'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration'
        ],
        entry_points = {
            'console_scripts': ['rest = rest3client.rest:main']
        },
        data_files = [],
        package_data = {},
        install_requires = [
            'requests',
            'retrying'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
