from setuptools import setup


setup(name='QCGym', version='v0.0.3-alpha', packages=['QCGym'], license='MIT',
      description='A Collection of Gym environments used in Quantum control',
      author='Onkar Deshpande', author_email='onkardeshpande07@gmail.com',
      url='https://github.com/oddgr8/QCGym',
      download_url='https://github.com/oddgr8/QCGym/archive/v0.0.3-alpha.tar.gz',
      keywords=['Quantum', 'Control', 'Gym', 'RL'],
      # And any other dependencies foo needs,
      install_requires=['gym', 'numpy', 'scipy'],
      classifiers=[
          # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
          'Development Status :: 3 - Alpha',
          # Define that your audience are developers
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',   # Again, pick a license
          # Specify which python versions that you want to support
          'Programming Language :: Python :: 3.8',
],
)
