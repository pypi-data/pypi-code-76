import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name='neadva',
    packages=['neadva'],
    version='0.51',
    license='MIT',
    description='Hungarian Tax Authority NAV reporting api library',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Andrew Azarov',
    author_email='andrew@serverastra.com',
    url='https://github.com/andrew-azarov/neadva',
    include_package_data=True,
    download_url='https://github.com/andrew-azarov/neadva/archive/v0.51-alpha.tar.gz',
    keywords=['tax', 'hungary', 'reporting', 'api'],
    setup_requires=['setuptools-git'],
    install_requires=['pycryptodome', 'requests', 'base62', 'lxml'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
