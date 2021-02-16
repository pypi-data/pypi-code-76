# pogfile shared imports
import subprocess
import sys
import argparse
import os
import shutil

# /pogfile shared imports

import logging as lg

from . import core
from .core import job, JobManager
from .jobenv import JobEnv
from importlib import util
import importlib


def find_all_subpogs(root):
    return subpogs


def inner_importer(root, cli_args, _filename=None):
    """
    Runs the importer for a target file and
    directory,

    :return: g_jobs, a glob of all the jbos in that file
    """

    filename = _filename
    if _filename == None:
        filename = "pogfile"

    apath = os.path.abspath(os.path.join(root, filename))
    if not os.path.exists(apath):
        tapath = os.path.abspath(os.path.join(root, filename + ".py"))
        assert os.path.exists(
            tapath
        ), f" Neither {root + apath} or the .py version exists"
        apath = tapath

    orig_dir = os.path.dirname(apath)

    loader = importlib.machinery.SourceFileLoader("tmpPackage", apath)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)

    # pogfile extra symbols
    mod.job = job  # job decorator
    mod.cli_args = cli_args  # parsed command line arguments
    mod.pogmake_core = core  # Access to all pogmake
    # internals but not the importer or the frontend
    mod.orig_dir = orig_dir  # absolute path to origin of this pogfile
    # /pogfile extra symbols

    # standard imports
    mod.sys = sys
    mod.subprocess = subprocess
    mod.shutil = shutil
    mod.os = os
    mod.include_paths = []
    mod.exclude_paths = []
    mod.env = JobEnv(orig_dir, cli_args)
    
    if not hasattr(mod, "autoindex"):
    
        mod.autoindex = False

    loader.exec_module(mod)

    gjobs = mod.pogmake_core.get_gjobs()
    for path in mod.include_paths:
        jpath = os.path.join(root, path)

        if not os.path.exists(jpath):
            print(f"Include path in {apath} does not exist: {jpath}")
            continue

        if os.path.isdir(jpath):
            rjobs, modinfo = inner_importer(jpath, cli_args)
            gjobs.update(rjobs)

        else:
            rjobs, modinfo = inner_importer(
                os.path.dirname(jpath),
                cli_args,
                os.path.basename(jpath)
            )

            gjobs.update(rjobs)

    return gjobs, mod

def main_importer(root, cli_args, startfile=None):
    gjobs, startmod = inner_importer(root, cli_args, startfile)
    
    if startmod.autoindex:
        rjobs = autoindex_importer(root, cli_args)
        gjobs.update(rjobs)

    return gjobs


def autoindex_importer(root, cli_args, filename="pogfile"):
    subpogs = []
    first = True
    gjobs = {}
    excluded = []
    for r, d, f in os.walk(root):
        should_skip = False
        for path in excluded:
            if r.startswith(os.path.abspath(path) + os.sep) or r == path:
                should_skip = True

        if not should_skip:
            for fname in f:
                if fname == filename or fname == filename+".py":
                    rjobs, modinfo = inner_importer(r, cli_args)
                    gjobs.update(rjobs)
                    for epath in modinfo.exclude_paths:
                        excluded.append(os.path.abspath(os.path.join(r, epath)))

    return gjobs
