from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='pylgorithm',
    version='0.0.1',
    description="A Package That Contains Lots Of Commonly Used Algorithms To Make The Developer's Life Easier",
    Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Gilad Barak',
    autor_email='gilad.barakGB007@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='gilad',
    packages=find_packages(),
    install_requires=['']
)