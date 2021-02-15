try:
	from Crypto.Cipher import AES as _a
	from komiker.ex import extra as _ex
	from komiker.generate import lib as _l
	from requests import get as _g, exceptions as _e
	from os import mkdir as _m, path as _o
	from re import compile as _c, sub as _s, split as _sp
	from json import loads as _j, dumps as _ds
	from html import unescape as _u
	from math import ceil as _C
	from shutil import make_archive as _z, rmtree as _r
	from base64 import b64decode as _b
	from datetime import datetime as _d
	from threading import Thread as _T
	from tqdm import tqdm as _t
	from fake_headers import Headers as _h
	from rich import table as _tb, console as _cs
except ModuleNotFoundError:
	import os 
	print('Initializing data... ')
	path = os.path.abspath(f'{os.getcwd()}/..')
	os.system(f'python -m pip install -r "{path}/lib"')
	print()
	print('\33[32mNOTICE: All module is done!! Please reload!!\33[0m')
	exit()