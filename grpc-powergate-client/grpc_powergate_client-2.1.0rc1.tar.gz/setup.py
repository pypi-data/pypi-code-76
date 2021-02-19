import setuptools

setuptools.setup(
    name="grpc_powergate_client",
    version="2.1.0-rc1",
    author="Textile",
    author_email="contact@textile.io",
    url="https://github.com/textileio/powergate",
    packages=setuptools.find_packages(where="src"),
    package_dir={'': 'src'},
    install_requires=[
      'protobuf',
      'grpcio',
    ],
)
