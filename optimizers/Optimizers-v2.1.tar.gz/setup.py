from distutils.core import setup
setup(
    name='Optimizers',
    packages=['Optimizers'],
    version='v2.1',
    license='GNU General Public License v3.0',
    description='A collection of examples for learning mathematical modelling',
    author='David S.W. Lai',
    author_email='s.w.lai@tue.nl',
    url='https://github.com/davidswlai/',
    download_url='https://github.com/davidswlai/Optimizers/releases/latest',
    keywords=['Optimizers', 'Mathematical Models', 'Logistics', 'Routing', 'Scheduling'],
    install_requires=[
        'requests>=2.24.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
