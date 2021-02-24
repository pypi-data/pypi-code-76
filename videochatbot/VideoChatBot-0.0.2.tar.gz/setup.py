import setuptools

setuptools.setup(name='VideoChatBot',
    version='0.0.2',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent'
                ],
    install_requires=['ChatterBot', 'opencv-python', 'SpeechRecognition', 'matplotlib', 'imageio','pyttsx3', 'text2emotion', 'tensorflow', 'fer'],
    python_requires='>=3.6'
        )
