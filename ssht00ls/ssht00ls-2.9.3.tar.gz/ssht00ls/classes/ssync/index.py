#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, cl1, syst3m, sys
from fil3s import Files, Formats, gfp
from r3sponse import r3sponse
sys.path.insert(1, syst3m.defaults.source_path(__file__, back=4))
from utils import index

# arguments.
path = cl1.get_argument("--path")
json = cl1.arguments_present(["--json", "-j"])

# checks.
if not os.path.exists(path):
	r3sponse.log(response=r3sponse.error_response(f"Path [{path}] does not exist."), json=json)
elif not os.path.isdir(path):
	r3sponse.log(response=r3sponse.error_response(f"Path [{path}] is not a directory."), json=json)

# handler.
dict = index(path)
r3sponse.log(json=json, response=r3sponse.success_response(f"Successfully indexed {len(dict)} files from directory [{path}].", {
	"index":dict,
}))