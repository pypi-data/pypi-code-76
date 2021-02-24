from setuptools import setup

setup(name='pyndf',
      version='2.1',
      description='Library to read, write amd create Neurobit Data Format (NDF) file and stream.',
      url='https://www.neurobit.io',
      author='Amiya Patanaik@Neurobit Technologies',
      author_email='amiya@neurobit.io',
      license='EULA',
      packages=['pyndf'],
      install_requires=[
          'numpy',
          'scikit-image',
          'scipy',
          'msgpack',
          'msgpack_numpy',
          'py-ecg-detectors',
          'numba'
      ],
      zip_safe=False)
