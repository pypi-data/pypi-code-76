from setuptools import setuptools

with open("README.md", "r") as fh:
      long_description = fh.read()

setuptools.setup(
      name='pxpy',
      version='1.0a66',
      author = 'Nico Piatkowski',
      author_email = 'nico.piatkowski@gmail.com',
      description = 'discrete pairwise undirected graphical models',
      long_description=long_description,
      url = 'https://www.randomfields.org/px',
      packages=['pxpy','pxpy.tools','pxpy.test'],
      package_data={'pxpy': ['pxpy_environ','lib/FILES','lib/libpx.so','lib/libpx_dbg.so','lib/libpx_ext_culbp.so','lib/libpx.dll','lib/libpx_aarch64.so','lib/libpx_aarch64_dbg.so','lib/libpx_aarch64_ext_culbp.so','data/sin44']},
      install_requires=['numpy'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
      ],
      python_requires='>=3.6'
)

