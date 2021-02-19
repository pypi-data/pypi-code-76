from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    include_package_data=True,
    name='snirocr',
    version='0.0.9',
    description='automatic ocr',
    long_description="""press the ctrl button two times, it will create a rectangle in the area you chose and ocr the image-the text will be copied to your clipboard""",
    url='',
    author='snir dekel',
    author_email='snirdekel101@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='optical computer vision',
    packages=find_packages(),
    install_requires=['keyboard', 'pytesseract', 'pyperclip', 'Pillow', 'playsound', 'pypiwin32', 'pyautogui', 'mega.py']
)