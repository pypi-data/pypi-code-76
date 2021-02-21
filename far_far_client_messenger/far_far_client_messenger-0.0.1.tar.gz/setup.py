from setuptools import setup, find_packages

setup(name="far_far_client_messenger",
      version="0.0.1",
      description="far_far_messenger",
      author="Fedor Polyakov",
      author_email="fp@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
