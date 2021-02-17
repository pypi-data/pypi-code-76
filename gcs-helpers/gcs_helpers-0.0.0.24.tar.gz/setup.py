from distutils.core import setup
setup(
  name = 'gcs_helpers',
  packages = [
    'gcs_helpers',
  ],
  package_dir = {
    'gcs_helpers': 'gcs_helpers'
  },
  version = '0.0.0.24',
  description = 'GCS_HELPERS: helper methods for working with google cloud storage',
  author = 'Brookie Guzder-Williams',
  author_email = 'brook.williams@gmail.com',
  url = 'https://github.com/brookisme/gcs_helpers',
  download_url = 'https://github.com/brookisme/gcs_helpers/tarball/0.1',
  keywords = ['python','google cloud storage','gcs'],
  include_package_data=False,
  data_files=[
    (
      'config',[]
    )
  ],
  install_requires=[
    'pandas',
    'numpy',
    'rasterio',
    'pyyaml',
    'affine',
    'pyproj',
    'geojson',
  ],
  classifiers = [],
  entry_points={
      'console_scripts': [
      ]
  }
)