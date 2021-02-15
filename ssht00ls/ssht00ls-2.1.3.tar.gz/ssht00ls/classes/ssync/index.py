#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, cl1
from fil3s import Files, Formats
from r3sponse import r3sponse

# arguments.
path = cl1.get_argument("--path")
json = cl1.arguments_present(["--json", "-j"])

# checks.
if not os.path.exists(path):
	r3sponse.log(json=json, response=r3sponse.error_response(f"Path [{path}] does not exist."))
elif not os.path.isdir(path):
	r3sponse.log(json=json, response=r3sponse.error_response(f"Path [{path}] is not a directory."))

# index.
index = {}
for path in Files.Directory(path=path).paths(recursive=True):
	index[path] = Formats.FilePath(path).mtime(format="seconds")

# handler.
r3sponse.log(json=json, response=r3sponse.success_response(f"Successfully indexed {len(index)} files from directory [{path}].", {
	"index":index,
}))