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
index = Files.Dictionary(path=False, dictionary={})
for _path_ in Files.Directory(path=path).paths(recursive=True):
	fp = Formats.FilePath(_path_)
	id = _path_
	if fp.directory(): id += " (d)"
	basepath = fp.base()
	base, known = Formats.FilePath(basepath), True
	if base.exists() and basepath not in path:
		try: index.dictionary[base.path]
		except: known = False
	if base.path not in index:
		index[base.path+" (d)"] = base.mtime(format="seconds")
	index[id] = fp.mtime(format="seconds")
index.dictionary = index.sort(alphabetical=True)

# handler.
r3sponse.log(json=json, response=r3sponse.success_response(f"Successfully indexed {len(index.dictionary)} files from directory [{path}].", {
	"index":index.dictionary,
}))