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
    name='snirpinball',
    version='0.0.2',
    description='a bot that can play pinball by himself',
    long_description="cool bot that plays pinball by tracking the ball",
    url='',
    author='snir dekel',
    author_email='snirdekel101@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='computer vision',
    packages=find_packages(),
    install_requires=['mss', 'opencv-python', 'opencv-contrib-python', 'Pillow', 'pydirectinput', 'pyautogui', 'pygetwindow']
)