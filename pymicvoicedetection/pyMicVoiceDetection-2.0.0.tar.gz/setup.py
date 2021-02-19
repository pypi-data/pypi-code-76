# coding:utf-8

from setuptools import setup
# or
# from distutils.core import setup  
foruser = '''# Author:KuoYuan Li

[![N|Solid](https://images2.imgbox.com/8f/03/gv0QnOdH_o.png)](https://sites.google.com/ms2.ccsh.tn.edu.tw/pclearn0915)
本程式提供一個以能量為基準的 VAD(Voice Activitive Dectection)演算法
由 mic 動態擷取有聲段
背景能量門檻值可由 TH 值做設定

 '''
setup(
        name='pyMicVoiceDetection',   
        version='2.0.0',   
        description='easy Voice Activitive Dectection from MIC for python',
        long_description=foruser,
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://pypi.org/project/pyMicVoiceDetection',      
        packages=['pyMicVoiceDetection'],   
        include_package_data=True,
        keywords = ['Voice Activitive Detection', 'VAD','MicVoiceDetection'],   # Keywords that define your package best
          install_requires=[ 
          'numpy',
          'wave',
          'pyaudio',
          'matplotlib'
          ],
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
      ],
)
