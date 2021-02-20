import setuptools

try:
    with open('README.md', 'rb') as handle:
        description = handle.read()
except IOError as e:
    print('Failed to read README file: {}'.format(e))
    exit(1)

# Packaging tutorial: https://packaging.python.org/tutorials/packaging-projects/
# Package classifiers: https://pypi.org/classifiers/

setuptools.setup(
    name='PyMonitorLib',
    version='0.2.0',
    author='Daniel Weiner',
    author_email='info@phantomnet.net',
    description='Library for creating simple interval processes. This is especially '
                'useful for interval based monitoring application that generate '
                'telemetry at a set interval.',
    long_description=description.decode('utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/Aprelius/PyMonitorLib',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
