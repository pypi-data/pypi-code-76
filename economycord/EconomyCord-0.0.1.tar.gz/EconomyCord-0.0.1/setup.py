from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='EconomyCord',
    version='0.0.1',
    description='A simple-compact economy package for discord.py with documentation',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://docs.economycord.xyz',  
    author='Lukas Canter',
    author_email='lukascanter07@outlook.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='discord.py', 
    packages=find_packages(),
    install_requires=['aiosqlite'] 
)