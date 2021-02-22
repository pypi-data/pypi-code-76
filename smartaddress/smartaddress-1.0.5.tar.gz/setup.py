from setuptools import setup, find_packages
# from setuptools import setup

setup(
    name='smartaddress',
    version='1.0.5',
    author='andy',
    author_email='liuxiaoming@yihaohulian.com',
    description='Intelligent resolution of receiving address',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    # url='',
    packages=find_packages(),
    # packages=['smartaddress', 'smartaddress.datas'],
    # py_modules=['smartaddress.address'],
    # packages=['smartaddress.datas'],
    python_requires='>=3.6',
)