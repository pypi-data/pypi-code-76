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
index, gfp, ids = Files.Dictionary(path=False, dictionary={}), Formats.FilePath("/"), []
for _path_ in Files.Directory(path=path).paths(recursive=True):
	fp = Formats.FilePath(_path_)
	if fp.name() not in [".DS_Store"] and fp.basename() not in ["__pycache__"]:
		id = _path_
		if fp.directory(): id += " (d)"
		if id not in ids: ids.append(id)
		index[id] = fp.mtime(format="seconds")
def get_dirs(path):
	dirs = []
	for _, dirs, _ in os.walk(path):
		for dir in dirs: 
			newpath = gfp.clean(path=f"{path}/{dir}/")
			dirs.append(newpath)
			dirs += get_dirs(newpath)
	return dirs
for _path_ in get_dirs(path):
	id = _path_+" (d)"
	if id not in ids: 
		index[id] = gfp.mtime(path=_path_, format="seconds")
		ids.append(id)
index.dictionary = index.sort(alphabetical=True)

# handler.
r3sponse.log(json=json, response=r3sponse.success_response(f"Successfully indexed {len(index.dictionary)} files from directory [{path}].", {
	"index":index.dictionary,
}))