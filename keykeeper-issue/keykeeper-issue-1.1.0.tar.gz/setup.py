from distutils.core import setup

setup(name='keykeeper-issue',
      version='1.1.0',
      description='Desciption for keykeeperissue here',
      author='Ville M. Vainio',
      author_email='ville.vainio@basware.com',
      url='https://github.com/vivainio/keykeeper',
      packages=['keykeeperissue'],
      install_requires=["boto3", "jwcrypto"],
      entry_points={
          'console_scripts': [
              'keykeeper-issue = keykeeperissue.cli:main'
          ]
      }
      )
