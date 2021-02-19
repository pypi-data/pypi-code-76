from distutils.core import setup

description = """

INSTALLATION:

python 3.x
	pip3 install GmicEffects
python 2.x
	pip install GmicEffects

USAGE:

for help:

    from GmicEffects import GmicEffects as ge\n
    import PIL.Image
    
    ge.help()#for help
    
for effects list:

    from GmicEffects import GmicEffects as ge\n
    import PIL.Image
    
    ge.effects()#for effects list

for example:

    from GmicEffects import GmicEffects as ge\n
    import PIL.Image
    
    oldPhoto = ge.old_photo("myphoto.png")#old photo effect
    
    # oldPhoto is pillow object
    
    oldPhoto.save("editedPhoto.png")#saved with pillow
"""

setup(
    name='GmicEffects',
    packages=['.'],
    version='0.1.2',
    description='Basic Gmic Effects',
    long_description=description,
    long_description_content_type="text/markdown",
    author='oguzY',
    author_email='oguzyesil17@gmail.com',
    url='https://github.com/oguzY147/GmicEffects',
    keywords=['Gmic', 'GmicEffects', 'effect', 'effects'],
    classifiers=["Programming Language :: Python :: 3"],
)
