from setuptools import setup
from setuptools.command.install import install


class AbortInstall(install):
    def run(self):
        raise SystemExit(
            "You're trying to install statice from pypi,"
            "however, it can be installed only from a private repository."
            "Please read the installation docs and contact your statice"
            "representative in case of any issues or questions.")


description = 'A fake package to warn the user they are not installing the correct package.'

setup(
    name='statice',
    version='1.0.0',
    description=description,
    long_description=description,
    author='Statice GmbH',
    author_email='support@statice.ai',
    url='https://www.statice.ai',
    cmdclass={
        'install': AbortInstall,
    },
    packages=['statice'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'License :: Other/Proprietary License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX',
    ],
)
