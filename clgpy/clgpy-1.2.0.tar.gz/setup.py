from setuptools import setup, find_packages

setup(
    name='clgpy',
    version='1.2.0',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='clgpy is the package for any new programmer to work with Python.',
    long_description=open('README.md').read(),
    install_requires=['numpy'],
    url='https://github.com/Rajatku301999mar/clgpypackage',
    author='Rajat Kumar, Gurmehar Singh Soni',
    author_email='rajatdj1999@gmail.com, gurmeharsoni.vit@gmail.com'
)
