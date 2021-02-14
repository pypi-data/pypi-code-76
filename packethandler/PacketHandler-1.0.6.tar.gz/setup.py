from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()



setup_args = dict(
    name='PacketHandler',
    version='1.0.6',
    description='Store data as packet. Serialize, Deserialize and Send, Recv, Encrypt, it.',
    long_description_content_type="text/markdown",
    long_description=README ,
    license='GPL',
    packages=["PacketHandler"],
    author='Emre Demircan',
    author_email='emrecpp1@gmail.com',
    keywords=['Packet', 'socket', 'Handler','PacketHandler', 'Packet Handler', 'send', 'recv','serialize','serialization','deserialize','deserialization','compress','encrypt'],
    url='https://github.com/emrecpp/PacketHandler',
    download_url='https://pypi.org/project/PacketHandler/',
    include_package_data=True

)

install_requires = [    
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)