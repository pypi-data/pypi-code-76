from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    include_package_data=True,
    name='snir',
    version='0.1.3',
    description='a package to handle sounds and text colors',
    long_description="the package contains sounds and text colors",
    url='',
    author='snir dekel',
    author_email='snirdekel101@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='sound',
    packages=find_packages(),
    install_requires=['']
)
