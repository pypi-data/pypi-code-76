from setuptools import setup, find_packages

with open("readme", "r", encoding="utf-8") as des:
    long_description = des.read()

# scr ent fy

setup(
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patod01/beta-beam",
    #project_urls={},
    packages=find_packages(),
    #py_modules=[], # alone
    install_requires=[],
    python_requires='>=3.9',
    #package_data={'pnomo':['../readme']},
    #data_files=[('',['readme'])], # zona mapa
    scripts=[],
    entry_points={
        'console_scripts': [
            'peta=pnomo.lib:run',
        ],
    },
)
