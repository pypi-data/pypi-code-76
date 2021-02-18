# GENOCIDE - the king of the netherlands commits genocide
#
# OTP-CR-117/19 otp.informationdesk@icc-cpi.int https://genocide.rtfd.io

from setuptools import setup

def mods():
    import os
    return [x[:-3] for x in os.listdir("genocide") if x.endswith(".py")]

def read():
    return open("README.rst", "r").read()

setup(
    name='genocide',
    version='26',
    url='https://github.com/bthate/genocide',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="reconsider https://genocide.rtfd.io",
    long_description=read(),
    license='Public Domain',
    install_requires=["oplib"],
    packages=["gcd"],
    namespace_packages=["gcd"],
    zip_safe=False,
    scripts=["bin/gcd", "bin/gcdctl", "bin/gcdudp", "bin/genocide", "bin/genocided"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
