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
	r3sponse.log(response=r3sponse.error_response(f"Path [{path}] does not exist."), json=json)
elif not os.path.isdir(path):
	r3sponse.log(response=r3sponse.error_response(f"Path [{path}] is not a directory."), json=json)

# index.
index, gfp, dir, ids = Files.Dictionary(path=False, dictionary={}), Formats.FilePath("/"), Files.Directory(path=path), []
for _path_ in dir.paths(recursive=True, files_only=True, banned_names=[".DS_Store", "__pycache__"]):
	if _path_ not in ids: 
		index[_path_] = gfp.mtime(format="seconds")
		ids.append(_path_)
for _path_ in dir.paths(recursive=True, dirs_only=True, banned_names=[".DS_Store", "__pycache__"]):
	id = _path_+" (d)"
	if os.listdir(_path_) == []: id += " (e)"
	if id not in ids: 
		index[id] = gfp.mtime(path=_path_, format="seconds")
		ids.append(id)
index.dictionary = index.sort(alphabetical=True)

# handler.
r3sponse.log(json=json, response=r3sponse.success_response(f"Successfully indexed {len(index.dictionary)} files from directory [{path}].", {
	"index":index.dictionary,
}))