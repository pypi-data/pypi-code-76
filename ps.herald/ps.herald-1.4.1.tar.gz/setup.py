from setuptools import setup
install_requires=["Flask", "click", "flask-sqlalchemy", 
                  "graphene","graphene_sqlalchemy", "flask-graphql", "flask-cors", 
                  "ps.basic",]
version='1.4.1'

setup(
    name="ps.herald",
    version=version,
    long_description=open("README.rst").read() + "\n" ,
    classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Operating System :: MacOS',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development',
          'Topic :: Utilities',
      ], 
    keywords='PS',
    author='Setz',
    url='https://bitbucket.org/drsetz/ps.herald',
    author_email='Thomas.Setz@acm.org',
    license='"License :: OSI Approved :: GNU General Public License (GPL)', 
    packages=["ps.herald"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "ps_neelix=ps.herald.ps_neelix:main",
            "ps_bridge=ps.herald.ps_bridge:main",
            "ps_herald=ps.herald.ps_herald:main",
        ],
    },
)
