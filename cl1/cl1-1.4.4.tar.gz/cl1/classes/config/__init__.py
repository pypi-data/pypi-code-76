#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, ast, json, glob, platform, subprocess, random
from fil3s import Files, Formats
from r3sponse import r3sponse

# functions.
def __get_operating_system__():
	os = platform.system().lower()
	if os in ["darwin"]: return "macos"
	elif os in ["linux"]: return "linux"
	else: raise ValueError(f"Unsupported operating system: [{os}].")

# source.
SOURCE_NAME = ALIAS = "cl1"
SOURCE_PATH = Formats.FilePath(__file__).base(back=3)
OS = __get_operating_system__()

# universal variables.
OWNER = os.environ.get("USER")
GROUP = "root"
HOME_BASE = "/home/"
HOME = f"/home/{os.environ.get('USER')}/"
MEDIA = f"/media/{os.environ.get('USER')}/"
if OS in ["macos"]: 
	HOME_BASE = "/Users/"
	HOME = f"/Users/{os.environ.get('USER')}/"
	MEDIA = f"/Volumes/"
	GROUP = "wheel"
