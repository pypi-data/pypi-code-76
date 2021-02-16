# pogfile shared imports
import subprocess
import sys
import argparse
import os
import shutil

# /pogfile shared imports

import inspect
import importlib
import logging as lg

from colorama import Fore, Style, init

init(autoreset=True)

gargs = None
g_jobs = {}

def get_gjobs():
    global g_jobs
    return g_jobs


def get_gargs():
    global gargs
    return gargs


class JobInfo:
    def __init__(self, func, desc, deps=None, default=False, name="Unknown", **kwargs):
        self.func = func
        self.docs = desc
        self.name = name
        self.deps = [*deps]
        # print("deps : ",self.deps)
        self.default = default
        self.extra = kwargs

    def explain_deps_nested(self, jobdict, _nest_count=None, _superiors=None):

        nest_count = 0 if _nest_count is None else _nest_count
        superiors = [] if _superiors is None else _superiors
        dash = "- "
        nest_count += 1
        for dep in self.deps:
            if dep not in jobdict:
                print(f"{' '*nest_count*2}{dash}{Fore.RED}{dep} (undefined dependency)")
            else:
                depinfo = jobdict[dep]
                descstr = "" if depinfo.docs == None else f": {Fore.CYAN}{depinfo.docs}"
                print(f"{' '*nest_count*2}{dash}{Fore.GREEN}{dep}{descstr}")
                if dep not in superiors:
                    superiors.append(dep)
                    jobdict[dep].explain_deps_nested(jobdict, nest_count, superiors)

    def get_deplist(self, deplist=None):
        global g_jobs

        if deplist is None:
            deplist = []

        for dep in self.deps:
            if not dep in g_jobs:
                print(
                    f"{Fore.RED}{dep} is listed as a dep of {self.name}, but is not a valid target"
                )
                continue

            if dep == self.name:
                print(f"warning: {self.name} has itself listed as a dependency")
                continue
            if dep not in deplist:
                deplist.append(dep)
                deplist += g_jobs[dep].get_deplist(deplist)

        odeplist = []

        for dep in deplist:
            if dep not in odeplist:
                odeplist.append(dep)
        return odeplist


def job(*deps, desc=None, default=True):
    def wrap(f):
        global g_jobs
        g_jobs[f.__name__] = JobInfo(
            f, desc, deps, default, f.__name__, where_defined=f.__code__.co_filename
        )

        def wrapped_f(*deps):
            f(*deps)

        return wrapped_f

    return wrap


class JobManager:
    def __init__(self, jobs):
        self.jobs = jobs
        self.defaults = []

        for name, info in self.jobs.items():
            if info.default:
                self.defaults.append(name)

        self.dispatched_jobs = []
        self.queued_jobs = []
        self.n_jobs = 0
        self.completed_jobs = []

    def queue_jobs(self, joblist):
        queued_jobs = joblist

        if "__ALL_JOBS__" in joblist:
            queued_jobs = self.defaults

        for jobname in queued_jobs:
            jobinfo = self.jobs[jobname]
            deplist = jobinfo.get_deplist()
            for dep in deplist:
                if dep not in queued_jobs:
                    queued_jobs.append(dep)

        self.queued_jobs = queued_jobs
        self.queued_count = len(queued_jobs)

        print("======================================================================")
        print("Queueing the following jobs:")
        maxshow = 10
        _maxshow = maxshow
        for job in self.queued_jobs:
            print(f"    {Fore.CYAN}{job}")
            maxshow -= 1
            if maxshow == 0:
                print(
                    f"    ... and {Fore.YELLOW}{self.queued_count - _maxshow}{Fore.RESET} more"
                )
                break
        print(f"  TOTAL: {Fore.YELLOW}{self.queued_count}")
        print("======================================================================")
        return queued_jobs

    def show_detailed_info(self, jobname):
        if jobname not in self.jobs:
            print(f"{Fore.RED}{jobname} is not a registered job")
            return
        job = self.jobs[jobname]
        print(f"Job: {Fore.CYAN}{jobname}")
        print(f"File: {Fore.CYAN}{job.extra['where_defined']}")
        print(f"Depends: ")
        job.explain_deps_nested(self.jobs)

    def show_jobs(self):
        word = "are"
        s = "s"
        default_jobs = []
        nondefault_jobs = []
        for name, job in self.jobs.items():
            if job.default:
                default_jobs.append(job)
            else:
                nondefault_jobs.append(job)

        if len(self.jobs) == 1:
            word = "is"
            s = ""

        def print_job(job):
            name = job.name
            asterix = "* "
            if not job.default:
                asterix = "  "
            else:
                asterix = "* "

            if job.docs is not None:
                print(f"   {asterix}{Fore.MAGENTA + name} - {Fore.GREEN + job.docs}")
            else:
                print(
                    f"   {asterix}{Fore.MAGENTA + name} - {Fore.YELLOW + 'no description available'}"
                )

        print(
            "\n======================================================================"
        )
        print(
            f"There {word} {Fore.YELLOW}{len(self.jobs)}{Style.RESET_ALL} job{s} registered: (* means part of the default)"
        )

        for job in default_jobs:
            print_job(job)

        for job in nondefault_jobs:
            print_job(job)
        print("======================================================================")

    def run_job(self, name):
        if name not in self.jobs:
            print(
                f"{Fore.RED}'{name}' is a listed job but we're skipping it because it is undefined..."
            )
            return

        job = self._get_job(name)

        if name not in self.completed_jobs:
            for dep in job.deps:
                if name == dep:
                    continue
                if dep not in self.completed_jobs:
                    self.run_job(dep)
            print(
                Fore.MAGENTA
                + f"=========== {Fore.GREEN}Running Job: "
                + Fore.CYAN
                + name
                + Fore.MAGENTA
                + f" [{Fore.GREEN}{len(self.completed_jobs) + 1}{Fore.MAGENTA}/{self.queued_count}] ======== "
            )
            try:
                job.func()
                self.completed_jobs.append(name)
            except:
                print(f"{Fore.RED}Job {name} failed")
                raise

    def run_jobs(self):
        for job in self.queued_jobs:
            self.run_job(job)

    def _get_job(self, jobname):
        job = self.jobs[jobname]
        return job

def get_manager():
    return JobManager(g_jobs)
